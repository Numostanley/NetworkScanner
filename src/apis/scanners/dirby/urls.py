from django.urls import path

from apis.scanners.dirby import views


app_name = "dirby"

urlpatterns = [
    # dirby urls
    path('scan', views.DirByScannerAPIView.as_view(), name='scan'),
    path('get-result', views.DirByScanResultAPIView.as_view(), name='result')
]
