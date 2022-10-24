from django.urls import path

from apis.scanners.scanvus import views


urlpatterns = [
    # scanvus urls
    path('scan', views.ScanvusScannerAPIView.as_view()),
    path('get-result', views.ScanvusScanResultAPIView.as_view())
]
