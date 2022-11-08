import json

from django.test import TestCase
from django.urls import reverse

from apis.scanners.hosts.models import Host
from apis.scanners.whatweb.models import WhatWeb


class WhatWebScannerTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("whatweb:scan")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("whatweb:scan")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_whatweb_scan_is_in_progress(self):
        response = self.client.get(f'{reverse("whatweb:scan")}?host={self.host}')
        self.assertEqual(response.status_code, 200)


class WhatWebScanResultTest(TestCase):

    def setUp(self) -> None:
        with open('fixtures/whatweb.json', 'r') as f:
           data = json.load(f)

        whatweb_data = []
        for datum in data:
            whatweb_data.append(datum)

        self.create_host_with_scan_results = Host.create_host('193.122.75.144')
        self.create_host_with_no_scan_results = Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.75.144')
        self.found_host_with_no_result = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_whatweb_scan = WhatWeb.create_whatweb_scan(self.found_host_with_result,
                                                               whatweb_data[0]['fields']['data']['data'])

        self.get_whatweb_scan_with_result = WhatWeb.get_whatweb_scan_by_host(self.found_host_with_result)
        self.get_whatweb_scan_with_no_result = WhatWeb.get_whatweb_scan_by_host(self.found_host_with_no_result)

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("whatweb:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("whatweb:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(f'{reverse("whatweb:result")}?host={self.not_found_host}')
        self.assertEqual(response.status_code, 404)

    def test_whatweb_scan_result_does_not_exist_for_host(self):
        response = self.client.get(f'{reverse("whatweb:result")}?host={self.found_host_with_no_result}')
        self.assertEqual(response.status_code, 404)

    def test_whatweb_scan_result_exist_for_host(self):
        response = self.client.get(f'{reverse("whatweb:result")}?host={self.found_host_with_result}')
        self.assertEqual(response.status_code, 200)
