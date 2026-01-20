# Kickplate Nesting Optimizer - Troubleshooting Guide

**Hardware Direct**
*Quick solutions to common issues*

---

## Quick Diagnosis

**Is your problem...**
- [File won't upload?](#file-upload-issues) → Check format and size
- [App shows error?](#processing-errors) → See error messages section
- [Can't see results?](#displayui-problems) → Try refresh or different browser
- [Download not working?](#exportdownload-issues) → Check pop-up blocker
- [Wrong data parsed?](#data-validation-errors) → Verify file format
- [App running slow?](#performance-issues) → Close other tabs, reduce file size

---

## File Upload Issues

### Problem: "No kickplate items found"
**Cause:** CSV doesn't contain items with "KP" prefix
**Solution:**
1. Open CSV in Excel/Notepad
2. Check `PartCode` column
3. Verify kickplate codes start with "KP"
4. If codes are different, use Manual Entry instead

**Prevention:** Use standard Cin7 export format

---

### Problem: CSV won't upload
**Cause:** File format incorrect or corrupted
**Solution:**
1. Ensure file extension is `.csv` (not `.xlsx`)
2. Open in Notepad - should see comma-separated values
3. Re-export from Cin7 if corrupted
4. Try different browser

**Prevention:** Don't edit CSV in Excel (can corrupt formatting)

---

### Problem: PDF won't upload
**Cause:** File size too large or format unsupported
**Solution:**
1. Check file size (max ~50MB recommended)
2. Ensure it's actual PDF (not image renamed as PDF)
3. Try "Save As" → PDF in Adobe Reader
4. Split large PDFs into smaller files

**Prevention:** Export directly as PDF from source system

---

### Problem: "Project info not found" when parsing PDF
**Cause:** PDF doesn't have standard Hardware Direct format
**Solution:**
1. Manually enter Project Code and Name in sidebar
2. Then click "Parse File & Generate Labels"
3. Or use Manual Entry tab

**Prevention:** Use standard Hardware Direct finishing schedule templates

---

## Processing Errors

### Problem: "No dimensions found" - many doors skipped
**Cause:** PDF has "W H" or "W H T" instead of actual measurements
**Solution:**
1. This is expected - incomplete doors are automatically skipped
2. Check PDF for doors with actual dimensions: "W 800 H 300"
3. Only doors with numbers will be processed
4. Manually add missing doors if needed

**Prevention:** Ensure finishing schedule is complete before PDF generation

---

### Problem: App freezes during "Optimizing layout"
**Cause:** Very large number of pieces (100+) or browser memory issue
**Solution:**
1. Wait up to 60 seconds (normal for large jobs)
2. If still frozen after 2 minutes:
   - Refresh page (F5)
   - Try smaller batch
   - Close other browser tabs
3. Split large orders into multiple sessions

**Prevention:**
- Process in batches of 50-75 pieces
- Close unused browser tabs
- Use modern browser (Chrome, Edge)

---

### Problem: "Invalid kickplate code format"
**Cause:** Code doesn't match expected pattern (KPXXXYYY...)
**Solution:**
1. Code must be: KP + width + height + material
2. Examples:
   - ✅ KP800300SSS (800×300 SSS)
   - ✅ KP0900300BRS (900×300 BRS)
   - ❌ KP80030SSS (missing digit)
   - ❌ K800300SSS (missing P)
3. Fix code in source data or use Manual Entry

**Prevention:** Use standard kickplate code format

---

### Problem: Efficiency very low (<60%)
**Cause:** Piece sizes don't fit well on stock size
**Solution:**
1. Check stock dimensions in sidebar are correct
2. Try different stock size if available
3. Consider grain direction setting
4. Some orders naturally have lower efficiency (very varied sizes)

**Prevention:**
- Use standard stock sizes (2400×1200 common)
- Group similar-sized orders together

---

## Display/UI Problems

### Problem: Diagrams not showing
**Cause:** Browser compatibility or slow internet
**Solution:**
1. Wait 5-10 seconds for diagrams to render
2. Try different browser (Chrome recommended)
3. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
4. Check internet connection

**Prevention:** Use modern, updated browser

---

### Problem: Tables cut off or misaligned
**Cause:** Browser zoom or screen size
**Solution:**
1. Reset zoom: Ctrl+0 (Windows) or Cmd+0 (Mac)
2. Use "wide" layout (already default)
3. Maximize browser window
4. Use landscape orientation on tablets

**Prevention:** Use desktop computer for best experience

---

### Problem: Sidebar hidden or missing
**Cause:** Narrow screen or sidebar collapsed
**Solution:**
1. Look for ">" arrow in top-left
2. Click to expand sidebar
3. Widen browser window
4. Refresh page

**Prevention:** Use screen width >1024px

---

### Problem: Colors look wrong
**Cause:** Theme not loaded or browser issue
**Solution:**
1. Hard refresh: Ctrl+Shift+R
2. Clear browser cache
3. Check if Hardware Direct orange (#F47920) shows on buttons
4. Update browser

**Prevention:** Keep browser updated

---

## Export/Download Issues

### Problem: PDF won't download
**Cause:** Pop-up blocker or browser settings
**Solution:**
1. Look for blocked pop-up icon in address bar
2. Click "Always allow" for this site
3. Try download button again
4. Right-click button → "Save link as..."

**Prevention:** Allow downloads for the app URL

---

### Problem: PDF opens in browser instead of downloading
**Cause:** Browser default behavior
**Solution:**
1. Right-click download button → "Save link as..."
2. Or: After opening, Ctrl+S to save
3. Change browser settings to always download PDFs

**Prevention:** Not a problem - both behaviors work fine

---

### Problem: Downloaded CSV opens wrong in Excel
**Cause:** Excel encoding or delimiter issues
**Solution:**
1. Don't double-click CSV
2. Open Excel first
3. File → Open → Select CSV
4. Use "Text Import Wizard" if prompted
5. Select "Comma" as delimiter

**Prevention:** Import CSV properly using Excel's import wizard

---

### Problem: Label PDF prints at wrong size
**Cause:** Printer scaling settings
**Solution:**
1. Open Print dialog
2. Find "Scale" or "Fit to page" setting
3. Set to "100%" or "Actual size"
4. Disable "Shrink to fit"
5. Print test page first

**Prevention:** Always check "Actual size" before printing labels

---

### Problem: Can't find downloaded files
**Cause:** Browser default download location
**Solution:**
1. Check Downloads folder
2. Look in browser downloads (Ctrl+J in Chrome)
3. Check browser settings → Downloads → Location
4. Files named: `[project]_cut_list.pdf`, etc.

**Prevention:** Set known download location in browser settings

---

## Data Validation Errors

### Problem: Wrong quantities in cut list
**Cause:** Data entry error or file corruption
**Solution:**
1. Check source CSV/PDF has correct quantities
2. Verify metrics match order:
   - Unique Items
   - Total Pieces
3. Re-upload file if needed
4. Use Manual Entry to verify

**Prevention:** Always review metrics before generating

---

### Problem: Pieces have wrong dimensions
**Cause:** Kickplate code parsing error
**Solution:**
1. Check kickplate code format
2. Verify width/height in code match actual dimensions
3. Example: KP800300SSS = 800mm wide, 300mm high
4. If wrong, fix source data and re-upload

**Prevention:** Use standard code format (KPWWWWHHHMM)

---

### Problem: Material codes mixed up
**Cause:** Inconsistent material naming
**Solution:**
1. Standardize codes:
   - SSS = Stainless Steel
   - BRS = Brass
   - (your standards)
2. Edit in source file
3. Re-upload

**Prevention:** Create material code standard document

---

### Problem: Door labels have wrong project name
**Cause:** Project info not set or incorrect in PDF
**Solution:**
1. Check sidebar "Project Info"
2. Click "Auto-detect Project Info" for PDFs
3. Or manually enter correct info
4. Re-parse file
5. Labels will update

**Prevention:** Always auto-detect or manually verify project info

---

### Problem: Some doors missing kickplate dimensions
**Cause:** Incomplete data in source
**Solution:**
1. This is normal - doors without sizes are skipped
2. Check source PDF/schedule for missing data
3. Add manually using Manual Entry tab if needed
4. Or request updated schedule from site

**Prevention:** Ensure finishing schedule is complete before exporting

---

## Performance Issues

### Problem: App loads slowly
**Cause:** Network or server issue
**Solution:**
1. Check internet connection
2. Try refresh (F5)
3. Wait 10-15 seconds
4. Try different time (server might be busy)

**Prevention:** Use during business hours, stable connection

---

### Problem: Large files time out
**Cause:** Too many pieces to process at once
**Solution:**
1. Split order into batches:
   - 50-75 pieces per batch recommended
   - Process separately
   - Combine PDFs later if needed
2. Close other browser tabs
3. Increase timeout patience (up to 60 seconds normal)

**Prevention:** Batch large orders (100+ pieces)

---

### Problem: Browser crashes
**Cause:** Memory overflow or browser issue
**Solution:**
1. Close all other tabs
2. Restart browser
3. Try different browser (Chrome recommended)
4. Process smaller batches
5. Update browser to latest version

**Prevention:**
- Use Chrome or Edge
- Close unused applications
- Process in batches

---

### Problem: "Out of memory" error
**Cause:** Browser memory limit reached
**Solution:**
1. Refresh page
2. Restart browser
3. Reduce file size:
   - Split into smaller batches
   - Remove unnecessary data from CSV
4. Use desktop computer (more RAM)

**Prevention:**
- Desktop > Laptop > Tablet
- 8GB+ RAM recommended
- Close other applications

---

## Error Messages Explained

### "DESCRIPTION NOT FOUND"
**Meaning:** Kickplate code not in hinge database
**Impact:** Descriptive text missing, but nesting still works
**Solution:** Ignore if just testing, or check code spelling

---

### "W H T" or "W H" in PDF
**Meaning:** Door has no kickplate dimensions
**Impact:** This door will be skipped
**Solution:** Normal behavior - only sized doors processed

---

### "Invalid file type"
**Meaning:** File extension not supported
**Impact:** Can't upload this file
**Solution:** Use CSV, PDF, or XLSX only

---

### "Could not parse project info"
**Meaning:** Auto-detection failed
**Impact:** Manual entry needed
**Solution:** Enter project code/name in sidebar manually

---

### "No hinge sheet found"
**Meaning:** Missing reference data file
**Impact:** App won't start
**Solution:** Contact IT - missing `hinge_data.xlsx` in `/data` folder

---

## Getting Help

### Before Contacting Support

✅ **Collect this information:**
1. Screenshot of error (if any)
2. File you were trying to upload (or sample)
3. Browser and version (e.g., Chrome 120)
4. Operating system (Windows/Mac)
5. Steps to reproduce issue

### Where to Get Help

**GitHub Issues (Recommended)**
- URL: https://github.com/DJCELL1/kickplate-nesting/issues
- Click "New Issue"
- Describe problem clearly
- Attach files/screenshots
- Response within 1-2 business days

**Email Support**
- Email: [your-support-email]
- Include all information above
- Attach files if under 10MB

**Internal Support**
- Contact: [IT Contact]
- Extension: [Number]
- Best for urgent production issues

### What to Include

**Good Report:**
```
Problem: PDF won't upload, shows "Invalid file type"
File: finishing_schedule_Q30683B.pdf (attached)
Browser: Chrome 120 on Windows 11
Steps: Tab 3 → Upload PDF → Select file → Error appears
Screenshot: [attached]
```

**Poor Report:**
```
App doesn't work, please fix
```

---

## System Requirements

### Minimum
- **Browser:** Chrome 100+, Firefox 100+, Edge 100+
- **RAM:** 4GB
- **Internet:** 1Mbps+
- **Screen:** 1024×768+

### Recommended
- **Browser:** Latest Chrome or Edge
- **RAM:** 8GB+
- **Internet:** 5Mbps+
- **Screen:** 1920×1080+
- **Device:** Desktop or laptop (not mobile)

### Not Supported
- Internet Explorer
- Mobile browsers (display issues)
- Very old browsers (pre-2020)

---

## Tips for Smooth Operation

### Daily Use
1. ✅ Use latest Chrome or Edge
2. ✅ Close unused tabs before starting
3. ✅ Check file formats before uploading
4. ✅ Review metrics before generating
5. ✅ Download files immediately

### Monthly Maintenance
1. ✅ Clear browser cache
2. ✅ Update browser
3. ✅ Check Downloads folder (delete old files)
4. ✅ Review saved CSVs

### Best Practices
- 📁 Organize files by project code
- 📅 Date-stamp manual entries
- 💾 Save CSV outputs for records
- 🖨️ Print test page before full run
- 📋 Keep project info updated in sidebar

---

## Still Having Issues?

### Check These First
1. Is your internet working?
2. Are you using a supported browser?
3. Did you try refreshing the page?
4. Did you check the FAQ in the User Manual?
5. Did you review this entire troubleshooting guide?

### Emergency Workarounds

**If app is completely down:**
- Use Manual Entry tab (requires less processing)
- Export data and process offline
- Contact support for alternative solutions

**If specific tab broken:**
- Try different tab for similar function
- Manual Entry can replace CSV upload
- Export CSV and process elsewhere

**If downloads broken:**
- Take screenshots of diagrams
- Copy table data to Excel
- Use browser "Print to PDF" feature

---

**Hardware Direct** | Professional Door Solutions
*Troubleshooting Guide for Kickplate Nesting Optimizer v1.0*
Last Updated: 2026-01-21
