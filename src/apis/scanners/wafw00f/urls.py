from django.urls import path

from apis.scanners.wafw00f import views


app_name = "wafwoof"

urlpatterns = [
    # wafwoof urls
    path('scan', views.WafWoofScannerAPIView.as_view(), name='scan'),
    path('get-result', views.WafW00fScanResultAPIView.as_view(), name='result')
]
