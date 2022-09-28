from django.urls import path

from apis.scan_reports.views import cvescanner, whatweb


urlpatterns = [
    # cvescanner urls
    path('cve-download', cvescanner.CVEDownloadScanReportAPIView.as_view()),
    path('cve-scan-ip', cvescanner.CVEScannerAPIView.as_view()),

    # whatweb
    path('whatweb-scan-ip', whatweb.WhatWebScannerAPIView.as_view()),
]
