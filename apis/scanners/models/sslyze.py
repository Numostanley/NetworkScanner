from django.db import models
from django.utils.timezone import now

from .base import Host


class SSLyze(models.Model):
    host = models.ForeignKey(Host, related_name='sslyze', on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_sslyze_scan(host: Host):
        pass

    def __str__(self):
        return f'{self.host.ip_address}'
