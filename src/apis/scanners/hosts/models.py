from ipaddress import ip_address

from django.db import models
from django.utils.timezone import now


class Host(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unique=True, db_index=True, null=True)
    domain_name = models.URLField(default='')

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_host(host: str):
        """save ip address"""
        try:
            # check if host is a valid IPv4/IPv6 address, then save to the ip_address field
            ip_address(host)
            return Host.objects.create(ip_address=host)
        except ValueError:
            # if host is not a valid IPv4/IPv6 address, save to the domain_name field
            return Host.objects.create(domain_name=host)

    @staticmethod
    def get_host(host: str):
        """
        params host: a valid ip address or domain name
        return host if found else None
        """
        try:
            try:
                # check if host is a valid IPv4/IPv6 address, then retrieve from the ip_address field
                ip_address(host)
                return Host.objects.get(ip_address=host)
            except ValueError:
                # if host is not a valid IPv4/IPv6 address, retrieve from the domain_name field
                return Host.objects.get(domain_name=host)
        except Host.DoesNotExist:
            return None

    def __str__(self):
        return f'{self.ip_address}'
