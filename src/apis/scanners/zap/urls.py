from django.urls import path

from . import views


app_name = "zap"

urlpatterns = [
    # zap urls
    path('scan', views.ZapScannerAPIView.as_view(), name='scan'),
    path('get-result', views.ZapScanResultAPIView.as_view(), name='result'),
]
