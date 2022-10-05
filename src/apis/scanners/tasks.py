"""
register scanners' tasks for celery to autodiscover
"""

from celery import shared_task
from .models.wapiti import Wapiti
from .models.base import Host
from django.core.exceptions import ObjectDoesNotExist
import json

from apis.scanners.tools import cvescanner, dirby, sslyze, wafwoof, wapiti, whatweb


@shared_task
def cvescanner_task(ip_address: str):
    return cvescanner.CVEScanner(ip_address).response()


@shared_task
def dirby_task(ip_address: str):
    return dirby.DirByScanner(ip_address).response()


@shared_task
def sslyze_task(ip_address: str):
    
    task = sslyze.SslyzeScanner(ip_address)
    data = task.response()
    
    return data


@shared_task
def wafwoof_task(ip_address: str):
    return wafwoof.WafWoofScanner(ip_address).response()


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
def whatweb_task(ip_address: str):
    return whatweb.WhatWebScanner(ip_address).response()


