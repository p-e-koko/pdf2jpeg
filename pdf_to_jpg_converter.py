#!/usr/bin/env python3
"""
Bulk PDF to JPG Converter - Extracts the first page of PDF files and saves them as JPG images.

Requirements:
    pip install pdf2image pillow

Additional system requirements:
    - Windows: No additional requirements
    - macOS: brew install poppler
    - Linux: sudo apt-get install poppler-utils
"""

import sys
import os
import glob
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Set up poppler path - handle both Windows and Docker/Linux environments
def get_poppler_path():
    # Check if running in Docker/Linux (poppler-utils installed system-wide)
    if os.path.exists('/usr/bin/pdftoppm'):
        return None  # Use system poppler
    # Windows - use bundled poppler
    return os.path.join(os.path.dirname(__file__), "poppler-23.01.0", "Library", "bin")

POPPLER_PATH = get_poppler_path()

def pdf_first_page_to_jpg(pdf_path, output_dir=None, dpi=200, quality=95, scale_factor=0.6):
    """
    Convert the first page of a PDF to JPG format.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_dir (str, optional): Directory for the output JPG file. 
                                   If None, uses same directory as PDF
        dpi (int): Resolution for the conversion (default: 200)
        quality (int): JPEG quality (1-100, default: 95)
        scale_factor (float): Scale factor for resizing (default: 0.6 = 60%)
    
    Returns:
        tuple: (success: bool, pdf_path: str, output_path: str or error_message: str)
    """
    try:
        pdf_path = Path(pdf_path)
        
        # Validate input file
        if not pdf_path.exists():
            return False, str(pdf_path), f"File not found: {pdf_path}"
        
        if pdf_path.suffix.lower() != '.pdf':
            return False, str(pdf_path), "Not a PDF file"
        
        # Set output directory
        if output_dir is None:
            output_dir = pdf_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create output filename
        output_path = output_dir / f"{pdf_path.stem}.jpg"
        
        # Convert first page only
        pages = convert_from_path(
            pdf_path, 
            dpi=dpi,
            first_page=1,
            last_page=1,
            fmt='RGB',
            poppler_path=POPPLER_PATH
        )
        
        if not pages:
            return False, str(pdf_path), "No pages found in PDF"
        
        # Save as JPG with resizing
        first_page = pages[0]
        
        # Scale down by the specified factor
        original_width, original_height = first_page.size
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        resized_image = first_page.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        resized_image.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return True, str(pdf_path), str(output_path)
        
    except Exception as e:
        return False, str(pdf_path), str(e)

def find_pdf_files(input_paths):
    """
    Find all PDF files from given input paths (files or directories).
    
    Args:
        input_paths (list): List of file paths or directory paths
    
    Returns:
        list: List of PDF file paths
    """
    pdf_files = []
    
    for input_path in input_paths:
        path = Path(input_path)
        
        if path.is_file() and path.suffix.lower() == '.pdf':
            pdf_files.append(str(path))
        elif path.is_dir():
            # Find all PDF files in directory (including subdirectories)
            pdf_files.extend([str(p) for p in path.rglob('*.pdf')])
            pdf_files.extend([str(p) for p in path.rglob('*.PDF')])
        elif '*' in str(path) or '?' in str(path):
            # Handle glob patterns
            pdf_files.extend(glob.glob(str(path)))
    
    return sorted(list(set(pdf_files)))  # Remove duplicates and sort

