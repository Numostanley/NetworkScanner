from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host


class CVEScannerV2(models.Model):
    host = models.ForeignKey(Host, related_name='cvescannerv2', on_delete=models.CASCADE)

    cve_data = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_cvescanner_scan(host: Host, data: list):
        """create a cvescannerv2 scan result"""
        return CVEScannerV2.objects.create(
            host=host,
            cve_data={"cve_data": data}
        )

    @staticmethod
    def get_cvescannerv2_scan_by_id(id):
        """retrieve cvescanenerv2 scan by id"""
        try:
            return CVEScannerV2.objects.get(id=id)
        except CVEScannerV2.DoesNotExist:
            return None

    @staticmethod
    def get_cvescannerv2_by_host(host: Host):
        """retrieve cvescannerv2 scans in reverse chronological order"""
        return CVEScannerV2.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
