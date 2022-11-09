from django.urls import path

from apis.scanners.cvescannerv2 import views


app_name = "cvescannerv2"

urlpatterns = [
    # cvescannerv2 urls
    path('scan', views.CVEScannerAPIView.as_view(), name='scan'),
    path('get-result', views.CVEScanResultAPIView.as_view(), name='result'),
]
