"""
register sslyze's task for celery to autodiscover
"""

import json

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apis.scanners.hosts.models import Host
from apis.scanners.tools import sslyze
from .models import SSLyze


@shared_task
@transaction.atomic
def sslyze_task(ip_address: str):
    task = sslyze.SslyzeScanner(ip_address)
    data = task.response()

    try:
        # retrieve host ip address
        host = Host.get_host(ip_address=ip_address)
    except ObjectDoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(
            ip_address=ip_address
        )

    # deserialize data from json to python objects
    data_cleaned = json.loads(data)

    # populate SSLyze table
    SSLyze.create_sslyze_scan(host=host, data=data_cleaned[0])

    # return the cleaned data
    return data_cleaned
