from django.urls import path

from apis.scanners.sslyze import views


urlpatterns = [
    # sslyze urls
    path('scan', views.SslyzeScannerAPIView.as_view()),
    path('get-result', views.SSLyzeScanResultAPIView.as_view()),
]
