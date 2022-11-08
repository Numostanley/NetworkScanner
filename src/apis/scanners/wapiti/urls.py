from django.urls import path

from apis.scanners.wapiti import views


app_name = "wapiti"

urlpatterns = [
    # wapiti urls
    path('scan', views.WapitiScannerAPIView.as_view(), name='scan'),
    path('get-result', views.WapitiScanResultAPIView.as_view(), name='result')
]
