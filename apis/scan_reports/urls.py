from django.urls import path

from apis.scan_reports.views import cvescanner, dirby, wafwoof, wapiti, whatweb


urlpatterns = [
    # cvescanner urls
    path('cve-download', cvescanner.CVEDownloadScanReportAPIView.as_view()),
    path('cve-scan', cvescanner.CVEScannerAPIView.as_view()),

    # dirb urls
    path('dirby-scan', dirby.DirByScannerAPIView.as_view()),

    # wafwoof urls
    path('wafwoof-scan', wafwoof.WafWoofScannerAPIView.as_view()),

    # wapiti urls
    path('wapiti-scan', wapiti.WapitiScannerAPIView.as_view()),

    # whatweb urls
    path('whatweb-scan', whatweb.WhatWebScannerAPIView.as_view()),
]
