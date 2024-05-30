from pdfparser.logger import logging
from pdfparser.exception import PdfParserException
from pdfparser.abstract_class_pdf_parser.abstract_strcture import PDFParser
import asyncio
from fastapi import HTTPException
import os,sys
import subprocess
from dotenv import load_dotenv
import uuid

# Load environment variables from the .env file
load_dotenv()

class MarkerPDFParser(PDFParser):
    def __init__(self):
        self.tasks = {}  # Stores status keyed by batch_id

    async def run_command(self, command, pdf_file, batch_id):
        """Run the command asynchronously and track its status."""
        proc = await asyncio.create_subprocess_shell(
            ' '.join(command),  # Command needs to be a single string for shell execution
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            self.tasks[batch_id]['files'][pdf_file] = 'success'
        else:
            self.tasks[batch_id]['files'][pdf_file] = 'failed'
            logging.error(f"Failed to parse {pdf_file}, Error: {stderr.decode()}")   
    

    async def parse_specific_pdf(self, filepath):
        # Implementation-specific method to parse a single PDF file
        pass

    async def parse_all_pdfs(self):
        """
        Parse all PDF files within the directory specified by the SOURCE_PDF_PATH
        environment variable using the `marker` command line tool.
        """
        logging.info(f"{'>>'*20} Parse All Pdf - Marker Pdf {'<<'*20}")
        # Fetch the source directory and destination directory from environment variables
        directory = os.getenv("SOURCE_PDF_PATH", "")
        
        if not directory:
            logging.error("Source PDF path not specified.")
            raise ValueError("Source PDF path not specified.")
        else:
            logging.info(f"The source directory exists")


        if not os.path.isdir(directory):
            logging.error(f"The directory {directory} does not exist.")
            raise ValueError(f"The directory {directory} does not exist.")
        else:
            logging.info(f"The destination directory exists")

        batch_id = str(uuid.uuid4())
        self.tasks[batch_id] = {'overall': 'running', 'files': {}}
        logging.info(f"Response id: {batch_id }")

        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

        if not pdf_files:
            logging.info(f"No PDF files found to process. Batch ID: {batch_id}")
            self.tasks[batch_id]['overall'] = 'no files'
            return batch_id
        else:
            logging.info(f"Individual pdf Parsing will start.")
            self.tasks[batch_id]['overall'] = 'files are present processing will start.'

        destination_pdf_path = os.getenv("DESTINATION_PDF_PATH", "")
        """       
        for pdf_file in pdf_files:
            source_file_path = os.path.join(directory, pdf_file)
            logging.info(f"Started Parsing the file:  {source_file_path}, Batch ID: {batch_id}")
            try:
                command = ["marker_single", source_file_path, destination_pdf_path]
                subprocess.check_call(command)
                logging.info(f"Successfully parsed {source_file_path}, Batch ID: {batch_id}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to parse {source_file_path}, Batch ID: {batch_id}: {str(e)}")
                raise PdfParserException("PDF parsing failed", sys)
            except Exception as e:
                logging.error(f"Unexpected error, Batch ID: {batch_id}: {str(e)}")
                raise PdfParserException("An unexpected error occurred", sys)
        """
        tasks = []
        for pdf_file in pdf_files:
            source_file_path = os.path.join(directory, pdf_file)
            logging.info(f"Started Parsing the file:  {source_file_path}, Batch ID: {batch_id}")
            command = ["marker_single", source_file_path, destination_pdf_path]
            self.tasks[batch_id]['files'][pdf_file] = 'in progress parsing the file {pdf_file}'
            task = asyncio.create_task(self.run_command(command, pdf_file, batch_id))
            tasks.append(task)
            logging.info(f"Successfully parsed {source_file_path}, Batch ID: {batch_id}")
        await asyncio.gather(*tasks)
        return batch_id


    def configuration(self, **kwargs):
        # Implementation for setting configurations
        pass

    def get_status(self, batch_id):
        # Return the status of the PDF parsing operation based on the batch_id
        return self.status_dict.get(batch_id, "No such batch ID")