from django.urls import path

from apis.scanners.screenshot import views


app_name = "screenshot"

urlpatterns = [
    path('scan', views.ScreenShotScannerAPIView.as_view(), name='scan'),
    path('get-result', views.ScreenShotScanResultAPIView.as_view(), name='result'),
]
