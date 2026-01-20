# Kickplate Nesting Optimizer - User Manual

**Hardware Direct**
*Professional kickplate cutting optimization and door label generation*

---

## Overview

### What It Does
The Kickplate Nesting Optimizer is a professional tool that:
- Optimizes the layout of kickplates on stock sheets to minimize waste
- Generates cutting diagrams for production
- Creates door labels from finishing schedules
- Produces cut lists and production PDFs

### Who It's For
- Production managers
- Workshop supervisors
- Estimators
- Project coordinators
- Anyone responsible for kickplate ordering and cutting

### Key Benefits
- **Reduce Material Waste**: Intelligent nesting algorithms maximize sheet usage
- **Save Time**: Automate cutting layouts instead of manual planning
- **Improve Accuracy**: Generate precise cutting instructions
- **Professional Output**: Print-ready PDFs and labels
- **Flexible Input**: Upload CSV, PDF, or enter manually

---

## Getting Started

### Accessing the App
1. Navigate to the Streamlit app URL (provided by IT/admin)
2. The app loads in your web browser
3. No installation required

### Basic Navigation
The app has **4 main tabs**:
1. **Upload Order CSV** - Import kickplate orders from CSV files
2. **Manual Entry** - Add kickplates one by one
3. **Door Labels** - Generate labels from finishing schedules
4. **Debug Tools** - Technical troubleshooting

### Sidebar Configuration
The left sidebar contains settings that apply to all tabs:

**⚙️ Configuration**
- **Stock Width (mm)**: Width of your stock sheets (default: 2400mm)
- **Stock Height (mm)**: Height of your stock sheets (default: 1200mm)
- **Kerf Width (mm)**: Saw blade thickness for cut spacing (default: 0mm)
- **Grain Direction**: Material grain constraints
  - *Horizontal*: No rotation allowed, grain runs horizontally
  - *Vertical*: No rotation allowed, grain runs vertically
  - *No preference*: Pieces can be rotated for better fit

**🏷️ Label Settings**
- **Label Width (mm)**: Width of printed labels (default: 60mm)
- **Label Height (mm)**: Height of printed labels (default: 70mm)
- **Include Project Code**: Toggle project code on labels

**📋 Project Info**
- **Project Code**: e.g., "Q30683B"
- **Project Name**: e.g., "Matamata Indoor Sports Facility"

---

## Features Guide

### Tab 1: Upload Order CSV

#### Purpose
Import kickplate orders from Cin7/ProMaster shipment CSVs and generate optimized cut lists.

#### How to Use

1. **Upload CSV File**
   - Click "Choose a CSV file"
   - Select your `*_ShipmentProductWithCostsAndPrice.csv` file
   - File name becomes the reference number

2. **Review Kickplate Items**
   - Table shows all kickplates found (items starting with "KP")
   - View: Part Code, Description, Quantity, Price
   - Metrics display:
     - Unique Items: Number of different kickplate types
     - Total Pieces: Total quantity to cut
     - Total Cost: Material cost
     - Total Revenue: Project value

3. **Generate Cut List**
   - Click "🚀 Generate Cut List"
   - App optimizes layout across multiple sheets
   - View results:
     - Number of sheets required
     - Total pieces
     - Average efficiency percentage

4. **Review Sheets**
   - Each sheet shown in expandable section
   - Interactive diagram shows piece placement
   - Grid lines every 100mm for reference
   - Color-coded pieces with labels
   - "↻" symbol indicates rotated pieces

5. **View Cutting Instructions**
   - Table lists each piece with:
     - Piece number
     - Part code
     - Description
     - X/Y position
     - Width/Height
     - Rotation status

6. **Download Outputs**
   - **CSV**: Spreadsheet with all cutting data
   - **PDF**: Professional cut list with diagrams

#### Tips
- Use actual stock dimensions for accurate planning
- Set kerf width if your saw blade is thick (usually 3-5mm)
- Higher efficiency = less waste
- PDF includes cutting checklist for workshop

