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
    cveid = models.CharField(max_length=50)
    cvssv2 = models.CharField(max_length=20)
    cvssv3 = models.CharField(max_length=20)

    exploit_db = models.CharField(max_length=10)
    metasploit = models.CharField(max_length=10)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_cvescanner_scan(host: Host, data: list):
        """create a cvescanner scan result"""
        cvescanner = CVEScannerV2()
        for datum in data:
            cvescanner.host = host
            cvescanner.port= datum['port']
            cvescanner.state = datum['state']
            cvescanner.service = datum['service']
            cvescanner.version = datum['version']
            cvescanner.cves = datum['cves']
            cvescanner.cveid = datum['cveid']
            cvescanner.cvssv2 = datum['cvssv2']
            cvescanner.cvssv3 = datum['cvssv3']
            cvescanner.exploit_db = datum['exploit_db']
            cvescanner.metasploit = datum['metasploit']
        return cvescanner

    @staticmethod
    def get_cvescanner_by_host(host: Host):
        """retrieve cvescanner scans in reverse chronological order"""
        return CVEScannerV2.objects.filter(host__ip_address__exact=host).order_by('-date_created').all()

    def __str__(self):
        return f'{self.host.ip_address}'
