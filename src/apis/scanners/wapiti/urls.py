from django.urls import path

from apis.scanners.wapiti import views


urlpatterns = [
    # wapiti urls
    path('scan', views.WapitiScannerAPIView.as_view()),
    path('get-result', views.WapitiScanResultAPIView.as_view())
]