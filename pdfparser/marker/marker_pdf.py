from pdfparser.logger import logging
from pdfparser.exception import PdfParserException
from pdfparser.abstract_class_pdf_parser.abstract_strcture import PDFParser
import os, sys
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Assuming .env at the root or set path accordingly

class MarkerPDFParser(PDFParser):
    
    def __init__(self):
        self.status_dict = {}  # Dictionary to keep track of status of each batch

    def parse_specific_pdf(self, filepath):
        # Implementation-specific method to parse a single PDF file
        pass

    def parse_all_pdfs(self, batch_id):
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

        logging.info(f"Response id for the request: {batch_id }")

        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

        if not pdf_files:
            logging.info(f"No PDF files found to process. Batch ID: {batch_id}")
            self.status_dict[batch_id] = {}
            return
        else:
            logging.info(f"Individual pdf Parsing will start.")
        
        destination_pdf_path = os.getenv("DESTINATION_PDF_PATH", "")
        if not destination_pdf_path:
            logging.error("DESTINATION PDF path not specified")
            raise ValueError("DESTINATION PDF path not specified.")
        else:
            logging.info(f"DESTINATION_PDF_PATH: {os.getenv('DESTINATION_PDF_PATH')}") 

        self.status_dict[batch_id] = {}
        for pdf_file in pdf_files:
            source_file_path = os.path.join(directory, pdf_file)
            self.status_dict[batch_id][pdf_file] = "In Progress"
            try:
                logging.info(f"Started Parsing the file:  {source_file_path}, Batch ID: {batch_id}")
                command = ["marker_single", source_file_path, destination_pdf_path]
                result = subprocess.run(command, capture_output=True, text=True)
                logging.info(f"Command output: {result.stdout}")
                if result.returncode == 0:
                    self.status_dict[batch_id][pdf_file] = "Completed"
                    logging.info(f"Successfully parsed {source_file_path}, Batch ID: {batch_id}")
                else:
                    self.status_dict[batch_id][pdf_file] = "Failed"
                    logging.error(f"Failed to parse {source_file_path}, Batch ID: {batch_id}: {result.stderr}")
                    raise PdfParserException("PDF parsing failed", sys)
            except subprocess.CalledProcessError as e:
                self.status_dict[batch_id][pdf_file] = "Failed"
                logging.error(f"Failed to parse {source_file_path}, Batch ID: {batch_id}: {str(e)}")
                raise PdfParserException("PDF parsing failed", sys)
            except Exception as e:
                self.status_dict[batch_id][pdf_file] = "Failed"
                logging.error(f"Unexpected error, Batch ID: {batch_id}: {str(e)}")
                raise PdfParserException("An unexpected error occurred", sys)

    def configuration(self, **kwargs):
        # Implementation for setting configurations
        pass

    def get_status(self, batch_id):
        """
        Return the status of the PDF parsing process for a specific batch.
        """
        return self.status_dict.get(batch_id, "Batch ID not found")
