from django.contrib import admin


# Register your models here.
from .models import wapiti, base

admin.site.register(base.Host)
admin.site.register(wapiti.Wapiti)


