from .base import PDFGenerator


class CVEScannerPDFGenerator(PDFGenerator):
    """Generates PDF document for ip address scan report"""
    def __init__(self,
        data,
        ip_address: str,
        tool: str,
        tool_template_file: str,
        tool_static_file: str
    ):
        super(CVEScannerPDFGenerator, self).__init__(data, ip_address, tool,
                                                     tool_template_file, tool_static_file)
