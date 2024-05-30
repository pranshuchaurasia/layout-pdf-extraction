from pdfparser.logger import logging
from pdfparser.exception import PdfParserException
from pdfparser.abstract_class_pdf_parser.abstract_strcture import PDFParser
import anyio
from fastapi import HTTPException
import os, sys
import subprocess
from dotenv import load_dotenv
import uuid

load_dotenv()  # Assuming .env at the root or set path accordingly

class MarkerPDFParser(PDFParser):
    
    def parse_specific_pdf(self, filepath):
        # Implementation-specific method to parse a single PDF file
        pass

    def parse_all_pdfs(self):
        """
        Parse all PDF files within the directory specified by the SOURCE_PDF_PATH
        environment variable using the `marker` command line tool.
        """
        # Fetch the source directory and destination directory from environment variables
        directory = os.getenv("SOURCE_PDF_PATH", "")
        if not directory:
            logging.error("Source PDF path not specified")
            raise ValueError("Source PDF path not specified.")
        else:
            logging.info(f"Environment Variable SOURCE_PDF_PATH: {os.getenv('SOURCE_PDF_PATH')}")   

        batch_id = str(uuid.uuid4())  # Unique ID for the batch
        logging.info(f"Response id: {batch_id }")

        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

        if not pdf_files:
            logging.info(f"No PDF files found to process. Batch ID: {batch_id}")
            return
        else:
            logging.info(f"Individual pdf Parsing will start.")
        
        destination_pdf_path = os.getenv("DESTINATION_PDF_PATH", "")
        if not destination_pdf_path :
            logging.error("DESTINATION PDF path not specified")
            raise ValueError("DESTINATION PDF path not specified.")
        else:
            logging.info(f"DESTINATION_PDF_PATH: {os.getenv('DESTINATION_PDF_PATH')}") 

        for pdf_file in pdf_files:
            source_file_path = os.path.join(directory, pdf_file)
            try:
                logging.info(f"Started Parsing the file:  {source_file_path}, Batch ID: {batch_id}")
                command = ["marker_single", source_file_path, destination_pdf_path]
                result = subprocess.run(command, capture_output=True, text=True)
                logging.info(f"Command output: {result.stdout}")
                if result.returncode == 0:
                    logging.info(f"Successfully parsed {source_file_path}, Batch ID: {batch_id}")
                else:
                    logging.error(f"Failed to parse {source_file_path}, Batch ID: {batch_id}: {result.stderr}")
                    raise PdfParserException("PDF parsing failed", sys)
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to parse {source_file_path}, Batch ID: {batch_id}: {str(e)}")
                raise PdfParserException("PDF parsing failed", sys)
            except Exception as e:
                logging.error(f"Unexpected error, Batch ID: {batch_id}: {str(e)}")
                raise PdfParserException("An unexpected error occurred", sys)
        #return batch_id

    def configuration(self, **kwargs):
        # Implementation for setting configurations
        pass

    def get_status(self):
        # Implementation for checking the parser's status
        pass
