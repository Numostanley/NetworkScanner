from django.urls import path
from . import views


urlpatterns = [
    path("", views.GetRoutes.as_view()),
    path('scan', views.VulnerabilityScanner.as_view(), name="scan"),
]