def process_pdfs_bulk(input_paths, output_dir=None, dpi=200, quality=95, max_workers=4, scale_factor=0.6):
    """
    Process multiple PDF files concurrently.
    
    Args:
        input_paths (list): List of PDF files, directories, or glob patterns
        output_dir (str, optional): Output directory for all JPG files
        dpi (int): Resolution for conversion
        quality (int): JPEG quality
        max_workers (int): Maximum number of concurrent workers
        scale_factor (float): Scale factor for resizing (default: 0.6 = 60%)
    
    Returns:
        dict: Summary of results
    """
    # Find all PDF files
    pdf_files = find_pdf_files(input_paths)
    
    if not pdf_files:
        print("No PDF files found!")
        return {"total": 0, "successful": 0, "failed": 0, "results": []}
    
    print(f"Found {len(pdf_files)} PDF files to process...")
    print(f"Using {max_workers} workers for parallel processing")
    if output_dir:
        print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    results = []
    successful = 0
    failed = 0
    start_time = time.time()
    
    # Process files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_pdf = {
            executor.submit(pdf_first_page_to_jpg, pdf_file, output_dir, dpi, quality, scale_factor): pdf_file
            for pdf_file in pdf_files
        }
        
        # Process completed tasks
        for i, future in enumerate(as_completed(future_to_pdf), 1):
            success, pdf_path, result_path_or_error = future.result()
            results.append((success, pdf_path, result_path_or_error))
            
            if success:
                successful += 1
                print(f"✓ [{i}/{len(pdf_files)}] {Path(pdf_path).name} -> {Path(result_path_or_error).name}")
            else:
                failed += 1
                print(f"✗ [{i}/{len(pdf_files)}] {Path(pdf_path).name} - Error: {result_path_or_error}")
    
    # Print summary
    elapsed_time = time.time() - start_time
    print("-" * 50)
    print(f"Processing completed in {elapsed_time:.2f} seconds")
    print(f"Total files: {len(pdf_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"Average time per file: {elapsed_time/len(pdf_files):.2f} seconds")
    
    return {
        "total": len(pdf_files),
        "successful": successful,
        "failed": failed,
        "results": results,
        "elapsed_time": elapsed_time
    }

def main():
    """Command line interface for the bulk PDF to JPG converter."""
    
    # Default paths - modify these as needed
    DEFAULT_PDF_INPUT = r"C:\Users\Pann\Downloads\idpdf"  # Default folder to look for PDFs
    DEFAULT_JPEG_OUTPUT = r"C:\Users\Pann\Downloads\JPEGs"  # Default folder for JPEG output
    
    if len(sys.argv) < 2:
        print("Bulk PDF to JPG Converter")
        print("=" * 30)
        print("Usage: python pdf_to_jpg.py <input> [output_dir] [dpi] [quality] [workers]")
        print("\nInput options:")
        print("  - Single file: document.pdf")
        print("  - Multiple files: file1.pdf file2.pdf file3.pdf")
        print("  - Directory: /path/to/pdfs/")
        print("  - Glob pattern: '*.pdf' or '/path/to/**/*.pdf'")
        print("\nExamples:")
        print("  python pdf_to_jpg.py document.pdf")
        print("  python pdf_to_jpg.py /path/to/pdfs/")
        print("  python pdf_to_jpg.py '*.pdf' output_folder 300 90 8")
        print("  python pdf_to_jpg.py file1.pdf file2.pdf file3.pdf")
        print(f"\nNo arguments provided. Using defaults:")
        print(f"  Input: {DEFAULT_PDF_INPUT}")
        print(f"  Output: {DEFAULT_JPEG_OUTPUT}")
        
        # Use default paths when no arguments provided
        if Path(DEFAULT_PDF_INPUT).exists():
            input_paths = [DEFAULT_PDF_INPUT]
            output_dir = DEFAULT_JPEG_OUTPUT
            dpi = 200
            quality = 95
            max_workers = 4
        else:
            print(f"Error: Default input path '{DEFAULT_PDF_INPUT}' does not exist!")
            return
    
    else:
        # Parse arguments
        input_paths = []
        output_dir = None
        dpi = 200
        quality = 95
        max_workers = 4
        
        # Collect input paths (all arguments until we hit a number or known directory)
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]
            
            # Check if this looks like a parameter (number) or output directory
            if arg.isdigit():
                # This is DPI
                dpi = int(arg)
                i += 1
                if i < len(sys.argv) and sys.argv[i].isdigit():
                    quality = int(sys.argv[i])
                    i += 1
                    if i < len(sys.argv) and sys.argv[i].isdigit():
                        max_workers = int(sys.argv[i])
                break
            elif (Path(arg).is_dir() or arg.endswith('/') or arg.endswith('\\')) and not Path(arg).suffix:
                # This is output directory
                output_dir = arg
                i += 1
            else:
                # This is an input path
                input_paths.append(arg)
                i += 1
    
    # Validate parameters
    if dpi < 72 or dpi > 600:
        print("Warning: DPI should typically be between 72 and 600")
    
    if quality < 1 or quality > 100:
        print("Error: Quality must be between 1 and 100")
        return
    
    if max_workers < 1 or max_workers > 16:
        print("Error: Workers should be between 1 and 16")
        return
    
    # Process files
    summary = process_pdfs_bulk(input_paths, output_dir, dpi, quality, max_workers, scale_factor=0.6)
    
    if summary["successful"] > 0:
        print(f"\n✓ Successfully processed {summary['successful']} files!")
    if summary["failed"] > 0:
        print(f"✗ Failed to process {summary['failed']} files!")
        sys.exit(1)

if __name__ == "__main__":
    main()