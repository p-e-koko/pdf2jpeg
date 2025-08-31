# PDF to JPG Converter - Docker Deployment Guide

This guide covers deploying the PDF to JPG converter using Docker, which is the simplest and most portable deployment method.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Clone/Download the project files**
2. **Navigate to the project directory:**
   ```bash
   cd pdf2image
   ```

3. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`
   - The application will be running with persistent file storage

5. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the Docker image:**
   ```bash
   docker build -t pdf-converter .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/outputs:/app/outputs pdf-converter
   ```

3. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for production deployment

### File Storage
- Uploads are stored in `./uploads` directory
- Converted files are stored in `./outputs` directory
- Both directories are mounted as volumes for persistence

## Deployment to Cloud Platforms

### Deploy to any VPS/Server with Docker

1. **Copy files to your server**
2. **Install Docker on the server**
3. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

### Deploy to Cloud Platforms

#### DigitalOcean App Platform
1. Connect your GitHub repository
2. Choose Docker as the build method
3. Set port to 5000
4. Deploy

#### Railway
1. Connect your GitHub repository
2. Railway will auto-detect the Dockerfile
3. Deploy with one click

#### Render
1. Connect your GitHub repository
2. Choose Docker as the environment
3. Set port to 5000
4. Deploy

## Security Notes

- The application runs on port 5000 by default
- For production, consider using a reverse proxy (nginx) for SSL termination
- Ensure proper firewall rules are in place
- Consider adding authentication for production use

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port mapping in `docker-compose.yml`: `"8080:5000"`

2. **Permission issues with volumes:**
   - Ensure the upload/output directories have proper permissions

3. **PDF conversion fails:**
   - Check if poppler-utils is properly installed in the container
   - Verify the PDF files are not corrupted

### Logs

To view application logs:
```bash
docker-compose logs -f pdf-converter
```

## File Structure

```
pdf2image/
├── Dockerfile                 # Docker container configuration
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt           # Python dependencies
├── web_app.py                # Flask web application
├── pdf_to_jpg_converter.py   # Core conversion logic
├── templates/
│   └── index.html            # Web interface
├── uploads/                  # Uploaded PDF files (created automatically)
└── outputs/                  # Converted JPG files (created automatically)
```

## Performance

- The application uses multithreading for concurrent PDF processing
- Default settings: 200 DPI, 95% quality, 0.6 scale factor
- Memory usage depends on PDF size and concurrent conversions

That's it! Docker makes deployment simple and consistent across different environments.