#### Example Workflow
```
1. Receive order from sales
2. Export shipment CSV from Cin7
3. Upload to app → Tab 1
4. Review metrics (ensure quantities match order)
5. Click "Generate Cut List"
6. Download PDF
7. Print for workshop
8. Download CSV for records
```

---

### Tab 2: Manual Entry

#### Purpose
Add kickplates manually when you don't have a CSV file, or for small custom orders.

#### How to Use

1. **Add Items Using Form**
   - **Width (mm)**: Kickplate width
   - **Height (mm)**: Kickplate height
   - **Quantity**: How many pieces
   - **Material Code**: e.g., "SSS" for stainless steel
   - **Description**: Optional notes
   - Click "Add Item"

2. **Review Items List**
   - Table shows all added items
   - Part Code auto-generated (e.g., KP300300SSS)

3. **Generate Cut List**
   - Click "🚀 Generate Cut List"
   - Same optimization as CSV upload
   - Same outputs available

4. **Clear or Modify**
   - Click "Clear All" to start over
   - Add more items before generating

#### Tips
- Use consistent material codes (SSS, BRS, etc.)
- Add description for easy identification
- Build up your list before generating
- Save the CSV output for records

#### Example
```
Manual Order Entry:
- 5 x 800×300mm SSS kickplates
- 3 x 600×300mm SSS kickplates
- 2 x 900×300mm BRS kickplates

Result: 2 sheets, 85% efficiency
```

---

### Tab 3: Door Labels

#### Purpose
Generate door labels from PDF finishing schedules and create nesting layouts from door orders.

#### How to Use

**Step 1: Select Input Method**
- **Finishing Sheet (PDF)**: Hardware Direct door schedule PDFs
- **Order CSV**: Kickplate order CSVs
- **Door Schedule (Excel)**: Excel door schedules
- **Manual Entry**: Add doors individually

**Step 2: Upload & Parse**

*For Finishing Sheet PDF:*
1. Click "🔍 Auto-detect Project Info" (optional)
   - Extracts project code/name from PDF
   - Fills in sidebar Project Info automatically

2. Click "📥 Parse File & Generate Labels"
   - App reads PDF
   - Extracts door numbers, areas, kickplate sizes
   - **Note**: Only doors WITH kickplate dimensions are included
   - Doors without dimensions are automatically skipped

3. Review parsed labels
   - Sample of first 10 labels shown
   - Check Door, Area, Size, Material, Project

*For Other File Types:*
- Similar process
- Different parsing logic for each format

**Step 3: Edit Labels (Optional)**
- Use data editor to modify:
  - Door numbers
  - Area/location names
  - Sizes (if needed)
- Click "🔄 Refresh Display" to update

**Step 4: Preview Labels**
- See first 3 labels as they'll print
- Verify formatting
- Check project code inclusion

**Step 5: Generate Cut List (Optional)**
1. Click "🚀 Generate Cut List from These Labels"
   - Converts door labels to kickplate pieces
   - Groups identical sizes
   - Runs nesting optimization

2. View Summary
   - Click "📊 Show Kickplate Summary"
   - See unique sizes, quantities, total area

3. Review Cut List Results
   - Sheets required
   - Efficiency metrics
   - Visual layout of first sheet

**Step 6: Download Outputs**
- **📄 Door Labels CSV**: Spreadsheet of all doors
- **🏷️ Door Labels PDF**: Printable labels (3×8 grid)
- **📊 Door Summary CSV**: Summary report
- **🔪 Cut List CSV**: Cutting instructions (if generated)
- **📄 Cut List PDF**: Production diagrams (if generated)

#### Tips
- Always auto-detect project info for PDFs
- Review parsed data before downloading
- Edit any incorrect door numbers/areas
- Labels PDF ready for Avery-compatible labels
- Cut list links labels to production

#### Example Workflow
```
Project: Q30683B - Matamata Sports Facility

1. Receive finishing schedule PDF from site
2. Upload to Tab 3 → "Finishing Sheet (PDF)"
3. Click "Auto-detect Project Info"
   → Confirms: Q30683B - Matamata...
4. Click "Parse File & Generate Labels"
   → Found 45 door labels
5. Review sample (first 10 look good)
6. Download "Door Labels PDF"
7. Print on label sheets
8. Click "Generate Cut List"
   → 3 sheets, 87% efficiency
9. Download Cut List PDF
10. Print for workshop
```

