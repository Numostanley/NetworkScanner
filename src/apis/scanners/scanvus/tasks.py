"""
register scanvus's task for celery to autodiscover
"""

from celery import shared_task
from django.db import transaction

from apis.scanners.hosts.models import Host
from apis.scanners.tools import scanvus
from .models import Scanvus


@shared_task
@transaction.atomic
def scanvus_task(ip_address: str, username: str, password: str):
    task = scanvus.ScanvusScanner(ip_address, username, password)
    data = task.response()

    try:
        # retrieve host ip address
        host = Host.objects.get(ip_address=ip_address)
    except Host.DoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(
            ip_address=ip_address
        )

    # populate Scanvus table
    Scanvus.create_scanvus_scan(host=host, data=data)

    # return the cleaned data
    return data
