from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from .models import DirBy


class DirbyTest(TestCase):




    # def setUp(self) -> None:
    #     host = Host.create_host(ip_address='193.122.66.53')

    def test_dirby_scanner_api_view(self):
        response = self.client.get(f'{BASE_URL}/dirby/scan?ip_address=193.122.67.133')
        self.assertEqual(response.status_code, 200)

    def test_dirby_scan_result_api_view(self):
        ip_address = '193.122.67.133'

        response_400 = self.client.get(f'{BASE_URL}/dirby/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        host = Host.get_host(ip_address)
        self.assertIsNone(host)
        # self.assertIsNotNone(host)

        # response = self.client.get(f'{BASE_URL}/dirby/get-result?ip_address={ip_address}')
        # self.assertEqual(response.status_code, 200)
