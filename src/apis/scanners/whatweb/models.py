from django.db import models
from django.utils.timezone import now

from apis.scanners.hosts.models import Host


class WhatWeb(models.Model):
    host = models.ForeignKey(Host, related_name='whatweb', on_delete=models.CASCADE)

    data = models.JSONField(default=dict)
    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_whatweb_scan(host: Host, data: list):
        """create a whatweb scan result"""
        return WhatWeb.objects.create(
            host=host,
            data={"data": data}
        )

    @staticmethod
    def get_whatweb_scan_by_id(id):
        """retrieve whatweb scan by id"""
        try:
            return WhatWeb.objects.get(id=id)
        except WhatWeb.DoesNotExist:
            return None

    @staticmethod
    def get_whatweb_scan_by_host(host: Host):
        """retrieve whatweb scans in reverse chronological order"""
        return WhatWeb.objects.filter(host=host).values().order_by('-date_created')

    def __str__(self):
        return f'{self.host.ip_address}'
