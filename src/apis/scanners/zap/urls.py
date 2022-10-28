from django.urls import path

from . import views

app_name = "zap"

urlpatterns = [
    # zap urls
    path('scan', views.ZapScannerAPIView.as_view()),
    # path('get-result', views.SSLyzeScanResultAPIView.as_view()),
]