---

### Tab 4: Debug Tools

#### Purpose
Technical troubleshooting and PDF analysis for support/developers.

#### How to Use
- **Upload PDF for debugging**: See raw text extraction
- **Run Deep Debug Analysis**: View first 3000 characters and line breakdown
- **Show Session State**: View app internal state
- Use only when requested by support

---

## Common Workflows

### Workflow 1: Standard Order Processing
```
1. Receive order confirmation
2. Export CSV from Cin7
3. Open app → Tab 1
4. Configure sidebar (stock size, kerf)
5. Upload CSV
6. Review metrics
7. Generate cut list
8. Download PDF
9. Print and send to workshop
10. Archive CSV for records
```

### Workflow 2: Door Installation Project
```
1. Receive finishing schedule PDF
2. Open app → Tab 3
3. Upload PDF
4. Auto-detect project info
5. Parse file
6. Review/edit labels
7. Download door labels PDF
8. Print labels
9. Generate cut list from labels
10. Download cut list PDF
11. Print for workshop
```

### Workflow 3: Custom One-Off Order
```
1. Customer calls with custom order
2. Open app → Tab 2
3. Add each kickplate manually
4. Review list
5. Generate cut list
6. Download PDF
7. Email PDF to customer for approval
8. Print for workshop when approved
```

---

## File Formats

### Supported Input Files

**CSV Files (Tab 1)**
- Format: Cin7/ProMaster shipment exports
- Required columns:
  - `PartCode`: Kickplate codes (e.g., KP800300SSS)
  - `Description`: Item description
  - `ProductQuantity`: Quantity
  - `ProductCost`: Unit cost
  - `ProductPrice`: Unit price
- File naming: `*_ShipmentProductWithCostsAndPrice.csv`

**PDF Files (Tab 3)**
- Format: Hardware Direct finishing schedules
- Must contain:
  - Project code (e.g., Q30683B)
  - Door numbers (e.g., D.26-K, W.15)
  - Kickplate codes (e.g., KP800300SSS)
  - Actual dimensions (W XXX H XXX)
- **Important**: Doors without dimensions (W H T) are skipped

**Excel Files (Tab 3)**
- Format: Door schedules (.xlsx, .xls)
- Expected columns (flexible):
  - Door number/reference
  - Area/location/room
  - Size/dimension or kickplate code
- App auto-detects column names

### Sample Data

**CSV Example:**
```csv
PartCode,Description,ProductQuantity,ProductCost,ProductPrice
KP800300SSS,Kickplate 800x300 SSS,5,45.00,75.00
KP600300SSS,Kickplate 600x300 SSS,3,35.00,60.00
```

**Kickplate Code Format:**
```
KP[WIDTH][HEIGHT][MATERIAL]

Examples:
KP800300SSS  = 800mm × 300mm Stainless Steel
KP600300BRS  = 600mm × 300mm Brass
KP0900300SSS = 900mm × 300mm Stainless Steel
```

---

## Output & Exports

### Cut List PDF
**Contents:**
- **Summary Page**:
  - Generation date/time
  - Stock dimensions
  - Grain direction
  - Total sheets
  - Sheet summary table

- **Sheet Pages** (one per sheet):
  - Visual cutting diagram
  - Grid overlay (100mm)
  - Color-coded pieces
  - Piece labels with codes
  - Cutting checklist with checkboxes
  - Reference number (if from CSV)

**Usage:**
- Print for workshop
- Pin to cutting station
- Check off pieces as cut
- File for quality records

### Cut List CSV
**Columns:**
- Sheet number
- Piece number
- Part code
- Description
- X position (mm)
- Y position (mm)
- Width (mm)
- Height (mm)
- Rotated (Yes/No)

**Usage:**
- Import to spreadsheet
- CNC machine programming
- Inventory tracking
- Quality records

