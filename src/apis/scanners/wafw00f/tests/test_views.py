import json

from django.test import TestCase
from django.urls import reverse

from apis.scanners.hosts.models import Host
from apis.scanners.wafw00f.models import WafWoof


class WafW00fScannerTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("wafwoof:scan")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("wafwoof:scan")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_wafw00f_scan_is_in_progress(self):
        response = self.client.get(f'{reverse("wafwoof:scan")}?host={self.host}')
        self.assertEqual(response.status_code, 200)


class WafW00fScanResultTest(TestCase):
    data = """
        [{
            "url": "https://193.122.75.144",
            "detected": false,
            "firewall": "None",
            "manufacturer": "None"
        }]
    """

    def setUp(self) -> None:
        Host.create_host('193.122.75.144')
        Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.75.144')
        self.found_host_with_no_result = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_wafw00f_scan = WafWoof.create_wafwoof_scan(self.found_host_with_result, json.loads(self.data))

        self.get_wafw00f_scan_with_result = WafWoof.get_wafw00f_scan_by_host(self.found_host_with_result)
        self.get_wafw00f_scan_with_no_result = WafWoof.get_wafw00f_scan_by_host(self.found_host_with_no_result)

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("wafwoof:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("wafwoof:result")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(f'{reverse("wafwoof:result")}?host={self.not_found_host}')
        self.assertEqual(response.status_code, 404)

    def test_wafw00f_scan_result_does_not_exist_for_host(self):
        response = self.client.get(f'{reverse("wafwoof:result")}?host={self.found_host_with_no_result}')
        self.assertEqual(response.status_code, 404)

    def test_wafw00f_scan_result_exist_for_host(self):
        response = self.client.get(f'{reverse("wafwoof:result")}?host={self.found_host_with_result}')
        self.assertEqual(response.status_code, 200)