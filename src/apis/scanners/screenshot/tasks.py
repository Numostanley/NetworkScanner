"""
register screenshot's task for celery to autodiscover
"""

from celery import shared_task
from django.db import transaction

from apis.scanners.hosts.models import Host
from apis.scanners.tools import screenshot


@shared_task
@transaction.atomic
def screenshot_task(ip_address: str):
    # retrieve scan response from celery background task
    data = screenshot.ScreenShotScanner(ip_address).response()

    try:
        # retrieve host ip address
        Host.objects.get(ip_address=ip_address)
    except Host.DoesNotExist:
        # if host ip address does not exist, create new host
        Host.create_host(ip_address)

    # return the cleaned data
    return data
