"""
register whatweb's tasks for celery to autodiscover
"""

import json

from celery import shared_task
from django.db import transaction

from apis.scanners.hosts.models import Host
from apis.scanners.tools import whatweb
from .models import WhatWeb


@shared_task
@transaction.atomic
def whatweb_task(ip_address: str):
    # retrieve scan response from celery background task
    data = whatweb.WhatWebScanner(ip_address).response()

    try:
        # retrieve host ip address
        host = Host.objects.get(ip_address=ip_address)
    except Host.DoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(ip_address)
    
    # create whatweb scan
    WhatWeb.create_whatweb_scan(host, data)

    # return the cleaned data
    return data
