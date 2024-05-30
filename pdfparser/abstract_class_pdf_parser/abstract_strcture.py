from abc import ABC, abstractmethod

class PDFParser(ABC):
    

    @abstractmethod
    def parse_specific_pdf(self, filepath):
        """
        Parse a specific PDF file.
        Args:
        filepath (str): The path to the PDF file to parse.
        """
        pass
    
    @abstractmethod
    def parse_all_pdfs(self):
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
    def get_status(self):
        """
        Get the current status of the parser.
        Returns:
        str: The status of the parser.
        """
        pass