from datetime import datetime
from pathlib import Path

import weasyprint
from jinja2 import Environment, FileSystemLoader

from .nmap_scan import scan_ip_address


def generate_scan_report_pdf(ip_address: str):
    """generate a pdf report for the specified IP address."""

    ip_address = ip_address

    # locate the parent directory of this module i.e pdf.py
    parent_dir = Path(__file__).resolve().parent

    # locate the templates path and template file
    template_path = f'{parent_dir}/templates'
    template_file = f'scan_report.html'

    # locate static path and static file
    static_path = f'{parent_dir}/static'
    static_file = f'main.css'

    css_style = f'{static_path}/{static_file}'

    # load the template with jinja2
    load_template = Environment(loader=FileSystemLoader(template_path))

    # get the template
    template = load_template.get_template(template_file)

    # get current date
    current_date = datetime.now()

    # retrieve result from nmap scan
    data = scan_ip_address(ip_address)

    context = {
        'data': data,
        'current_date': current_date.strftime('%Y-%m-%d'),
        'ip_address': ip_address
    }

    # render context as string
    stringify_context = template.render(context)

    html = weasyprint.HTML(string=stringify_context)

    # create file_downloads/scan_report_statement/ folder in the project root directory if it does not exist
    Path('file_downloads/scan_reports').mkdir(exist_ok=True, parents=True)

    # generate pdf with a name
    html.write_pdf(
        f'file_downloads/scan_reports/scan_report_on_{ip_address}.pdf',
        stylesheets=[css_style]
    )

    # return pdf path
    file_name = f'{parent_dir.parent.parent}/file_downloads/scan_reports/scan_report_on_{ip_address}.pdf'
    return file_name


def delete_scan_report(file_path: Path):
    """delete pdf file after download."""
    Path(file_path).unlink(missing_ok=True)
