"""
register cvescannerv2's task for celery to autodiscover
"""

import json

from celery import shared_task
from django.db import transaction
from django.http import FileResponse

from apis.scanners.hosts.models import Host
from apis.scanners.tools import cvescanner
from apis.scanners.utils.pdf.cvescanner import CVEScannerPDFGenerator
from apis.utils.error_logs import logger
from .models import CVEScannerV2


@shared_task
@transaction.atomic
def cvescanner_task(ip_address: str):
    task = cvescanner.CVEScanner(ip_address)
    data = task.response()

    try:
        # retrieve host ip address
        host = Host.objects.get(ip_address=ip_address)
    except Host.DoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(
            ip_address=ip_address
        )

    # deserialize data from json to python objects
    data_cleaned = json.loads(data)

    # populate CVEScannerV2 table
    CVEScannerV2.create_cvescanner_scan(host=host, data=data_cleaned)

    # return the cleaned data
    return data_cleaned


@shared_task
def send_pdf_report(data, host: Host):
    tool = 'cvescanner'
    template_file_name = 'cve_scan_report.html'
    static_file = 'cve_main.css'
    cve_pdf = CVEScannerPDFGenerator(data, host.ip_address, tool, template_file_name, static_file)

    # generate pdf and return file path
    pdf = cve_pdf.generate_pdf()

    try:
        # return generated scan report as response
        file_response = FileResponse(open(pdf, 'rb'),
                                     as_attachment=True,
                                     filename=pdf)
        return file_response
    except Exception as e:
        logger.error('send_pdf_report@Error')
        logger.error(e)
        return None
    finally:
        # delete file
        cve_pdf.delete_pdf()
