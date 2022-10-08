from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host


class CVEScannerV2(models.Model):
    host = models.ForeignKey(Host, related_name='cvescannerv2', on_delete=models.CASCADE)

    cve_data = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_cvescanner_scan(host: Host, data: list):
        """create a cvescanner scan result"""

        CVEScannerV2.objects.create(
            host=host,
            cve_data={"cve_data":data}
        )

    @staticmethod
    def get_cvescanner_by_host(host: Host):
        """retrieve cvescanner scans in reverse chronological order"""
        return CVEScannerV2.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
