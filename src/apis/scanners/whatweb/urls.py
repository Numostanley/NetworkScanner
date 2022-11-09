from django.urls import path

from apis.scanners.whatweb import views


app_name = "whatweb"

urlpatterns = [
    # whatweb urls
    path('scan', views.WhatWebScannerAPIView.as_view(), name='scan'),
    path('get-result', views.WhatWebScanResultAPIView.as_view(), name='result')
]
