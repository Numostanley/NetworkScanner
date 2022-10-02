from django.urls import path
from .views import cvescanner, sslyze, wapiti


urlpatterns = [
    path('cves_can', cvescanner.CVEScannerAPI.as_view(), name="cvescan"),
    path('sslyze_scan', sslyze.SslyzeAPIView.as_view(), name="sslyze_scan"),
    path('wapiti_scan', wapiti.WapitiAPIView.as_view(), name="wapiti_scan"),
    
]
