from pathlib import Path

import weasyprint

from django.test import TestCase
from jinja2 import Environment, Template

from apis.scanners.utils.pdf.base import PDFGenerator
from apis.scanners.utils.pdf.cvescanner import CVEScannerPDFGenerator


class PDFGeneratorTest(TestCase):
    data = []
    ip_address = '111.11.222.33'
    tool = 'cvescanner'
    tool_template_file = 'cve_scan_report.html'
    tool_static_file = 'cve_main.css'

    def setUp(self) -> None:
        self.scanners_dir = Path(__file__).resolve().parent.parent.parent
        self.cve_pdf = CVEScannerPDFGenerator(
            self.data,
            self.ip_address,
            self.tool,
            self.tool_template_file,
            self.tool_static_file
        )

    def test_pdf_creation(self):
        self.assertIsInstance(self.cve_pdf, PDFGenerator)

    def test_get_app_dir(self):
        self.assertEqual(self.cve_pdf.get_app_dir(), self.scanners_dir)

    def test_locate_template_path(self):
        self.assertEqual(self.cve_pdf.locate_template_path(),
                         f'{self.cve_pdf.get_app_dir()}/templates/{self.tool}')

    def test_locate_static(self):
        static_path = f'{self.cve_pdf.get_app_dir()}/static/{self.tool}'
        self.assertEqual(self.cve_pdf.locate_static(),
                         f'{static_path}/{self.tool_static_file}')

    def test_load_template_path(self):
        self.assertIsInstance(self.cve_pdf.load_template_path(), Environment)

    def test_get_template(self):
        self.assertIsInstance(self.cve_pdf.get_template(), Template)

    def test_stringify_context(self):
        self.assertIsInstance(self.cve_pdf.stringify_context(), weasyprint.HTML)

    def test_generate_pdf(self):  # issue
        self.assertIsInstance(self.cve_pdf.generate_pdf(), bytes)

    def test_return_pdf_file_path(self):
        root_dir = self.cve_pdf.get_app_dir().parent.parent
        file_path = f'{root_dir}/file_downloads/scanners/{self.tool}/scan_report_on_{self.ip_address}.pdf'
        self.assertEqual(self.cve_pdf.return_pdf_file_path(), file_path)

    def test_delete_pdf(self):
        self.assertTrue(self.cve_pdf.delete_pdf(), True)
