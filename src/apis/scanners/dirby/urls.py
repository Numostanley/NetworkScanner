from django.urls import path

from apis.scanners.dirby import views


urlpatterns = [
    # dirby urls
    path('scan', views.DirByScannerAPIView.as_view()),
]
