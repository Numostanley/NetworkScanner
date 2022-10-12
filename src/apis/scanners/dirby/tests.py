from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from .models import DirBy


class DirbyTest(TestCase):
    fixtures = {}

    def setUp(self) -> None:
        self.host = Host.create_host(ip_address='193.122.66.53')
        self.none_host = Host.get_host('122.121.33.45')
        self.dirby_scan = DirBy.get_dirby_scan_by_ip_address(host=self.host)
        self.create_dirby_scan = DirBy.create_dirby_scan(self.host, self.fixtures)

    def test_dirby_creation(self):
        self.assertIsInstance(self.create_dirby_scan, DirBy)

    def test_dirby_scanner(self):
        response_400 = self.client.get(f'{BASE_URL}/dirby/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        response_200 = self.client.get(f'{BASE_URL}/dirby/scan?ip_address=193.122.67.133')
        self.assertEqual(response_200.status_code, 200)

    def test_dirby_scan_result(self):
        response_400 = self.client.get(f'{BASE_URL}/dirby/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        self.assertIsNone(self.none_host)

        found_host = Host.get_host(self.host.ip_address)
        self.assertIsNotNone(found_host)

        response = self.client.get(f'{BASE_URL}/dirby/get-result?ip_address={self.host.ip_address}')

        if self.dirby_scan.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.dirby_scan.count() > 0:
            self.assertEqual(response.status_code, 200)
