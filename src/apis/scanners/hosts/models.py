from ipaddress import ip_address

from django.db import models
from django.utils.timezone import now


class Host(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unique=True, db_index=True)
    domain_name = models.URLField(default='')

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_host(ip_address: str):
        """save ip address"""
        return Host.objects.create(ip_address=ip_address)

    @staticmethod
    def get_host(host: str):
        """
        params host: a valid ip address or domain name
        return host if found else None
        """
        try:
            try:
                ip_address(host)
                return Host.objects.get(ip_address=host)
            except ValueError:
                return Host.objects.get(domain_name=host)
        except Host.DoesNotExist:
            return None

    def __str__(self):
        return f'{self.ip_address}'
