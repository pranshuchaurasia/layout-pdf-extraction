import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pdfparser.marker.marker_pdf import MarkerPDFParser
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import uuid
import markdown

app = FastAPI()
parser = MarkerPDFParser()

@app.post("/pdf_parser/parse_specific_pdf/")
async def parse_specific_pdf(background_tasks: BackgroundTasks, pdf_name: str, page_number: int = None):
    try:
        
        batch_id = str(uuid.uuid4())
        background_tasks.add_task(parser.parse_specific_pdf, pdf_name, page_number, batch_id)
        return {"message": "Specific PDF parsing started.", "pdf_name": pdf_name, "page_number": page_number, "batch_id": batch_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pdf_parser/parse_all_pdfs")
async def parse_pdfs(background_tasks: BackgroundTasks):
    try:
        batch_id = str(uuid.uuid4())
        background_tasks.add_task(parser.parse_all_pdfs, batch_id)
        return {"message": "PDF parsing started.", "batch_id": batch_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pdf_parser/all_esg_pdf_files")
async def all_esg_pdf_files():
    status = parser.all_source_files()
    return JSONResponse(content=status)

@app.get("/pdf_parser/display_result/{pdf_name}")
async def display_result(pdf_name: str, format: str = "markdown"):
    try:
        results = parser.view_parsed_pdf(pdf_name, format)
        if format == "markdown":
            markdown_content, image_paths = results
            return {"markdown": markdown_content, "images": image_paths}
        elif format == "html":
            return FileResponse(results, media_type='text/html')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pdf_parser/status/{batch_id}")
async def status(batch_id: str):
    status = parser.get_status(batch_id)
    if status == "Batch ID not found":
        raise HTTPException(status_code=404, detail="Batch ID not found")
    return JSONResponse(content=status)