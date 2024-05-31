from abc import ABC, abstractmethod

class PDFParser(ABC):
    

    @abstractmethod
    def parse_specific_pdf(self,pdf_name,page_number, batch_id):
        """
        Parse a specific PDF file.
        Args:
        filepath (str): The path to the PDF file to parse.
        """
        pass
    
    @abstractmethod
    def parse_all_pdfs(self, batch_id):
        """
        Parse all PDF files within a given directory. If the file is already parsed, it will skip.
        Args:
        directory (str): The path to the directory containing PDF files.
        """
        pass
    
    @abstractmethod
    def configuration(self, **kwargs):
        """
        Configure the pdf -parser settings.
        Args:
        **kwargs: Arbitrary keyword arguments for configuration settings.
        """
        pass



    @abstractmethod
    def view_parsed_pdf(self,pdf_name,format):
        """
        Display the parsed result of a PDF file in Markdown, JSON, or HTML format.
        
        Args:
        pdf_name (str): The name of the PDF file to display results for.
        format (str): The format to display the results in ('markdown', 'json', 'html').

        Returns:
        str: The result in the requested format.
        """
        pass

    @abstractmethod
    def all_source_files(self):
        """
        Get all the ESG pdf files list that are present in the source path.
        """
        pass

    @abstractmethod
    def get_status(self):
        """
        Get the current status of the parser.
        Returns:
        str: The status of the parser.
        """
        pass