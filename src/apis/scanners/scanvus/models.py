from email.policy import default
from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host

# Create your models here.

class Scanvus(models.Model):
    host = models.ForeignKey(Host, related_name='scanvus', on_delete=models.CASCADE)
    
    data = models.JSONField(default=dict)
    
    date_created = models.DateTimeField(default=now)
    
    @staticmethod
    def create_scanvus_scan(host: Host, data: dict):
        """create a scanvus scan result"""
        return Scanvus.objects.create(
            host=host,
            data=data
        )
        
    @staticmethod
    def get_scanvus_scan_by_id(id):
        """retrieve scanvus scan by id"""
        try:
            return Scanvus.objects.get(id=id)
        except Scanvus.DoesNotExist:
            return None
        
    @staticmethod
    def get_scanvus_scan_by_host(host: Host):
        """retrieve scanvus scans in reverse chronological order"""
        return Scanvus.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
    
    