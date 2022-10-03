from django.db import models
from django.utils.timezone import now

from .base import Host


class DirBy(models.Model):
    host = models.ForeignKey(Host, related_name='dirby', on_delete=models.CASCADE)

    base_url = models.URLField()
    port = models.IntegerField()
    report = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_dirby_scan(host: Host, data: dict):
        """create a dirby scan result"""
        return DirBy.objects.create(
            host=host,
            base_url=data['base_url'],
            port=data['port'],
            report=data['report']
        )

    @staticmethod
    def get_dirby_scan_by_ip_address(host: Host):
        """retrieve dirby scans in reverse chronological order"""
        return DirBy.objects.filter(host__ip_address__exact=host).order_by('-date_created').all()

    def __str__(self):
        return f'{self.host.ip_address}'
