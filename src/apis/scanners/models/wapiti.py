from django.db import models
from django.utils.timezone import now

from .base import Host


class Wapiti(models.Model):
    host = models.ForeignKey(Host, related_name='wapiti', on_delete=models.CASCADE)
    
    vulnerabilities = models.JSONField(default=dict)
    anomalies = models.JSONField(default=dict)
    infos = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_wapiti_scan(host: Host, data: list):
        """create a wapiti scan result"""
        return Wapiti.objects.create(
            host=host,
            vulnerabilities=data[0],
            anomalies=data[1],
            infos=data[2]
        )
        
    @staticmethod
    def get_wapiti_scan_by_ip_address(host: Host):
        """retrieve wapiti scans in reverse chronological order"""
        return Wapiti.objects.filter(host__ip_address__exact=host).order_by('-date_created').all()

    def __str__(self):
        return f'{self.host.ip_address}'
