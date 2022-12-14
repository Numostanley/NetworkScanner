"""
register dirby's task for celery to autodiscover
"""

from celery import shared_task
from django.db import transaction

from apis.scanners.hosts.models import Host
from apis.scanners.tools import dirby
from .models import DirBy


@shared_task
@transaction.atomic
def dirby_task(ip_address: str):
    # retrieve scan response from celery background task
    data = dirby.DirByScanner(ip_address).response()

    try:
        # retrieve host ip address
        host = Host.objects.get(ip_address=ip_address)
    except Host.DoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(ip_address)

    # create dirby scan
    DirBy.create_dirby_scan(host, data)

    # return the cleaned data
    return data
