from pdfparser.logger import logging
from pdfparser.exception import PdfParserException
from pdfparser.abstract_class_pdf_parser.abstract_strcture import PDFParser
import os, sys
import markdown,json
import subprocess
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from bs4 import BeautifulSoup

load_dotenv()  # Assuming .env at the root or set path accordingly

class MarkerPDFParser(PDFParser):
    
    def __init__(self):
        self.status_dict = {}  # Dictionary to keep track of status of each batch
        self.destination_path = os.getenv("DESTINATION_PDF_PATH", "")

    def parse_specific_pdf(self,pdf_name,page_number, batch_id):
        # Implementation-specific method to parse a single PDF file
        # Fetch the source and destination directory from environment variables
        logging.info(f"Response id for the individual pdf parsing request: {batch_id }") 
        source_directory = os.getenv("SOURCE_PDF_PATH", "")
        if not source_directory:
            logging.error("Source PDF path not specified")
            raise ValueError("Source PDF path not specified.")
        else:
            logging.info(f" SOURCE_PDF_PATH: {os.getenv('SOURCE_PDF_PATH')}") 
            
        destination_pdf_path = os.getenv("DESTINATION_PDF_PATH", "")
        if not destination_pdf_path:
            logging.error("Destination PDF path not specified")
            raise ValueError("Destination PDF path not specified.")
        else:
            logging.info(f"DESTINATION_PDF_PATH: {os.getenv('DESTINATION_PDF_PATH')}") 

           
        pdf_file_path = os.path.join(source_directory, pdf_name)
        if not os.path.exists(pdf_file_path):
            logging.error(f"PDF file not found: {pdf_file_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_file_path}")
        else:
            logging.info(f"PDF file is found at: {pdf_file_path}")
        self.status_dict[batch_id] = {pdf_name: "In Progress"}

        try:
            # Define the path for extracted pages
            specific_pages_path = os.path.join(destination_pdf_path, "specific_pages")
            if not os.path.exists(specific_pages_path):
                logging.info(f"Careating specific pages path: {specific_pages_path}")
                os.makedirs(specific_pages_path)

            extracted_pdf_path = pdf_file_path  # default path is the original file
            if page_number:
                logging.info(f"User has given Page number to extract from pdf: {page_number}")
                reader = PdfReader(pdf_file_path)
                writer = PdfWriter()

                # Extract the specified page (pages are zero-indexed in PyPDF)
                logging.info(f"Extract the specified page (pages are zero-indexed in PyPDF): {page_number}")
                writer.add_page(reader.pages[page_number - 1])

                extracted_pdf_path = os.path.join(source_directory, f"extracted_page_{page_number}_{pdf_name}")
                logging.info(f"Saving the extracted pdf: {extracted_pdf_path}")
                with open(extracted_pdf_path, 'wb') as f:
                    writer.write(f)
                
            # Process the new or original PDF
            command = ["marker_single", extracted_pdf_path, destination_pdf_path]
            logging.info(f"The marker command: {command}")
            logging.info(f"Started parsing the file: {extracted_pdf_path}, Batch ID: {batch_id}")
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                self.status_dict[batch_id][pdf_name] = "Completed"
                logging.info(f"Successfully parsed {extracted_pdf_path}, Batch ID: {batch_id}")
            else:
                self.status_dict[batch_id][pdf_name] = "Failed"
                logging.error(f"Failed to parse {extracted_pdf_path}, Batch ID: {batch_id}: {result.stderr}")
                raise PdfParserException("PDF parsing failed", sys)
        except subprocess.CalledProcessError as e:
            self.status_dict[batch_id][pdf_name] = "Failed"
            logging.error(f"Failed to parse {extracted_pdf_path}, Batch ID: {batch_id}: {str(e)}")
            raise PdfParserException("PDF parsing subprocess failed", e)
        except Exception as e:
            self.status_dict[batch_id][pdf_name] = "Failed"
            logging.error(f"Unexpected error, Batch ID: {batch_id}: {str(e)}")
            raise PdfParserException("An unexpected error occurred", e)

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
            logging.info(f" SOURCE_PDF_PATH: {os.getenv('SOURCE_PDF_PATH')}")   

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
    
    def all_source_files(self):
        """
        Get all the ESG pdf files list that are present in the source path.
        """
        # Fetch the source directory and destination directory from environment variables
        directory = os.getenv("SOURCE_PDF_PATH", "")
        if not directory:
            logging.error("Source PDF path not specified")
            raise ValueError("Source PDF path not specified.")
        else:
            logging.info(f" SOURCE_PDF_PATH: {os.getenv('SOURCE_PDF_PATH')}")   


        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

        if not pdf_files:
            logging.info(f"No PDF files found in the source path.")
            return ("No PDF files found in the source path.")
        else:
            logging.info(f"We will display the list of all ESG files present in the path.")
            return pdf_files

    def view_parsed_pdf(self, pdf_name: str, format: str = "markdown"):

        destination_path = os.getenv("DESTINATION_PDF_PATH", "")
        # Remove '.pdf' extension if present
        if pdf_name.lower().endswith(".pdf"):
            logging.info(f"Removing .pdf extension from: {pdf_name}") 
            pdf_name = pdf_name[:-4]  # Remove the last four characters

        
        if not destination_path:
            logging.error("DESTINATION PDF path not specified")
            raise ValueError("DESTINATION PDF path not specified.")
        else:
            logging.info(f"DESTINATION_PDF_PATH: {os.getenv('DESTINATION_PDF_PATH')}") 
        # Directory setup
        logging.info(f"Creating json and html path") 
        try:
            json_path = os.path.join(self.destination_path, "pdf_json")
            html_path = os.path.join(self.destination_path, "pdf_html")
            os.makedirs(json_path, exist_ok=True)
            os.makedirs(html_path, exist_ok=True)
        except Exception as e:
            logging.error(f"Issue in creating json/html directory.") 
            raise PdfParserException(e, sys)
        

        try:
            markdown_path = os.path.join(self.destination_path, f"{pdf_name}/{pdf_name}.md")
            logging.info(f"MARKDOWN_PATH: {markdown_path}") 
            with open(markdown_path, "r") as file:
                markdown_content = file.read()
                #logging.info(f"MARKDOWN_CONTENT: {markdown_content}") 
        except FileNotFoundError:
            logging.error(f"Result file does not exist for the specified PDF.") 
            raise ValueError("Result file does not exist for the specified PDF.")
            
        
        if format == "markdown":
            logging.info(f"Started Processing to display markdown contents") 
            # Return markdown content and associated images
            image_paths = [os.path.join(self.destination_path, pdf_name, img) for img in os.listdir(os.path.join(self.destination_path, pdf_name)) if img.endswith(('.png', '.jpg', '.jpeg'))]
            logging.info(f"Process successful for markdown.") 
            return markdown_content, image_paths
                   
        elif format == "html":
            logging.info(f"Processing to display html contents") 
            html_content = markdown.markdown(markdown_content)
            html_file_path = os.path.join(html_path, f"{pdf_name}.html")
            with open(html_file_path, 'w') as html_file:
                html_file.write(html_content)
            logging.info(f"Process successful for html.") 
            return html_file_path
        else:
            logging.error(f"Unsupported format specified. Choose 'markdown', or 'html'.") 
            raise ValueError("Unsupported format specified. Choose 'markdown', or 'html'.")

    def get_status(self, batch_id):
        """
        Return the status of the PDF parsing process for a specific batch.
        """
        return self.status_dict.get(batch_id, "Batch ID not found")
