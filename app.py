import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Tuple, Optional
import re
from dataclasses import dataclass
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg

@dataclass
class Piece:
    code: str
    description: str
    width: int
    height: int
    material: str
    qty: int

@dataclass
class Placement:
    x: int
    y: int
    width: int
    height: int
    code: str
    description: str
    rotated: bool

@dataclass
class Sheet:
    id: int
    placements: List[Placement]
    waste_area: float

class KickplateNester:
    def __init__(self, stock_width: int, stock_height: int, kerf_width: int, grain_direction: str):
        self.stock_width = stock_width
        self.stock_height = stock_height
        self.kerf_width = kerf_width
        self.grain_direction = grain_direction
    
    def parse_kickplate_code(self, code: str) -> Optional[Dict]:
        """Parse kickplate code like KP300300SSS into dimensions and material"""
        match = re.match(r'^KP(\d{3,4})(\d{3,4})(.+)$', code, re.IGNORECASE)
        if not match:
            return None
        
        width = int(match.group(1))
        height = int(match.group(2))
        material = match.group(3)
        
        if width <= 0 or height <= 0:
            return None
        
        return {'width': width, 'height': height, 'material': material}
    
    def find_gaps(self, placements: List[Placement], max_w: int, max_h: int, kerf: int) -> List[Dict]:
        """Find available gaps in the sheet"""
        gaps = []
        sorted_placements = sorted(placements, key=lambda p: (p.y, p.x))
        
        for p in sorted_placements:
            # Right of piece
            gaps.append({
                'x': p.x + p.width + kerf,
                'y': p.y,
                'width': max_w - (p.x + p.width + kerf),
                'height': p.height
            })
            
            # Above piece
            gaps.append({
                'x': p.x,
                'y': p.y + p.height + kerf,
                'width': p.width,
                'height': max_h - (p.y + p.height + kerf)
            })
        
        # Filter valid gaps
        valid_gaps = []
        for gap in gaps:
            if gap['width'] <= 0 or gap['height'] <= 0:
                continue
            if gap['x'] >= max_w or gap['y'] >= max_h:
                continue
            
            # Check if gap overlaps with any placement
            overlaps = False
            for p in placements:
                if not (gap['x'] >= p.x + p.width + kerf or
                       gap['x'] + gap['width'] <= p.x or
                       gap['y'] >= p.y + p.height + kerf or
                       gap['y'] + gap['height'] <= p.y):
                    overlaps = True
                    break
            
            if not overlaps:
                valid_gaps.append(gap)
        
        return sorted(valid_gaps, key=lambda g: g['x'] + g['y'])
    
    def find_placement(self, sheet: Sheet, piece: Piece) -> Optional[Placement]:
        """Find a placement for a piece on a sheet"""
        orientations = []
        if self.grain_direction == 'none':
            orientations = [
                {'w': piece.width, 'h': piece.height, 'rotated': False},
                {'w': piece.height, 'h': piece.width, 'rotated': True}
            ]
        else:
            orientations = [{'w': piece.width, 'h': piece.height, 'rotated': False}]
        
        for orient in orientations:
            if len(sheet.placements) == 0:
                if orient['w'] <= self.stock_width and orient['h'] <= self.stock_height:
                    return Placement(
                        x=0, y=0,
                        width=orient['w'],
                        height=orient['h'],
                        code=piece.code,
                        description=piece.description,
                        rotated=orient['rotated']
                    )
            else:
                gaps = self.find_gaps(sheet.placements, self.stock_width, 
                                     self.stock_height, self.kerf_width)
                for gap in gaps:
                    if orient['w'] <= gap['width'] and orient['h'] <= gap['height']:
                        return Placement(
                            x=gap['x'], y=gap['y'],
                            width=orient['w'],
                            height=orient['h'],
                            code=piece.code,
                            description=piece.description,
                            rotated=orient['rotated']
                        )
        
        return None
    
    def nest_pieces(self, pieces: List[Piece]) -> List[Sheet]:
        """Nest all pieces onto sheets"""
        sheets = []
        current_sheet = Sheet(id=0, placements=[], 
                            waste_area=self.stock_width * self.stock_height)
        sheets.append(current_sheet)
        
        # Expand pieces by quantity
        all_pieces = []
        for piece in pieces:
            for i in range(piece.qty):
                all_pieces.append(piece)
        
        # Sort by area (largest first)
        all_pieces.sort(key=lambda p: p.width * p.height, reverse=True)
        
        # Place each piece
        for piece in all_pieces:
            placed = False
            
            for sheet in sheets:
                placement = self.find_placement(sheet, piece)
                if placement:
                    sheet.placements.append(placement)
                    used_area = sum(p.width * p.height for p in sheet.placements)
                    sheet.waste_area = (self.stock_width * self.stock_height) - used_area
                    placed = True
                    break
            
            if not placed:
                current_sheet = Sheet(id=len(sheets), placements=[], 
                                    waste_area=self.stock_width * self.stock_height)
                sheets.append(current_sheet)
                placement = self.find_placement(current_sheet, piece)
                if placement:
                    current_sheet.placements.append(placement)
                    used_area = sum(p.width * p.height for p in current_sheet.placements)
                    current_sheet.waste_area = (self.stock_width * self.stock_height) - used_area
        
        return sheets

