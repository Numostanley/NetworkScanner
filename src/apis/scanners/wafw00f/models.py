from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host


class WafWoof(models.Model):
    host = models.ForeignKey(Host, related_name='wafwoof', on_delete=models.CASCADE)

    detected = models.BooleanField(default=False)
    firewall = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=150)
    url = models.URLField()

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_wafwoof_scan(host: Host, data: list):
        """create a wafw00f scan result"""
        wafw00f = WafWoof()
        for datum in data:
            wafw00f.host = host
            wafw00f.detected = datum['detected']
            wafw00f.firewall = datum['firewall']
            wafw00f.manufacturer = datum['manufacturer']
            wafw00f.url = datum['url']
        return wafw00f

    @staticmethod
    def get_wafw00f_scan_by_ip_address(host: Host):
        """retrieve wafw00f scans in reverse chronological order"""
        return WafWoof.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
