from django.db import models
from django.utils.timezone import now


class IPAddress(models.Model):
    ip_address = models.CharField(max_length=150, unique=True, db_index=True)
    host_name = models.CharField(max_length=200)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_ip_address(ip_address: str):
        IPAddress.objects.create(ip_address=ip_address).save()

    def __str__(self):
        return f'{self.ip_address}'
