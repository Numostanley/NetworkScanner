from django.db import models
from django.utils.timezone import now

from .base import IPAddress


class WhatWeb(models.Model):
    ip_address = models.ForeignKey(IPAddress, related_name='whatweb', on_delete=models.CASCADE)

    data = models.JSONField(default=dict)
    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_whatweb_scan(ip_address: IPAddress, data: list):
        """create a whatweb scan result"""
        return WhatWeb.objects.create(
            ip_address=ip_address,
            data=data[0]
        )

    @staticmethod
    def get_whatweb_scan_by_ip_addr(ip_address: IPAddress):
        """retrieve whatweb scans in reverse chronological order"""
        return WhatWeb.objects.filter(ip_address__ip_address__exact=ip_address).order_by('-date_created').al()

    def __str__(self):
        return f'{self.ip_address.ip_address}'
