"""
register dirby's task for celery to autodiscover
"""

import json

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
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
        host = Host.get_host(ip_address)
    except ObjectDoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(ip_address)

    # deserialize data from json to python objects
    cleaned_data = json.loads(data)

    # create dirby scan
    DirBy.create_dirby_scan(host, cleaned_data)

    # return the cleaned data
    return cleaned_data
