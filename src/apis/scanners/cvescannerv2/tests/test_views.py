import json

from django.test import TestCase
from django.urls import reverse

from apis.scanners.hosts.models import Host
from apis.scanners.cvescannerv2.models import CVEScannerV2


class CVEScannerv2Test(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("cvescannerv2:scan")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("cvescannerv2:scan")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_cvescannerv2_scan_is_in_progress(self):
        response = self.client.get(f'{reverse("cvescannerv2:scan")}?host={self.host}')
        self.assertEqual(response.status_code, 200)


class CVEScannerv2ScanResultTest(TestCase):

    def setUp(self) -> None:
        with open('fixtures/cvescannerv2.json', 'r') as f:
           data = json.load(f)

        cvescannerv2_data = []
        for datum in data:
            cvescannerv2_data.append(datum)

        Host.create_host('193.122.75.144')
        Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.75.144')
        self.found_host_with_no_result_scan = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_cvescannerv2_scan = CVEScannerV2.create_cvescanner_scan(self.found_host_with_result,
                                                               cvescannerv2_data[0]['fields']['cve_data']['cve_data'])

        self.get_cvescannerv2_scan_with_result = CVEScannerV2.get_cvescannerv2_by_host(self.found_host_with_result)
        self.get_cvescannerv2_scan_with_no_result = CVEScannerV2.get_cvescannerv2_by_host(self.found_host_with_no_result_scan)

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("cvescannerv2:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("cvescannerv2:result")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(f'{reverse("cvescannerv2:result")}?host={self.not_found_host}')
        self.assertEqual(response.status_code, 404)

    def test_cvescannerv2_scan_result_does_not_exist_for_host(self):
        response = self.client.get(f'{reverse("cvescannerv2:result")}?host={self.found_host_with_no_result_scan}')
        self.assertEqual(response.status_code, 404)

    def test_cvescannerv2_scan_result_exist_for_host(self):
        response = self.client.get(f'{reverse("cvescannerv2:result")}?host={self.found_host_with_result}')
        self.assertEqual(response.status_code, 200)
