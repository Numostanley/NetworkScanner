from django.db import models
from django.utils.timezone import now

from .base import Host


class SSLyze(models.Model):
    host = models.ForeignKey(Host, related_name='sslyze', on_delete=models.CASCADE)
    
    connection_type = models.CharField(max_length=10)
    connectivity_error_trace = models.CharField(max_length=10)
    connectivity_result = models.JSONField(default=dict)
    connectivity_status = models.CharField(max_length=20)
    date_scans_completed = models.DateTimeField()
    date_scans_started = models.DateTimeField()
    network_configuration = models.JSONField(default=dict)
    port = models.IntegerField()
    scan_result = models.JSONField(default=dict)
    scan_status = models.CharField(max_length=20)
    uuid = models.CharField(max_length=30)
    
    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_sslyze_scan(host: Host, data: dict):
        """create an sslyze scan result"""
        return SSLyze.objects.create(
            host=host,
            connection_type=data['connection_type'],
            connectivity_error_trace=data['connectivity_error_trace'],
            connectivity_result=data['connectivity_result'],
            connectivity_status=data['connectivity_status'],
            date_scans_completed=data['date_scans_completed'],
            date_scans_started=data['date_scans_started'],
            port=data['port'],
            scan_result=data['scan_result'],
            scan_status=data['scan_status'],
            uuid=data['uuid']
        )
        
    @staticmethod
    def get_sslyze_scan_by_ip_address(host: Host):
        """retrieve sslyze scans in reverse chronological order"""
        return SSLyze.objects.filter(host__ip_address__exact=host).order_by('-date_created').all()

    def __str__(self):
        return f'{self.host.ip_address}'