### Door Labels PDF
**Format:**
- 3 columns × 8 rows per page
- Label size: 60×70mm (configurable)
- Each label contains:
  - DOOR: [number]
  - AREA: [location]
  - KICKPLATE: [width]×[height]mm
  - PROJECT: [code] (optional)

**Usage:**
- Print on Avery-compatible label sheets
- Apply to each kickplate
- Track during installation
- Match to door schedule

### Door Labels CSV
**Columns:**
- door_number
- area
- kickplate_code
- width
- height
- project_code
- project_name
- material
- quantity

**Usage:**
- Import to other systems
- Create custom reports
- Data backup
- Audit trail

---

## Tips & Best Practices

### Before You Start
1. **Check stock dimensions** in sidebar match your actual sheets
2. **Set kerf width** if your saw blade is thick (improves accuracy)
3. **Enter project info** for proper labeling and tracking
4. **Use latest browser** (Chrome, Edge, Firefox recommended)

### While Using
1. **Review metrics** before generating (catch errors early)
2. **Check efficiency** - 80%+ is good, 90%+ is excellent
3. **Verify rotations** make sense for your material grain
4. **Save CSV outputs** for your records
5. **Print PDFs at 100% scale** (no shrink-to-fit)

### After Generation
1. **Double-check quantities** against original order
2. **Verify dimensions** on diagrams
3. **File PDFs** by project code
4. **Keep CSVs** for warranty tracking
5. **Update inventory** systems

### Performance
- Large files (100+ pieces) may take 10-30 seconds
- Close other browser tabs for faster processing
- Refresh page if app becomes slow
- Download files promptly (session-based storage)

---

## Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Submit forms (Add Item, etc.)
- **Ctrl+F**: Search within tables (browser feature)
- **Ctrl+S**: Download current page (browser feature)

---

## FAQ

### 1. Why are some doors missing from my labels?
**Answer:** The app only includes doors that have actual kickplate dimensions. Doors with "W H" or "W H T" (no numbers) are automatically skipped because they don't have sizes to cut.

### 2. Can I change the stock size mid-project?
**Answer:** Yes, adjust in the sidebar. You'll need to click "Generate Cut List" again to re-optimize with the new size.

### 3. What's a good efficiency percentage?
**Answer:**
- 75-80%: Acceptable
- 80-90%: Good
- 90%+: Excellent
- Below 75%: Consider different stock size or manual layout

### 4. Can I rotate pieces if my material has grain?
**Answer:** Set "Grain Direction" to Horizontal or Vertical to prevent rotation. Use "No preference" only for materials without grain direction.

### 5. How do I handle different materials (SSS vs BRS)?
**Answer:** They're treated as separate pieces. The app doesn't mix materials on the same sheet.

### 6. Can I edit the cut list after generating?
**Answer:** No, but you can:
- Edit input data and regenerate
- Download CSV and modify in Excel
- Use Manual Entry to fine-tune

### 7. What if my CSV doesn't have kickplates?
**Answer:** The app filters for items starting with "KP". If none found, you'll see a warning. Check your CSV has kickplate items or use Manual Entry.

### 8. Can I save my work and return later?
**Answer:** No, the app doesn't save between sessions. Download your CSVs/PDFs before closing. You can re-upload CSVs later.

### 9. How accurate are the cutting positions?
**Answer:** Positions are exact to the millimeter based on your stock size and kerf settings. Always verify first sheet before cutting all.

### 10. Can I use this for materials other than kickplates?
**Answer:** Yes! Any rectangular pieces can be nested. Just enter dimensions in Manual Entry tab.

---

## Support & Updates

### Report Issues
- GitHub: [https://github.com/DJCELL1/kickplate-nesting/issues](https://github.com/DJCELL1/kickplate-nesting/issues)
- Email: [your-support-email]
- Include: Screenshot, file used, error message

### Request Features
- Same GitHub link
- Describe use case clearly
- Explain benefit

### Version Info
Check commit history on GitHub for latest updates and changes.

---

**Hardware Direct** | Professional Door Solutions
*This manual covers Kickplate Nesting Optimizer v1.0*
