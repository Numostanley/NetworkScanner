from django.contrib import admin


# Register your models here.
from .models import wapiti, base, sslyze, cvescanner

admin.site.register(base.Host)
admin.site.register(wapiti.Wapiti)
admin.site.register(sslyze.SSLyze)
admin.site.register(cvescanner.CVEScannerV2)



