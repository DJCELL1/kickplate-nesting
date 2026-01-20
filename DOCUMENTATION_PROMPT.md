# App Documentation Prompt Template

Use this prompt to generate consistent, professional documentation for Hardware Direct Streamlit applications.

---

## Prompt to Use:

```
Create comprehensive user documentation for this Streamlit application with the following structure:

## 1. USER MANUAL

### Overview
- What the application does
- Who it's for
- Key benefits

### Getting Started
- How to access the app
- First-time setup
- Basic navigation

### Features Guide
For each major feature/tab:
- **Purpose**: What it does
- **How to Use**: Step-by-step instructions
- **Tips**: Best practices
- **Example**: Real-world use case

### Workflows
- Common task workflows
- Step-by-step procedures
- Screenshots/descriptions where helpful

### File Formats
- Supported file types
- Expected file structure
- Sample data examples

### Output & Exports
- What files are generated
- How to download/use them
- Format specifications

---

## 2. TROUBLESHOOTING GUIDE

### Common Issues & Solutions
For each issue:
- **Problem**: Clear description
- **Cause**: Why it happens
- **Solution**: Step-by-step fix
- **Prevention**: How to avoid it

### Categories:
1. **File Upload Issues**
2. **Processing Errors**
3. **Display/UI Problems**
4. **Export/Download Issues**
5. **Data Validation Errors**

### Error Messages
- List common error messages
- Explain what they mean
- Provide solutions

### Performance Tips
- How to handle large files
- Browser recommendations
- System requirements

### Getting Help
- Where to report bugs
- How to request features
- Support contact info

---

## 3. QUICK REFERENCE

### Cheat Sheet
- Keyboard shortcuts (if any)
- Quick tips
- Common patterns

### FAQ
- Top 10 frequently asked questions
- Clear, concise answers

---

## Format Requirements:
- Use clear headings (##, ###)
- Include examples
- Use bullet points and numbered lists
- Write in simple, professional language
- Include specific field names and button labels
- Add warnings/notes where needed
- Hardware Direct branding throughout
```

---

## Usage Instructions:

1. Copy the prompt above
2. Run it with context about your specific app
3. Provide:
   - App name and purpose
   - List of features/tabs
   - Sample workflows
   - Known issues/limitations
4. Review and customize the generated documentation
5. Save as `USER_MANUAL.md` and `TROUBLESHOOTING.md` in your project

---

## Example Context to Provide:

```
App Name: [Your App Name]
Purpose: [Brief description]
Main Features:
- Feature 1: [Description]
- Feature 2: [Description]
- Feature 3: [Description]

File Types Supported: [List]
Export Formats: [List]
Special Requirements: [Any dependencies, data sources, etc.]
```

---

## Customization Tips:

- Adjust section depth based on app complexity
- Add app-specific sections (e.g., "API Integration" for connected apps)
- Include screenshots for complex workflows
- Update regularly as features change
- Keep language consistent with Hardware Direct brand voice
