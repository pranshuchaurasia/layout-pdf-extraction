import os
from fastapi import FastAPI, HTTPException
from pdfparser.marker.marker_pdf import MarkerPDFParser
import uvicorn
#app = FastAPI()
parser = MarkerPDFParser()  # Initialize the parser

def main():
    parser = MarkerPDFParser()
    parser.parse_all_pdfs()

if __name__ == "__main__":
    main()