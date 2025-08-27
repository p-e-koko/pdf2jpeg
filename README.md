# PDF to JPEG Converter

A high-performance bulk PDF to JPEG converter that extracts the first page of PDF files and converts them to high-quality JPEG images with automatic resizing.

## Features

- 🚀 **Bulk Processing**: Convert multiple PDFs simultaneously using parallel processing
- 🖼️ **Smart Resizing**: Automatically scales images to 40% of original size for optimal file size
- 📁 **Flexible Input**: Supports single files, directories, or glob patterns
- ⚡ **Fast Performance**: Multi-threaded processing with configurable worker count
- 🔧 **Customizable**: Adjustable DPI, quality, and scaling factors
- 💻 **Windows Ready**: Includes bundled Poppler utilities (no additional installation needed)

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Windows 10/11 (tested)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd pdf2image
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install pdf2image pillow
   ```

4. **You're ready to go!** The script includes Poppler utilities, so no additional installation is needed.

### Basic Usage

#### Convert all PDFs in a folder (using defaults)
```bash
python pdf_to_jpg_converter.py
```
*Uses default input folder: `C:\Users\Pann\Downloads\idpdf`*
*Outputs to: `C:\Users\Pann\Downloads\JPEGs`*

#### Convert a specific PDF file
```bash
python pdf_to_jpg_converter.py document.pdf
```

#### Convert all PDFs in a specific folder
```bash
python pdf_to_jpg_converter.py "C:\path\to\your\pdfs\"
```

#### Convert with custom output folder
```bash
python pdf_to_jpg_converter.py "C:\input\folder\" "C:\output\folder\"
```

#### Advanced usage with custom settings
```bash
python pdf_to_jpg_converter.py "*.pdf" output_folder 300 90 8
```
- `300` = DPI (resolution)
- `90` = JPEG quality (1-100)
- `8` = Number of parallel workers

## Configuration

### Default Paths

To change the default input and output folders, edit these lines in `pdf_to_jpg_converter.py`:

```python
DEFAULT_PDF_INPUT = r"C:\Users\Pann\Downloads\idpdf"      # Change this path
DEFAULT_JPEG_OUTPUT = r"C:\Users\Pann\Downloads\JPEGs"   # Change this path
```

### Image Settings

The script is currently configured to:
- **Scale images to 40%** of original size
- **DPI: 200** (good balance of quality and file size)
- **JPEG Quality: 95** (high quality)
- **Resampling: LANCZOS** (high-quality scaling algorithm)

To change the scaling factor, edit this line:
```python
def pdf_first_page_to_jpg(pdf_path, output_dir=None, dpi=200, quality=95, scale_factor=0.4):
```
Change `scale_factor=0.4` to:
- `0.3` for 30% size
- `0.5` for 50% size
- `0.8` for 80% size
- `1.0` for original size

## File Structure

```
pdf2image/
├── pdf_to_jpg_converter.py    # Main script
├── poppler-23.01.0/           # Bundled Poppler utilities
├── .venv/                     # Virtual environment (after setup)
├── README.md                  # This file
└── requirements.txt           # Python dependencies (optional)
```

## Input Options

The script accepts various input formats:

### Single File
```bash
python pdf_to_jpg_converter.py document.pdf
```

### Multiple Files
```bash
python pdf_to_jpg_converter.py file1.pdf file2.pdf file3.pdf
```

### Directory (processes all PDFs including subdirectories)
```bash
python pdf_to_jpg_converter.py "C:\path\to\pdfs\"
```

### Glob Patterns
```bash
python pdf_to_jpg_converter.py "*.pdf"
python pdf_to_jpg_converter.py "C:\documents\**\*.pdf"
```

## Examples

### Example 1: Convert all PDFs in Downloads folder
```bash
python pdf_to_jpg_converter.py "C:\Users\YourName\Downloads\"
```

### Example 2: High-quality conversion
```bash
python pdf_to_jpg_converter.py input.pdf output_folder 300 100
```

### Example 3: Fast batch processing
```bash
python pdf_to_jpg_converter.py "*.pdf" output_folder 150 85 16
```

### Example 4: Convert specific files to custom location
```bash
python pdf_to_jpg_converter.py report1.pdf report2.pdf "C:\converted_images\"
```

## Performance Tips

- **More workers**: Increase the worker count for faster processing on multi-core systems
- **Lower DPI**: Use 150 DPI for faster processing if high resolution isn't needed
- **SSD storage**: Use SSD drives for input/output for better performance
- **Batch size**: Process 50-100 files at a time for optimal memory usage

## Troubleshooting

### Common Issues

**"No PDF files found"**
- Check that the input path exists
- Ensure PDF files have `.pdf` extension
- Use absolute paths if relative paths don't work

**"Unable to get page count"**
- The bundled Poppler should work automatically
- If issues persist, try running as administrator

**Memory issues with large PDFs**
- Reduce the number of parallel workers
- Process files in smaller batches
- Lower the DPI setting

**Permission errors**
- Ensure you have write permissions to the output directory
- Try running as administrator if needed

### Getting Help

If you encounter issues:
1. Check that all file paths exist and are accessible
2. Verify that input files are valid PDF documents
3. Ensure sufficient disk space for output files
4. Try processing a single file first to isolate issues

## Technical Details

- **Language**: Python 3.7+
- **Key Libraries**: pdf2image, Pillow (PIL)
- **PDF Processing**: Poppler (bundled)
- **Image Format**: JPEG with optimization
- **Concurrency**: ThreadPoolExecutor for parallel processing
- **Resampling**: LANCZOS algorithm for high-quality scaling

## Output Information

The script provides detailed progress information:
- ✓ Successful conversions with file names
- ✗ Failed conversions with error messages
- Processing time and performance statistics
- File count summaries

## License

This script is provided as-is for educational and personal use.

---

**Happy Converting!** 🎯

For questions or improvements, feel free to modify the script to suit your specific needs.
