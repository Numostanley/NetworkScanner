from django.db import models
from django.utils.timezone import now

from .base import Host


class CVEScannerV2(models.Model):
    host = models.ForeignKey(Host, related_name='cvescannerv2', on_delete=models.CASCADE)

    port = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    service = models.CharField(max_length=20)
    version = models.CharField(max_length=100)

    cves = models.CharField(max_length=20)
    cve_data = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_cvescanner_scan(host: Host, data: list):
        """create a cvescanner scan result"""
        
        for datum in data:
            cvescanner = CVEScannerV2()
            
            cvescanner.host = host
            cvescanner.port= datum['port']
            cvescanner.state = datum['state']
            cvescanner.service = datum['service-name']
            cvescanner.version = datum['version']
            cvescanner.cves = datum['cves']
            cvescanner.cve_data = datum['CVE_Data']

            cvescanner.save()
            
        return cvescanner

    @staticmethod
    def get_cvescanner_by_host(host: Host):
        """retrieve cvescanner scans in reverse chronological order"""
        return CVEScannerV2.objects.filter(host__ip_address__exact=host).order_by('-date_created').all()

    def __str__(self):
        return f'{self.host.ip_address}'
