"""
register scanners' tasks for celery to autodiscover
"""

from celery import shared_task

from apis.scanners.tools import cvescanner, dirby, sslyze, wafwoof, wapiti, whatweb


@shared_task
def cvescanner_task(ip_address: str):
    return cvescanner.CVEScanner(ip_address).response()


@shared_task
def dirby_task(ip_address: str):
    return dirby.DirByScanner(ip_address).response()


@shared_task
def sslyze_task(ip_address: str):
    return sslyze.SslyzeScanner(ip_address).response()


@shared_task
def wafwoof_task(ip_address: str):
    return wafwoof.WafWoofScanner(ip_address).response()


@shared_task
def wapiti_task(ip_address: str):
    return wapiti.WapitiScanner(ip_address).response()


@shared_task
def whatweb_task(ip_address: str):
    return whatweb.WhatWebScanner(ip_address).response()
