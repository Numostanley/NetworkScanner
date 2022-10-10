from django.db import models
from django.utils.timezone import now


class Host(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unique=True, db_index=True)
    host_name = models.URLField(default='')

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_host(ip_address: str):
        """save ip address"""
        return Host.objects.create(ip_address=ip_address)

    @staticmethod
    def get_host(ip_address: str):
        """return host if found else None"""
        try:
            return Host.objects.get(ip_address=ip_address)
        except Host.DoesNotExist:
            return None

    def __str__(self):
        return f'{self.ip_address}'
