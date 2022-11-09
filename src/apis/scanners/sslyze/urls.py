from django.urls import path

from apis.scanners.sslyze import views


app_name = "sslyze"

urlpatterns = [
    # sslyze urls
    path('scan', views.SslyzeScannerAPIView.as_view(), name='scan'),
    path('get-result', views.SSLyzeScanResultAPIView.as_view(), name='result'),
]
