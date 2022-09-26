from django.urls import path

from . import views


urlpatterns = [
    path('download', views.DownloadScanReportAPIView.as_view()),
    path('scan-ip', views.ScanIPAPIView.as_view()),
]
