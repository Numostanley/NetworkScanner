import json

from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from apis.scanners.wapiti.models import Wapiti


class WapitiScannerTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/wapiti/scan?')
        self.assertEqual(response.status_code, 400)

    def test_host_value_not_specified_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/wapiti/scan?host=')
        self.assertEqual(response.status_code, 400)

    def test_wapiti_scan_is_in_progress(self):
        response = self.client.get(f'{BASE_URL}/wapiti/scan?host={self.host}')
        self.assertEqual(response.status_code, 200)


class WapitiScanResultTest(TestCase):
    
    def setUp(self) -> None:
        with open('fixtures/wapiti.json', 'r') as f:
            data = json.load(f)

        wapiti_data = []
        for datum in data:
            wapiti_data.append(datum)

        wapiti_data_list = [
            wapiti_data[0]['fields']['vulnerabilities'],
            wapiti_data[0]['fields']['anomalies'],
            wapiti_data[0]['fields']['infos']
        ]

        self.create_host_with_scan_results = Host.create_host('193.122.75.144')
        self.create_host_with_no_scan_results = Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.75.144')
        self.found_host_with_no_result_scan = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_wapiti_scan = Wapiti.create_wapiti_scan(self.found_host_with_result, wapiti_data_list)

        self.get_wapiti_scan_with_result = Wapiti.get_wapiti_scan_by_host(self.found_host_with_result)
        self.get_wapiti_scan_with_no_result = Wapiti.get_wapiti_scan_by_host(self.found_host_with_no_result_scan)
    
    def test_host_key_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/wapiti/get-result?')
        self.assertEqual(response.status_code, 400)

    def test_host_value_not_specified_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/wapiti/get-result?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(
            f'{BASE_URL}/wapiti/get-result?host={self.not_found_host}'
        )
        self.assertEqual(response.status_code, 404)

    def test_wapiti_scan_result_does_not_exist_for_host(self):
        response = self.client.get(
            f'{BASE_URL}/wapiti/get-result?host={self.found_host_with_no_result_scan}'
        )
        self.assertEqual(response.status_code, 404)

    def test_wapiti_scan_result_exist_for_host(self):
        response = self.client.get(
            f'{BASE_URL}/wapiti/get-result?host={self.found_host_with_result}'
        )
        self.assertEqual(response.status_code, 200)
