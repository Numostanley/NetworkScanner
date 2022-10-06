"""
register scanners' tasks for celery to autodiscover
"""

import json

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from .models.base import Host
from .models.dirby import DirBy
from .models.wafwoof import WafWoof
from .models.wapiti import Wapiti
from .models.whatweb import WhatWeb

from apis.scanners.tools import cvescanner, dirby, sslyze, wafwoof, wapiti, whatweb


@shared_task
def cvescanner_task(ip_address: str):
    return cvescanner.CVEScanner(ip_address).response()


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


@shared_task
def sslyze_task(ip_address: str):
    
    task = sslyze.SslyzeScanner(ip_address)
    data = task.response()
    
    return data


@shared_task
@transaction.atomic
def wafwoof_task(ip_address: str):
    # retrieve scan response from celery background task
    data = wafwoof.WafWoofScanner(ip_address).response()

    try:
        # retrieve host ip address
        host = Host.get_host(ip_address)
    except ObjectDoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(ip_address)

    # deserialize data from json to python objects
    cleaned_data = json.loads(data)

    # create wafw00f scan
    WafWoof.create_wafwoof_scan(host, cleaned_data)

    # return the cleaned data
    return cleaned_data


@shared_task
def wapiti_task(ip_address: str):
    
    task = wapiti.WapitiScanner(ip_address)
    data = task.response()
    
    try:
        host = Host.objects.get(ip_address=ip_address)
    except ObjectDoesNotExist:
        host = Host.create_host(
            ip_address=ip_address
        )
        
    data_cleaned = json.loads(data)
    
    Wapiti.create_wapiti_scan(host=host, data=data_cleaned)
    
    return data_cleaned


@shared_task
@transaction.atomic
def whatweb_task(ip_address: str):
    # retrieve scan response from celery background task
    data = whatweb.WhatWebScanner(ip_address).response()

    try:
        # retrieve host ip address
        host = Host.get_host(ip_address)
    except ObjectDoesNotExist:
        # if host ip address does not exist, create new host
        host = Host.create_host(ip_address)

    # deserialize data from json to python objects
    cleaned_data = json.loads(data)

    # create whatweb scan
    WhatWeb.create_whatweb_scan(host, cleaned_data)

    # return the cleaned data
    return cleaned_data
