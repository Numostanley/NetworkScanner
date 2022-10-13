import json

from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from .models import WafWoof


class WafW00fTest(TestCase):
    found_ip_addr = '193.122.75.144'
    not_found_ip_addr = '122.121.33.45'

    def setUp(self) -> None:
        with open('fixtures/wafw00f.json', 'r') as f:
           data = json.load(f)

        self.found_host = Host.create_host(ip_address=self.found_ip_addr)
        self.not_found_host = Host.get_host(self.not_found_ip_addr)
        for datum in data:
            WafWoof.create_wafwoof_scan(self.found_host, datum)
        self.get_wafw00f_scan_result = WafWoof.get_wafw00f_scan_by_ip_address(host=self.found_host)

    # def test_wafw00f_creation(self):
    #     self.assertIsInstance(self.create_wafw00f_scan, WafWoof)

    def test_wafw00f_scanner(self):
        no_ip_address_key = self.client.get(f'{BASE_URL}/wafwoof/scan?')
        self.assertEqual(no_ip_address_key.status_code, 400)

        response_400 = self.client.get(f'{BASE_URL}/wafwoof/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        response_200 = self.client.get(f'{BASE_URL}/wafwoof/scan?ip_address=193.122.75.144')
        self.assertEqual(response_200.status_code, 200)

    def test_wafw00f_scan_result(self):
        # test if ip_address key is in query parameters
        no_ip_address_key = self.client.get(f'{BASE_URL}/wafwoof/get-result?')
        self.assertEqual(no_ip_address_key.status_code, 400)

        # test if ip_address key has a value
        response_400 = self.client.get(f'{BASE_URL}/wafwoof/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        # test if the host is not found
        self.assertIsNone(self.not_found_host)

        # test if the host is found
        self.assertIsNotNone(self.found_host)

        not_found_host_response = self.client.get(
            f'{BASE_URL}/wafwoof/get-result?ip_address={self.not_found_ip_addr}'
        )
        self.assertEqual(not_found_host_response.status_code, 404)

        response = self.client.get(f'{BASE_URL}/wafwoof/get-result?ip_address={self.found_host.ip_address}')

        if self.get_wafw00f_scan_result.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.get_wafw00f_scan_result.count() > 0:
            self.assertEqual(response.status_code, 200)
