import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pdfparser.marker.marker_pdf import MarkerPDFParser
from fastapi.responses import JSONResponse
import uuid

app = FastAPI()
parser = MarkerPDFParser()

@app.post("/pdf_parser/parse_all_pdfs")
async def parse_pdfs(background_tasks: BackgroundTasks):
    try:
        batch_id = str(uuid.uuid4())
        background_tasks.add_task(parser.parse_all_pdfs, batch_id)
        return {"message": "PDF parsing started.", "batch_id": batch_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pdf_parser/status/{batch_id}")
async def status(batch_id: str):
    status = parser.get_status(batch_id)
    if status == "Batch ID not found":
        raise HTTPException(status_code=404, detail="Batch ID not found")
    return JSONResponse(content=status)