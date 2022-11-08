import json

from django.test import TestCase
from django.urls import reverse

from apis.scanners.hosts.models import Host
from apis.scanners.zap.models import Zap


class ZapScannerTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("zap:scan")}?')
        self.assertEqual(response.status_code, 400)

    def test_api_key_in_query_params(self):
        response = self.client.get(f'{reverse("zap:scan")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("zap:scan")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_api_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("zap:scan")}?host={self.host}&api_key=')
        self.assertEqual(response.status_code, 400)

    def test_zap_scan_is_in_progress(self):
        api_key = '9ipcclp6d52k81s2rau95kpm57'
        response = self.client.get(f'{reverse("zap:scan")}?host={self.host}&api_key={api_key}')
        self.assertEqual(response.status_code, 200)


class ZapScanResultTest(TestCase):

    def setUp(self) -> None:
        with open('fixtures/zap.json') as f:
            data = json.load(f)

        self.create_host_with_scan_results = Host.create_host('193.122.67.133')
        self.create_host_with_no_scan_results = Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.67.133')
        self.found_host_with_no_result = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_zap_scan = Zap.create_zap_scan(self.found_host_with_result, data[0]['fields']['data'])

        self.get_zap_scan_with_result = Zap.get_zap_scan_by_host(self.found_host_with_result)
        self.get_zap_scan_with_no_result = Zap.get_zap_scan_by_host(self.found_host_with_no_result)

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("zap:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("zap:result")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(f'{reverse("zap:result")}?host={self.not_found_host}')
        self.assertEqual(response.status_code, 404)

    def test_zap_scan_result_does_not_exist_for_host(self):
        response = self.client.get(f'{reverse("zap:result")}?host={self.found_host_with_no_result}')
        self.assertEqual(response.status_code, 404)

    def test_zap_scan_result_exist_for_host(self):
        response = self.client.get(f'{reverse("zap:result")}?host={self.found_host_with_result}')
        self.assertEqual(response.status_code, 200)
