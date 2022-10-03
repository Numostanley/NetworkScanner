from django.db import models
from django.utils.timezone import now

from .base import IPAddress


class DirBy(models.Model):
    ip_address = models.ForeignKey(IPAddress, related_name='dirby', on_delete=models.CASCADE)

    base_url = models.URLField()
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    report = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_dirby_scan(ip_address: IPAddress, data: dict):
        """create a dirby scan result"""
        return DirBy.objects.create(
            ip_address=ip_address,
            base_url=data['base_url'],
            host=data['host'],
            port=data['port'],
            report=data['report']
        )

    @staticmethod
    def get_dirby_scan_by_ip_address(ip_address: IPAddress):
        """retrieve dirby scans in reverse chronological order"""
        return DirBy.objects.filter(ip_address__ip_address__exact=ip_address).order_by('-date_created').all()

    def __str__(self):
        return f'{self.ip_address.ip_address}'
