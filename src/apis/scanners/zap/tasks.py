"""
register zap's task for celery to autodiscover
"""

from celery import shared_task
from django.db import transaction

from apis.scanners.hosts.models import Host
from apis.scanners.tools import zap
from .models import Zap


@shared_task
@transaction.atomic
def zap_task(ip_address: str, api_key: str):

    task = zap.ZapScanner(ip_address, api_key)
    data = task.response()

    http_prefixes = ['http://', 'https://']

    for http_prefix in http_prefixes:
        if ip_address.startswith(http_prefix):
            ip_address = ip_address.removeprefix(http_prefix)

    try:
        # retrieve host ip address
        host = Host.objects.get(ip_address=ip_address)
    except Host.DoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(host=ip_address)

    # populate Zap table
    Zap.create_zap_scan(host, data)

    # return the cleaned data
    return data
