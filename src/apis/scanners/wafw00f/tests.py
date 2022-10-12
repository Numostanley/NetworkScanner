import json

from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from .models import WafWoof


class WafW00fTest(TestCase):
    fixtures = ['wafw00f.json']

    def setUp(self) -> None:
        with open(self.fixtures[0], 'r') as f:
           data = json.load(f)

        self.host = Host.create_host(ip_address='193.122.75.144')
        self.none_host = Host.get_host('122.121.33.45')
        self.create_wafw00f_scan = WafWoof.create_wafwoof_scan(self.host, data)
        self.wafw00f_scan = WafWoof.get_wafw00f_scan_by_ip_address(host=self.host)

    def test_wafw00f_creation(self):
        self.assertIsInstance(self.create_wafw00f_scan, WafWoof)

    def test_wafw00f_scanner(self):
        response_400 = self.client.get(f'{BASE_URL}/wafwoof/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        response_200 = self.client.get(f'{BASE_URL}/wafwoof/scan?ip_address=193.122.75.144')
        self.assertEqual(response_200.status_code, 200)

    def test_wafw00f_scan_result(self):
        response_400 = self.client.get(f'{BASE_URL}/wafwoof/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        self.assertIsNone(self.none_host)

        found_host = Host.get_host(self.host.ip_address)
        self.assertIsNotNone(found_host)

        response = self.client.get(f'{BASE_URL}/wafwoof/get-result?ip_address={self.host.ip_address}')

        if self.wafw00f_scan.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.wafw00f_scan.count() > 0:
            self.assertEqual(response.status_code, 200)
