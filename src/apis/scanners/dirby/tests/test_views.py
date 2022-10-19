from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
from apis.scanners.dirby.models import DirBy


class DirbyScannerTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/dirby/scan?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/dirby/scan?host=')
        self.assertEqual(response.status_code, 400)

    def test_dirby_scan_is_in_progress(self):
        response = self.client.get(f'{BASE_URL}/dirby/scan?host={self.host}')
        self.assertEqual(response.status_code, 200)


class DirbyScanResultTest(TestCase):

    def setUp(self) -> None:
        dirby_data = {}

        self.create_host_with_scan_results = Host.create_host('193.122.75.144')
        self.create_host_with_no_scan_results = Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.75.144')
        self.found_host_with_no_result_scan = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_dirby_scan = DirBy.create_dirby_scan(self.found_host_with_result, dirby_data)

        self.get_dirby_scan_with_result = DirBy.get_dirby_scan_by_host(self.found_host_with_result)
        self.get_dirby_scan_with_no_result = DirBy.get_dirby_scan_by_host(self.found_host_with_no_result_scan)

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/dirby/get-result?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{BASE_URL}/dirby/get-result?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(
            f'{BASE_URL}/dirby/get-result?host={self.not_found_host}'
        )
        self.assertEqual(response.status_code, 404)

    def test_dirby_scan_result_does_not_exist_for_host(self):
        response = self.client.get(
            f'{BASE_URL}/dirby/get-result?host={self.found_host_with_no_result_scan}'
        )
        self.assertEqual(response.status_code, 404)

    def test_dirby_scan_result_exist_for_host(self):
        response = self.client.get(
            f'{BASE_URL}/dirby/get-result?host={self.found_host_with_result}'
        )
        self.assertEqual(response.status_code, 200)
