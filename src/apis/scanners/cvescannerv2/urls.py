from django.urls import path

from apis.scanners.cvescannerv2 import views


urlpatterns = [
    # cvescanner urls
    path('scan', views.CVEScannerAPIView.as_view()),
    path('get-result', views.CVEScanResultAPIView.as_view()),
]
