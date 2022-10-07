from django.urls import path

from apis.scanners.wafw00f import views


urlpatterns = [
    # wafwoof urls
    path('scan', views.WafWoofScannerAPIView.as_view()),
]
