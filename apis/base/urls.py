from django.urls import path
from .views import CVEScanner, sslyze


urlpatterns = [
    path("", CVEScanner.GetRoutes.as_view()),
    path('cvescan', CVEScanner.CVEScannerAPI.as_view(), name="cvescan"),
    path('sslyze_scan', sslyze.SslyzeAPIView.as_view(), name="sslyze_scan"),
    
]
