from django.db import models
from django.utils.timezone import now


class IPAddress(models.Model):
    ip_address = models.CharField(max_length=150, unique=True, db_index=True)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_ip_address(ip_address: str):
        IPAddress.objects.create(ip_address=ip_address).save()

    def __str__(self):
        return f'{self.ip_address}'


class CVEScannerV2(models.Model):
    ip_address = models.OneToOneField(IPAddress, related_name='cvescannerv2', on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_cvescanner_scan(ip_scanner: IPAddress):
        pass

    def __str__(self):
        return f'{self.ip_address.ip_address}'


class DirBy(models.Model):
    ip_address = models.OneToOneField(IPAddress, related_name='dirby', on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_dirby_scan(ip_scanner: IPAddress):
        pass

    def __str__(self):
        return f'{self.ip_address.ip_address}'


class SSLyze(models.Model):
    ip_address = models.OneToOneField(IPAddress, related_name='sslyze', on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_sslyze_scan(ip_scanner: IPAddress):
        pass

    def __str__(self):
        return f'{self.ip_address.ip_address}'


class WafWoof(models.Model):
    ip_address = models.OneToOneField(IPAddress, related_name='wafwoof', on_delete=models.CASCADE)

    detected = models.BooleanField(default=False)
    firewall = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=150)
    url = models.URLField()

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_wafwoof_scan(ip_scanner: IPAddress):
        pass

    def __str__(self):
        return f'{self.ip_address.ip_address}'


class Wapiti(models.Model):
    ip_address = models.OneToOneField(IPAddress, related_name='wapiti', on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_wapiti_scan(ip_scanner: IPAddress):
        pass

    def __str__(self):
        return f'{self.ip_address.ip_address}'


class WhatWeb(models.Model):
    ip_address = models.OneToOneField(IPAddress, related_name='whatweb', on_delete=models.CASCADE)

    target = models.URLField()
    plugins = models.JSONField(default=dict)

    date_created = models.DateTimeField(default=now)

    @staticmethod
    def create_whatweb_scan(ip_scanner: IPAddress, data):
        target = data[0]['target']
        plugins = data[0]['plugins']

    def __str__(self):
        return f'{self.ip_address.ip_address}'
