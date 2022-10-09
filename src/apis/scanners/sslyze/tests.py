from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
import json
from .models import SSLyze


class SslyzeTest(TestCase):
    
    def setUp(self):
        
        host = Host.create_host(ip_address='193.122.67.133')
       
        with open('test_db_data/sslyze.json', 'r') as f:
           json_data = f.read()
           
           data = json.loads(json_data)
         
        for datum in data:
            SSLyze.create_sslyze_scan(host=host, data=datum['fields'])

    def test_sslyze(self):
        view = self.client.get(f'{BASE_URL}/sslyze/scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/sslyze/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)

    
    def test_scan_result(self):
        response = self.client.get(f'{BASE_URL}/sslyze/get-result?ip_address=193.122.67.133')
        self.assertEqual(response.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/sslyze/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)
    
        
    def test_model_field_type(self):
        sslyze = SSLyze.objects.get(id=1)
        
        connectivity_result= sslyze._meta.get_field('connectivity_result').get_internal_type()
        network_configuration= sslyze._meta.get_field('network_configuration').get_internal_type()
        scan_result= sslyze._meta.get_field('scan_result').get_internal_type()
        self.assertEqual(connectivity_result, 'JSONField')
        self.assertEqual(network_configuration, 'JSONField')
        self.assertEqual(scan_result, 'JSONField')
        
        