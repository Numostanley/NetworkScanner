from django.urls import path

from apis.scanners.scanvus import views


app_name = "scanvus"

urlpatterns = [
    # scanvus urls
    path('scan', views.ScanvusScannerAPIView.as_view(), name='scan'),
    path('get-result', views.ScanvusScanResultAPIView.as_view(), name='result')
]
