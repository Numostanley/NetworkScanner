"""
register scanners' tasks for celery to autodiscover
"""

from celery import shared_task

from apis.scanners.tools import cvescanner, dirby, sslyze, wafwoof, wapiti, whatweb


@shared_task
def cvescanner_task(ip_address: str):
    cvescanner.CVEScanner(ip_address).run()


@shared_task
def dirby_task(ip_address: str):
    dirby.DirByScanner(ip_address).run()


@shared_task
def sslyze_task(ip_address: str):
    sslyze.SslyzeScanner(ip_address).run()


@shared_task
def wafwoof_task(ip_address: str):
    wafwoof.WafWoofScanner(ip_address).run()


@shared_task
def wapiti_task(ip_address: str):
    wapiti.WapitiScanner(ip_address).run()


@shared_task
def whatweb_task(ip_address: str):
    whatweb.WhatWebScanner(ip_address).run()
