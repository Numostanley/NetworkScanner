from django.urls import path

from apis.scanners.whatweb import views


urlpatterns = [
    # whatweb urls
    path('scan', views.WhatWebScannerAPIView.as_view()),
]
