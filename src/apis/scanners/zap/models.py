from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host

# Create your models here.

class Zap(models.Model):
    host = models.ForeignKey(Host, related_name='zap', on_delete=models.CASCADE)
    
    data = models.JSONField(default=dict)
    
    date_created = models.DateTimeField(default=now)
    
    @staticmethod
    def create_zap_scan(host: Host, data: dict):
        """create a zap scan result"""
        return Zap.objects.create(
            host=host,
            data=data
        )
        
    @staticmethod
    def get_zap_scan_by_id(id):
        """retrieve zap scan by id"""
        try:
            return Zap.objects.get(id=id)
        except Zap.DoesNotExist:
            return None
        
    @staticmethod
    def get_zap_scan_by_host(host: Host):
        """retrieve zap scans in reverse chronological order"""
        return Zap.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
    