def create_sheet_visualization(sheet: Sheet, stock_width: int, stock_height: int, 
                               grain_direction: str) -> go.Figure:
    """Create a Plotly visualization of a sheet layout"""
    fig = go.Figure()
    
    # Add sheet boundary
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=stock_width, y1=stock_height,
        line=dict(color="black", width=3),
        fillcolor="white"
    )
    
    # Add grid lines every 100mm
    for i in range(100, stock_width, 100):
        fig.add_shape(type="line", x0=i, y0=0, x1=i, y1=stock_height,
                     line=dict(color="lightgray", width=1, dash="dot"))
    for i in range(100, stock_height, 100):
        fig.add_shape(type="line", x0=0, y0=i, x1=stock_width, y1=i,
                     line=dict(color="lightgray", width=1, dash="dot"))
    
    # Add pieces
    colors_list = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
    for i, p in enumerate(sheet.placements):
        color = colors_list[i % len(colors_list)]
        
        # Add rectangle
        fig.add_shape(
            type="rect",
            x0=p.x, y0=p.y, x1=p.x + p.width, y1=p.y + p.height,
            line=dict(color="darkblue", width=2),
            fillcolor=color,
            opacity=0.7
        )
        
        # Add text label
        fig.add_annotation(
            x=p.x + p.width/2,
            y=p.y + p.height/2,
            text=f"{p.code}<br>{p.width}×{p.height}{'↻' if p.rotated else ''}",
            showarrow=False,
            font=dict(color="white", size=10, family="monospace"),
            bgcolor=color,
            opacity=0.9
        )
    
    fig.update_layout(
        title=f"Sheet {sheet.id + 1} - Efficiency: {100 - (sheet.waste_area / (stock_width * stock_height) * 100):.1f}%",
        xaxis=dict(title="Width (mm)", range=[0, stock_width]),
        yaxis=dict(title="Height (mm)", range=[0, stock_height], scaleanchor="x", scaleratio=1),
        width=900,
        height=600,
        showlegend=False
    )
    
    return fig

