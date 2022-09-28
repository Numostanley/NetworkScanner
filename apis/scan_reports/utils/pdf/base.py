from abc import ABC, abstractmethod

from datetime import datetime
from pathlib import Path

import weasyprint
from jinja2 import Environment, FileSystemLoader


class AbstractBasePDFGenerator(ABC):
    """Abstract Base Class for PDFGenerator"""

    @abstractmethod
    def get_app_dir(self):
        """retrieve the app directory"""
        pass

    @abstractmethod
    def locate_template_path(self):
        """locate the template path"""
        pass

    @abstractmethod
    def locate_static(self):
        """locate static path and file for the tool"""
        pass

    @abstractmethod
    def load_template_path(self):
        """load the template path with jinja2"""
        pass

    @abstractmethod
    def get_template(self):
        """retrieve the template file"""
        pass

    @abstractmethod
    def stringify_context(self):
        """stringify the context and load it in weasyprint for rendering"""
        pass

    @abstractmethod
    def generate_pdf(self):
        """generate pdf"""
        pass

    @abstractmethod
    def delete_pdf(self):
        """delete PDF"""
        pass


class PDFGenerator(AbstractBasePDFGenerator):

    def __init__(self,
        data,
        ip_address: str,
        tool: str,
        tool_template_file: str,
        tool_static_file: str
    ):
        self.data = data
        self.ip_address = ip_address
        self.tool = tool.lower()
        self.tool_template_file = tool_template_file.lower()
        self.tool_static_file = tool_static_file.lower()

    def get_app_dir(self) -> Path:
        """retrieve application directory i.e (scan_reports app)"""
        app_dir = Path(__file__).resolve().parent.parent.parent
        return app_dir

    def locate_template_path(self) -> str:
        """locate the template path of the specified tool"""
        template_path = f'{self.get_app_dir()}/templates/{self.tool}'
        return template_path

    def locate_static(self) -> str:
        """locate the static path and file for the tool"""
        static_path = f'{self.get_app_dir()}/static/{self.tool}'
        return f'{static_path}/{self.tool_static_file}'

    def load_template_path(self):
        """load the template path with jinja2"""
        template_path = self.locate_template_path()
        return Environment(loader=FileSystemLoader(template_path))

    def get_template(self):
        """retrieve the template file and load it into jinja2"""
        return self.load_template_path().get_template(self.tool_template_file)

    def stringify_context(self):
        """stringify the context and load it in weasyprint for rendering"""

        # get current date
        current_date = datetime.now()
        context = {
            'data': self.data,
            'current_date': current_date.strftime('%Y-%m-%d'),
            'ip_address': self.ip_address
        }
        stringify_context = self.get_template().render(context)

        html = weasyprint.HTML(string=stringify_context)
        return html

    def generate_pdf(self):
        """generate pdf using the IP address as the name and return pdf file path"""

        # get the root directory
        root_dir = self.get_app_dir().parent.parent
        html = self.stringify_context()

        # generate pdf
        html.write_pdf(
            f'file_downloads/scan_reports/{self.tool}/scan_report_on_{self.ip_address}.pdf',
            stylesheets=[self.locate_static()]
        )

        # create file_downloads/scan_report_statement/{self.tool}
        # folder in the project root directory if it does not exist
        Path(f'file_downloads/scan_reports/{self.tool}').mkdir(exist_ok=True, parents=True)

        # return pdf path
        file_name = f'{root_dir}/file_downloads/' \
                    f'scan_reports/{self.tool}/scan_report_on_{self.ip_address}.pdf'
        return file_name

    def delete_pdf(self):
        """delete pdf file after download."""
        Path(self.generate_pdf()).unlink(missing_ok=True)
