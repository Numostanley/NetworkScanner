from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from .models import WhatWeb


class WhatWebTest(TestCase):
    fixtures = []

    def setUp(self) -> None:
        self.host = Host.create_host(ip_address='193.122.66.53')
        self.none_host = Host.get_host('122.121.33.45')
        self.whatweb_scan = WhatWeb.get_whatweb_scan_by_ip_addr(host=self.host)
        self.create_whatweb_scan = WhatWeb.create_whatweb_scan(self.host, self.fixtures)

    def test_whatweb_creation(self):
        self.assertTrue(isinstance(self.create_whatweb_scan, WhatWeb))

    def test_whatweb_scanner(self):
        response_400 = self.client.get(f'{BASE_URL}/whatweb/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        response_200 = self.client.get(f'{BASE_URL}/whatweb/scan?ip_address=193.122.67.133')
        self.assertEqual(response_200.status_code, 200)

    def test_whatweb_scan_result(self):
        response_400 = self.client.get(f'{BASE_URL}/whatweb/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        self.assertIsNone(self.none_host)

        found_host = Host.get_host(self.host.ip_address)
        self.assertIsNotNone(found_host)

        response = self.client.get(f'{BASE_URL}/wafwoof/get-result?ip_address={self.host.ip_address}')

        if self.whatweb_scan.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.whatweb_scan.count() > 0:
            self.assertEqual(response.status_code, 200)
            
            