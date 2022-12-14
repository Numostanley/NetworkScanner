"""VulnScan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core.settings import base
from core.routers.api_versioning import get_api_version


# admin urls

admin_urls = [
    path('admin/', admin.site.urls),
]

# api urls
api_urls = [
    path('scanners/', include(([
        path('cvescannerv2/', include('apis.scanners.cvescannerv2.urls', namespace='cvescannerv2')),
        path('dirby/', include('apis.scanners.dirby.urls', namespace='dirby')),
        path('scanvus/', include('apis.scanners.scanvus.urls', namespace='scanvus')),
        path('screenshot/', include('apis.scanners.screenshot.urls', namespace='screenshot')),
        path('sslyze/', include('apis.scanners.sslyze.urls', namespace='sslyze')),
        path('wafwoof/', include('apis.scanners.wafw00f.urls', namespace='wafwoof')),
        path('wapiti/', include('apis.scanners.wapiti.urls', namespace='wapiti')),
        path('whatweb/', include('apis.scanners.whatweb.urls', namespace='whatweb')),
        path('zap/', include('apis.scanners.zap.urls', namespace='zap'))
    ]))),
]

api_version_one = get_api_version(base.API_VERSIONS, 'v1')

# append API prefix and version to all url patterns
if base.API_PREFIX:
    api_urls = [
        path(f'{base.API_PREFIX}/{api_version_one}/', include(api_urls))
    ]

urlpatterns = api_urls + admin_urls
