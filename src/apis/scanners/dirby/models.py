from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host


class DirBy(models.Model):
    host = models.ForeignKey(Host, related_name='dirby', on_delete=models.CASCADE)

    data = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_dirby_scan(host: Host, data: dict):
        """create a dirby scan result"""
        return DirBy.objects.create(
            host=host,
            data=data
        )

    @staticmethod
    def get_dirby_scan_by_id(id):
        """retrieve dirby scan by id"""
        try:
            return DirBy.objects.get(id=id)
        except DirBy.DoesNotExist:
            return None

    @staticmethod
    def get_dirby_scan_by_host(host: Host):
        """retrieve dirby scans in reverse chronological order"""
        return DirBy.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
