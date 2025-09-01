# PDF to JPEG Converter

A high-performance bulk PDF to JPEG converter that extracts the first page of PDF files and converts them to high-quality JPEG images with automatic resizing. Now with Docker support and web interface!

## Features

- 🚀 **Bulk Processing**: Convert multiple PDFs simultaneously using parallel processing
- 🖼️ **Smart Resizing**: Automatically scales images to 40% of original size for optimal file size
- 📁 **Flexible Input**: Supports single files, directories, or glob patterns via command line
- 🌐 **Web Interface**: Easy-to-use browser-based upload and conversion
- ⚡ **Fast Performance**: Multi-threaded processing with configurable worker count
- 🔧 **Customizable**: Adjustable DPI, quality, and scaling factors
- � **Docker Ready**: Containerized deployment with zero dependency management
- 💻 **Cross-Platform**: Works on Windows, Mac, and Linux with Docker

## Quick Start (Docker - Recommended)

### Prerequisites

- Git
- Docker Desktop

### Installation & Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/p-e-koko/pdf2jpeg.git
   cd pdf2jpeg
   ```

2. **Start with Docker**
   ```bash
   docker-compose up --build
   ```

3. **Access the web interface**
   - Open your browser to: `http://localhost:5000`
   - Upload PDFs and download converted JPEGs

That's it! No Python installation, no dependencies, no configuration needed.

## Alternative: Command Line Usage (Docker)

You can also use the command line interface within the Docker container:

```bash
# Access the container
docker-compose exec pdf-converter bash

# Run the command line converter
python pdf_to_jpg_converter.py
```

## Alternative: Native Python Installation

If you prefer to run without Docker:

### Prerequisites
- Python 3.7 or higher
- Windows 10/11 (tested)

### Installation
1. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

2. **Install dependencies**
   ```bash
   pip install pdf2image pillow flask werkzeug
   ```

3. **Run the web app**
   ```bash
   python web_app.py
   ```
   Access at: `http://localhost:5000`

### Command Line Usage (Native Python)

#### Convert all PDFs in a folder (using defaults)
```bash
python pdf_to_jpg_converter.py
```
*Uses default input folder: `./uploads`*
*Outputs to: `./outputs`*

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

## Docker Commands

### Basic Operations
```bash
# Start the application
docker-compose up --build

# Run in background
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs

# Access container shell
docker-compose exec pdf-converter bash
```

### Deployment Options
- **Development**: `docker-compose up` for local development
- **Production**: Deploy to any cloud platform supporting Docker
- **Scaling**: Modify `docker-compose.yml` to add more instances

## Configuration

### Web Interface
The web interface allows easy drag-and-drop PDF upload and automatic conversion. Converted images are available for download immediately.

### Command Line Configuration

To change the default input and output folders, edit these lines in `pdf_to_jpg_converter.py`:

```python
DEFAULT_PDF_INPUT = r"./uploads"      # Change this path
DEFAULT_JPEG_OUTPUT = r"./outputs"   # Change this path
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
pdf2jpeg/
├── web_app.py                 # Flask web application
├── pdf_to_jpg_converter.py    # Command line script
├── templates/                 # Web interface templates
│   └── index.html
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── requirements.txt           # Python dependencies
├── uploads/                   # Input PDFs (web interface)
├── outputs/                   # Generated JPEGs
├── poppler-23.01.0/           # Bundled Poppler utilities (Windows)
└── README.md                  # This file
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

## Docker Commands

### Basic Operations
```bash
# Start the application
docker-compose up --build

# Run in background
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs

# Access container shell
docker-compose exec pdf-converter bash
```

### Deployment Options
- **Development**: `docker-compose up` for local development
- **Production**: Deploy to any cloud platform supporting Docker
- **Scaling**: Modify `docker-compose.yml` to add more instances

## Usage Examples

### Web Interface (Recommended)
1. Start Docker: `docker-compose up --build`
2. Open browser: `http://localhost:5000`
3. Upload PDF files using drag & drop
4. Download converted JPEGs automatically

### Command Line Examples (within Docker container)

#### Example 1: Convert all PDFs in uploads folder
```bash
docker-compose exec pdf-converter python pdf_to_jpg_converter.py
```

#### Example 2: High-quality conversion
```bash
docker-compose exec pdf-converter python pdf_to_jpg_converter.py input.pdf outputs 300 100
```

#### Example 3: Fast batch processing
```bash
docker-compose exec pdf-converter python pdf_to_jpg_converter.py "*.pdf" outputs 150 85 16
```

### Example 4: Convert specific files to custom location
```bash
docker-compose exec pdf-converter python pdf_to_jpg_converter.py report1.pdf report2.pdf outputs
```

## Technical Details

- **Language**: Python 3.12+
- **Key Libraries**: pdf2image, Pillow (PIL), Flask
- **PDF Processing**: Poppler (included in Docker)
- **Image Format**: JPEG with optimization
- **Concurrency**: ThreadPoolExecutor for parallel processing
- **Resampling**: LANCZOS algorithm for high-quality scaling
- **Deployment**: Docker containerized with web interface

## Troubleshooting

### Docker Issues

**Container won't start**
- Ensure Docker Desktop is running
- Check port 5000 is not in use: `docker ps`
- Restart Docker Desktop if needed

**Can't access web interface**
- Verify container is running: `docker-compose ps`
- Check browser URL: `http://localhost:5000`
- Try `http://127.0.0.1:5000` if localhost doesn't work

**File upload/conversion issues**
- Check file is a valid PDF
- Ensure sufficient disk space
- Check Docker container logs: `docker-compose logs`

### Getting Help

If you encounter issues:
1. Check Docker container status: `docker-compose ps`
2. View logs: `docker-compose logs`
3. Restart the application: `docker-compose restart`
4. Try with a simple test PDF first

## Performance Tips

- **Docker resources**: Allocate more CPU/RAM to Docker in settings
- **Concurrent uploads**: Web interface handles multiple files
- **Batch processing**: Use command line for very large batches
- **Storage**: Mount external volumes for large file processing

## Output Information

The application provides detailed feedback:
- **Web Interface**: Real-time upload progress and download links
- **Command Line**: Detailed conversion status and statistics
- ✓ Successful conversions with file names
- ✗ Failed conversions with error messages
- Processing time and performance statistics

## License

This project is provided as-is for educational and personal use.

---

**Happy Converting!** 🎯🐳

For questions or improvements, feel free to open an issue or submit a pull request.
