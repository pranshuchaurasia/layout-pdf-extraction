import os
from fastapi import FastAPI, HTTPException
from pdfparser.marker.marker_pdf import MarkerPDFParser
import uvicorn
app = FastAPI()
parser = MarkerPDFParser()  # Initialize the parser

'''
def main():
    
    
    @app.post("/parse/")
    async def parse_pdfs():
        """
        Endpoint to initiate PDF parsing.
        Returns a batch ID for tracking the operation.
        """
        try:
            batch_id = await parser.parse_all_pdfs()
            return {"batch_id": batch_id, "message": "PDF parsing initiated, track with batch ID."}
        except HTTPException as e:
            return {"error": str(e.detail)}
        except Exception as e:
            return {"error": str(e)}

    @app.get("/status/{batch_id}")
    async def get_status(batch_id: str):
        """
        Endpoint to get the status of a PDF parsing operation.
        Requires a batch ID.
        """
        status = parser.get_status(batch_id)
        if status == "No such batch ID":
            raise HTTPException(status_code=404, detail="Batch ID not found")
        return {"batch_id": batch_id, "status": status}

"""
parser = MarkerPDFParser()
parser.parse_all_pdfs()
"""
if __name__ == "__main__":
    main()
'''


@app.post("/parse/parse_all_pdf")
async def parse_all_pdfs():
    """
    Endpoint to initiate PDF parsing.
    Returns a batch ID for tracking the operation.
    """
    try:
        batch_id = await parser.parse_all_pdfs()
        return {"batch_id": batch_id, "message": "PDF parsing initiated, track with batch ID."}
    except HTTPException as e:
        return {"error": str(e.detail)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/pdfparser/status/{batch_id}")
async def get_status(batch_id: str):
    """
    Endpoint to get the status of a PDF parsing operation.
    Requires a batch ID.
    """
    status = parser.get_status(batch_id)
    if status == "No such batch ID":
        raise HTTPException(status_code=404, detail="Batch ID not found")
    return {"batch_id": batch_id, "status": status}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)