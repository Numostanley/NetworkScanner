import json

from django.test import TestCase
from django.urls import reverse

from apis.scanners.hosts.models import Host
from apis.scanners.scanvus.models import Scanvus


class ScanvusScannerTest(TestCase):
    
    def setUp(self) -> None:
        self.host = '3.101.140.30'
        self.username = 'ubuntu'
        self.password = 'Numonde@1'
        
    def test_credential_keys_in_query_params(self):
        response = self.client.get(f'{reverse("scanvus:scan")}?')
        self.assertEqual(response.status_code, 400)
        
    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("scanvus:scan")}?host=&username={self.username}&password={self.password}')
        self.assertEqual(response.status_code, 400)

    def test_username_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("scanvus:scan")}?host={self.host}&username=&password={self.password}')
        self.assertEqual(response.status_code, 400)
        
    def test_password_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("scanvus:scan")}?host={self.host}&username={self.username}&password=')
        self.assertEqual(response.status_code, 400)
        
    def test_scanvus_scan_is_in_progress(self):
        response = self.client.get(f'{reverse("scanvus:scan")}?host={self.host}&username={self.username}&password={self.password}')
        self.assertEqual(response.status_code, 200)
        

class ScanvusScanResultTest(TestCase):

    def setUp(self) -> None:
        with open('fixtures/scanvus.json', 'r') as f:
           data = json.load(f)

        scanvus_data = []
        for datum in data:
            scanvus_data.append(datum)

        Host.create_host('3.101.140.30')
        Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('3.101.140.30')
        self.found_host_with_no_result = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('122.121.33.45')

        self.create_scanvus_scan = Scanvus.create_scanvus_scan(self.found_host_with_result, scanvus_data[0]['fields'])

        self.get_scanvus_scan_with_result = Scanvus.get_scanvus_scan_by_host(self.found_host_with_result)
        self.get_scanvus_scan_with_no_result = Scanvus.get_scanvus_scan_by_host(self.found_host_with_no_result)

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("scanvus:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("scanvus:result")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(f'{reverse("scanvus:result")}?host={self.not_found_host}')
        self.assertEqual(response.status_code, 404)
        
    def test_scanvus_scan_result_does_not_exist_for_host(self):
        response = self.client.get(f'{reverse("scanvus:result")}?host={self.found_host_with_no_result}')
        self.assertEqual(response.status_code, 404)
        
    def test_scanvus_scan_result_exist_for_host(self):
        response = self.client.get(f'{reverse("scanvus:result")}?host={self.found_host_with_result}')
        self.assertEqual(response.status_code, 200)
