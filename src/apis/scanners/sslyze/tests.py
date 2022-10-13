from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
import json
from .models import SSLyze


class SslyzeTest(TestCase):
    
    def setUp(self):
        
        self.host = Host.create_host(ip_address='193.122.67.133')
        self.none_host = Host.get_host('122.121.33.45')
        with open('fixtures/sslyze.json', 'r') as f:
           data = json.load(f)
           
        for datum in data:
            SSLyze.create_sslyze_scan(host=self.host, data=datum['fields'])
        self.sslyze_scan = SSLyze.get_sslyze_scan_by_ip_address(host=self.host)
        

    def test_sslyze(self):
        view = self.client.get(f'{BASE_URL}/sslyze/scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/sslyze/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)

    
    def test_scan_result(self):
        self.assertIsNone(self.none_host)
        
        found_host = Host.get_host(self.host.ip_address)
        self.assertIsNotNone(found_host)
        
        response = self.client.get(f'{BASE_URL}/sslyze/get-result?ip_address=193.122.67.133')
        if self.sslyze_scan.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.sslyze_scan.count() > 0:
            self.assertEqual(response.status_code, 200)
        
        query_params = response.request['QUERY_STRING']
        check = 'ip_address' in query_params
        response_400 = self.client.get(f'{BASE_URL}/sslyze/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)
        self.assertEqual(check, True)
        
    def test_model_field_type(self):
        sslyze = SSLyze.objects.get(id=1)
        
        connectivity_result= sslyze._meta.get_field('connectivity_result').get_internal_type()
        network_configuration= sslyze._meta.get_field('network_configuration').get_internal_type()
        scan_result= sslyze._meta.get_field('scan_result').get_internal_type()
        self.assertEqual(connectivity_result, 'JSONField')
        self.assertEqual(network_configuration, 'JSONField')
        self.assertEqual(scan_result, 'JSONField')
        
        