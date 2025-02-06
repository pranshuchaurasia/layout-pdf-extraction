# PDF Parser Service

A FastAPI-based service that leverages Marker for converting PDFs to markdown, JSON, and HTML formats.

## About Marker

Marker is a powerful tool that converts PDFs and images to markdown, JSON, and HTML quickly and accurately. It offers:

- Support for documents in all languages
- Formatting for tables, forms, equations, links, references, and code blocks
- Image extraction and saving alongside markdown
- Header/footer/artifact removal
- Easy extensibility with custom formatting and logic
- Optional LLM integration for improved accuracy
- Support for GPU, CPU, or MPS processing

### How Marker Works

Marker employs a pipeline of deep learning models:
1. Text extraction with OCR when necessary (using heuristics and surya)
2. Page layout detection and reading order determination (surya)
3. Block cleaning and formatting (heuristics, texify, surya)
4. Optional LLM integration for quality improvement
5. Block combination and text post-processing

The system optimizes performance by utilizing models only where necessary.

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Configure the environment variables:
```bash
SOURCE_PDF_PATH=<path_to_source_pdfs>
DESTINATION_PDF_PATH=<path_to_destination>
```

## API Endpoints

### PDF Processing

#### Parse Specific PDF
```http
POST /pdf_parser/parse_specific_pdf/
```
Parameters:
- `pdf_name`: Name of the PDF file to process
- `page_number` (optional): Specific page to process

Returns:
```json
{
    "message": "Specific PDF parsing started.",
    "pdf_name": "<pdf_name>",
    "page_number": "<page_number>",
    "batch_id": "<batch_id>"
}
```

#### Parse All PDFs
```http
POST /pdf_parser/parse_all_pdfs
```
Returns:
```json
{
    "message": "PDF parsing started.",
    "batch_id": "<batch_id>"
}
```

### File Management

#### List All PDF Files
```http
GET /pdf_parser/all_esg_pdf_files
```
Returns a list of all PDF files in the source directory.

#### Display Results
```http
GET /pdf_parser/display_result/{pdf_name}
```
Parameters:
- `pdf_name`: Name of the PDF file
- `format` (optional): Output format ("markdown" or "html", defaults to "markdown")

Returns:
- For markdown: JSON containing markdown content and image paths
- For HTML: HTML file response

### Status Checking

#### Check Processing Status
```http
GET /pdf_parser/status/{batch_id}
```
Returns the current status of the processing batch.

## Configuration

The service requires the following environment variables:

- `SOURCE_PDF_PATH`: Directory containing source PDF files
- `DESTINATION_PDF_PATH`: Directory for processed output files