def create_matplotlib_diagram(sheet: Sheet, stock_width: int, stock_height: int, 
                             grain_direction: str) -> io.BytesIO:
    """Create a matplotlib diagram for PDF export"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set up the plot
    ax.set_xlim(0, stock_width)
    ax.set_ylim(0, stock_height)
    ax.set_aspect('equal')
    
    # Add grid lines every 100mm
    for i in range(0, stock_width + 1, 100):
        ax.axvline(i, color='lightgray', linewidth=0.5, linestyle='--', alpha=0.5)
    for i in range(0, stock_height + 1, 100):
        ax.axhline(i, color='lightgray', linewidth=0.5, linestyle='--', alpha=0.5)
    
    # Draw sheet boundary
    boundary = patches.Rectangle((0, 0), stock_width, stock_height, 
                                linewidth=3, edgecolor='black', 
                                facecolor='white', fill=True)
    ax.add_patch(boundary)
    
    # Color palette
    color_palette = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
    
    # Draw each piece
    for i, p in enumerate(sheet.placements):
        color = color_palette[i % len(color_palette)]
        
        # Draw rectangle
        rect = patches.Rectangle((p.x, p.y), p.width, p.height,
                                linewidth=2, edgecolor='darkblue',
                                facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        
        # Add text label
        text_x = p.x + p.width / 2
        text_y = p.y + p.height / 2
        
        label = f"{p.code}\n{p.width}×{p.height}"
        if p.rotated:
            label += " ↻"
        
        ax.text(text_x, text_y, label,
               ha='center', va='center',
               fontsize=8, fontweight='bold',
               color='white',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.9))
    
    # Labels and title
    efficiency = 100 - (sheet.waste_area / (stock_width * stock_height) * 100)
    ax.set_xlabel('Width (mm)', fontsize=10)
    ax.set_ylabel('Height (mm)', fontsize=10)
    ax.set_title(f'Sheet {sheet.id + 1} - Efficiency: {efficiency:.1f}%', 
                fontsize=12, fontweight='bold')
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    # Save to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    return buf

def generate_pdf_cutlist(sheets: List[Sheet], stock_width: int, stock_height: int, 
                        grain_direction: str, filename: str = "cut_list.pdf") -> bytes:
    """Generate a PDF cut list with diagrams and tables"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                           rightMargin=20, leftMargin=20,
                           topMargin=30, bottomMargin=20)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Add title
    title = Paragraph("Kickplate Cutting List", title_style)
    elements.append(title)
    
    # Add generation info
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    info_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>"
    info_text += f"Stock Size: {stock_width}mm × {stock_height}mm<br/>"
    info_text += f"Grain Direction: {grain_direction.title()}<br/>"
    info_text += f"Total Sheets: {len(sheets)}"
    
    elements.append(Paragraph(info_text, info_style))
    elements.append(Spacer(1, 20))
    
    # Summary table
    summary_data = [['Sheet', 'Pieces', 'Efficiency', 'Waste Area']]
    for sheet in sheets:
        efficiency = 100 - (sheet.waste_area / (stock_width * stock_height) * 100)
        summary_data.append([
            f"Sheet {sheet.id + 1}",
            str(len(sheet.placements)),
            f"{efficiency:.1f}%",
            f"{sheet.waste_area:.0f} mm²"
        ])
    
    summary_table = Table(summary_data, colWidths=[60*mm, 40*mm, 40*mm, 50*mm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    elements.append(summary_table)
    elements.append(PageBreak())
    
    # Add each sheet with visual diagram
    for sheet in sheets:
        # Sheet header
        sheet_title = Paragraph(f"<b>Sheet {sheet.id + 1}</b> - {len(sheet.placements)} pieces", 
                               styles['Heading2'])
        elements.append(sheet_title)
        elements.append(Spacer(1, 10))
        
        # Create visual diagram using matplotlib
        img_buffer = create_matplotlib_diagram(sheet, stock_width, stock_height, grain_direction)
        
        # Add image to PDF
        img = Image(img_buffer, width=240*mm, height=160*mm)
        elements.append(img)
        elements.append(Spacer(1, 15))
        
        # Cutting instructions table
        table_data = [['#', 'Part Code', 'Description', 'X (mm)', 'Y (mm)', 'Width', 'Height', 'Rotated']]
        
        for i, p in enumerate(sheet.placements):
            table_data.append([
                str(i + 1),
                p.code,
                p.description[:30],  # Truncate long descriptions
                str(p.x),
                str(p.y),
                str(p.width),
                str(p.height),
                '↻' if p.rotated else '-'
            ])
        
        col_widths = [15*mm, 30*mm, 50*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm]
        detail_table = Table(table_data, colWidths=col_widths)
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(detail_table)
        
        # Add page break between sheets (except last one)
        if sheet.id < len(sheets) - 1:
            elements.append(PageBreak())
        else:
            elements.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def main():
    st.set_page_config(page_title="Kickplate Nesting Optimizer", layout="wide")
    
    st.title("🔧 Kickplate Nesting Optimizer")
    st.markdown("Optimize cutting layouts for kickplates from stock sheets")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        stock_width = st.number_input("Stock Width (mm)", value=2400, min_value=100, step=10)
        stock_height = st.number_input("Stock Height (mm)", value=1200, min_value=100, step=10)
        kerf_width = st.number_input("Kerf Width (mm)", value=3, min_value=0, step=1)
        grain_direction = st.selectbox(
            "Grain Direction",
            options=['horizontal', 'vertical', 'none'],
            format_func=lambda x: {
                'horizontal': 'Horizontal (no rotation)',
                'vertical': 'Vertical (no rotation)',
                'none': 'No preference (allow rotation)'
            }[x]
        )
    
    # Main content
    tab1, tab2 = st.tabs(["📤 Upload Order CSV", "➕ Manual Entry"])
    
    with tab1:
        st.subheader("Upload Order CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} rows from {uploaded_file.name}")
            
            # Filter kickplate items
            kickplate_df = df[df['PartCode'].str.startswith('KP', na=False)].copy()
            
            if len(kickplate_df) > 0:
                st.write(f"Found {len(kickplate_df)} kickplate items:")
                st.dataframe(kickplate_df[['PartCode', 'Description', 'ProductQuantity', 'ProductPrice']])
                
                # Show summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Unique Items", len(kickplate_df))
                with col2:
                    total_qty = kickplate_df['ProductQuantity'].sum()
                    st.metric("Total Pieces", int(total_qty))
                with col3:
                    total_cost = (kickplate_df['ProductCost'] * kickplate_df['ProductQuantity']).sum()
                    st.metric("Total Cost", f"${total_cost:.2f}")
                with col4:
                    total_price = (kickplate_df['ProductPrice'] * kickplate_df['ProductQuantity']).sum()
                    st.metric("Total Revenue", f"${total_price:.2f}")
                
                if st.button("🚀 Generate Cut List", type="primary", use_container_width=True):
                    nester = KickplateNester(stock_width, stock_height, kerf_width, grain_direction)
                    
                    # Parse pieces
                    pieces = []
                    for _, row in kickplate_df.iterrows():
                        parsed = nester.parse_kickplate_code(row['PartCode'])
                        if parsed:
                            pieces.append(Piece(
                                code=row['PartCode'],
                                description=row['Description'],
                                width=parsed['width'],
                                height=parsed['height'],
                                material=parsed['material'],
                                qty=int(row['ProductQuantity'])
                            ))
                    
                    # Nest pieces
                    with st.spinner("Optimizing layout..."):
                        sheets = nester.nest_pieces(pieces)
                    
                    st.success(f"✅ Generated cut list with {len(sheets)} sheet(s)")
                    
                    # Summary metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sheets Required", len(sheets))
                    with col2:
                        total_pieces = sum(len(s.placements) for s in sheets)
                        st.metric("Total Pieces", total_pieces)
                    with col3:
                        avg_efficiency = sum(100 - (s.waste_area / (stock_width * stock_height) * 100) for s in sheets) / len(sheets)
                        st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
                    
                    # Display sheets
                    for sheet in sheets:
                        with st.expander(f"📋 Sheet {sheet.id + 1} - {len(sheet.placements)} pieces", expanded=True):
                            fig = create_sheet_visualization(sheet, stock_width, stock_height, grain_direction)
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Cutting instructions
                            st.subheader("Cutting Instructions")
                            cut_data = []
                            for i, p in enumerate(sheet.placements):
                                cut_data.append({
                                    'Piece #': i + 1,
                                    'Part Code': p.code,
                                    'Description': p.description,
                                    'X (mm)': p.x,
                                    'Y (mm)': p.y,
                                    'Width (mm)': p.width,
                                    'Height (mm)': p.height,
                                    'Rotated': '↻ Yes' if p.rotated else 'No'
                                })
                            st.dataframe(pd.DataFrame(cut_data), use_container_width=True)
                    
                    # Download button
                    cut_list_data = []
                    for sheet in sheets:
                        for i, p in enumerate(sheet.placements):
                            cut_list_data.append({
                                'Sheet': sheet.id + 1,
                                'Piece #': i + 1,
                                'Part Code': p.code,
                                'Description': p.description,
                                'X Position': p.x,
                                'Y Position': p.y,
                                'Width': p.width,
                                'Height': p.height,
                                'Rotated': 'Yes' if p.rotated else 'No'
                            })
                    
                    csv = pd.DataFrame(cut_list_data).to_csv(index=False)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name="cut_list.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    with col2:
                        pdf_data = generate_pdf_cutlist(sheets, stock_width, stock_height, grain_direction)
                        st.download_button(
                            label="📄 Download PDF",
                            data=pdf_data,
                            file_name="cut_list.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
            else:
                st.warning("No kickplate items (starting with 'KP') found in the CSV")
    
    with tab2:
        st.subheader("Manual Entry")
        st.info("Add kickplates manually using the form below")
        
        if 'manual_items' not in st.session_state:
            st.session_state.manual_items = []
        if 'manual_sheets' not in st.session_state:
            st.session_state.manual_sheets = None
        
        with st.form("add_item_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                width = st.number_input("Width (mm)", min_value=1, value=300, step=10)
            with col2:
                height = st.number_input("Height (mm)", min_value=1, value=300, step=10)
            with col3:
                qty = st.number_input("Quantity", min_value=1, value=1)
            
            col4, col5 = st.columns(2)
            with col4:
                material = st.text_input("Material Code", value="SSS", help="Default: SSS (Stainless Steel)").upper()
            with col5:
                description = st.text_input("Description (optional)", value="", placeholder="e.g., Kitchen kickplate")
            
            submitted = st.form_submit_button("Add Item", use_container_width=True)
            if submitted:
                code = f"KP{width}{height}{material}"
                if not description:
                    description = f"{width}×{height}mm {material}"
                
                st.session_state.manual_items.append({
                    'code': code,
                    'width': width,
                    'height': height,
                    'material': material,
                    'description': description,
                    'qty': qty
                })
                st.success(f"Added {code} ({width}×{height}mm) × {qty}")
                st.rerun()
        
        if st.session_state.manual_items:
            st.write("### Current items:")
            display_items = []
            for item in st.session_state.manual_items:
                display_items.append({
                    'Part Code': item['code'],
                    'Width (mm)': item['width'],
                    'Height (mm)': item['height'],
                    'Material': item['material'],
                    'Description': item['description'],
                    'Quantity': item['qty']
                })
            items_df = pd.DataFrame(display_items)
            st.dataframe(items_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear All", use_container_width=True):
                    st.session_state.manual_items = []
                    st.session_state.manual_sheets = None
                    st.rerun()
            with col2:
                if st.button("🚀 Generate Cut List", type="primary", use_container_width=True, key="manual_generate"):
                    nester = KickplateNester(stock_width, stock_height, kerf_width, grain_direction)
                    pieces = [Piece(
                        code=item['code'],
                        description=item['description'],
                        width=item['width'],
                        height=item['height'],
                        material=item['material'],
                        qty=item['qty']
                    ) for item in st.session_state.manual_items]
                    
                    with st.spinner("Optimizing layout..."):
                        st.session_state.manual_sheets = nester.nest_pieces(pieces)
                    st.rerun()
        
        # Display results
        if st.session_state.manual_sheets:
            sheets = st.session_state.manual_sheets
            st.success(f"✅ Generated cut list with {len(sheets)} sheet(s)")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sheets Required", len(sheets))
            with col2:
                total_pieces = sum(len(s.placements) for s in sheets)
                st.metric("Total Pieces", total_pieces)
            with col3:
                avg_efficiency = sum(100 - (s.waste_area / (stock_width * stock_height) * 100) for s in sheets) / len(sheets)
                st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
            
            for sheet in sheets:
                with st.expander(f"📋 Sheet {sheet.id + 1} - {len(sheet.placements)} pieces", expanded=True):
                    fig = create_sheet_visualization(sheet, stock_width, stock_height, grain_direction)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Cutting instructions
                    st.subheader("Cutting Instructions")
                    cut_data = []
                    for i, p in enumerate(sheet.placements):
                        cut_data.append({
                            'Piece #': i + 1,
                            'Part Code': p.code,
                            'Description': p.description,
                            'X (mm)': p.x,
                            'Y (mm)': p.y,
                            'Width (mm)': p.width,
                            'Height (mm)': p.height,
                            'Rotated': '↻ Yes' if p.rotated else 'No'
                        })
                    st.dataframe(pd.DataFrame(cut_data), use_container_width=True)
            
            # Download button
            cut_list_data = []
            for sheet in sheets:
                for i, p in enumerate(sheet.placements):
                    cut_list_data.append({
                        'Sheet': sheet.id + 1,
                        'Piece #': i + 1,
                        'Part Code': p.code,
                        'Description': p.description,
                        'X Position': p.x,
                        'Y Position': p.y,
                        'Width': p.width,
                        'Height': p.height,
                        'Rotated': 'Yes' if p.rotated else 'No'
                    })
            
            csv = pd.DataFrame(cut_list_data).to_csv(index=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="manual_cut_list.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col2:
                pdf_data = generate_pdf_cutlist(sheets, stock_width, stock_height, grain_direction)
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_data,
                    file_name="manual_cut_list.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()