from django.db import models
from django.utils.timezone import now

from .base import IPAddress


class Wapiti(models.Model):
    ip_address = models.ForeignKey(IPAddress, related_name='wapiti', on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_wapiti_scan(ip_scanner: IPAddress):
        pass

    def __str__(self):
        return f'{self.ip_address.ip_address}'
