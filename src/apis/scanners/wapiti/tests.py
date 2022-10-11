from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
import json
from .models import Wapiti

class WapitiTest(TestCase):
    # fixtures = 'wapiti.json'
    
    def setUp(self):
        
        self.host = Host.create_host(ip_address='193.122.66.53')
        self.none_host = Host.get_host('122.121.33.45')
        with open('fixtures/wapiti.json', 'r') as f:
           json_data = f.read()
           data = json.loads(json_data)
        for datum in data:
            Wapiti.objects.create(
                host=self.host, 
                vulnerabilities=datum['fields']['vulnerabilities'],
                anomalies=datum['fields']['anomalies'],
                infos=datum['fields']['infos']
                )
        self.wapiti_scan = Wapiti.get_wapiti_scan_by_ip_address(host=self.host)

    def test_wapiti(self):
        view = self.client.get(f'{BASE_URL}/wapiti/scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/wapiti/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)
        
        
    def test_scan_result(self):
        self.assertIsNone(self.none_host)
        
        found_host = Host.get_host(self.host.ip_address)
        self.assertIsNotNone(found_host)
        
        response = self.client.get(f'{BASE_URL}/wapiti/get-result?ip_address=193.122.66.53')
        if self.wapiti_scan.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.wapiti_scan.count() > 0:
            self.assertEqual(response.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/wapiti/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)


    def test_model_field_type(self):
        wapiti = Wapiti.objects.get(id=1)
        
        vulnerabilities= wapiti._meta.get_field('vulnerabilities').get_internal_type()
        anomalies= wapiti._meta.get_field('anomalies').get_internal_type()
        infos= wapiti._meta.get_field('infos').get_internal_type()
        self.assertEqual(vulnerabilities, 'JSONField')
        self.assertEqual(anomalies, 'JSONField')
        self.assertEqual(infos, 'JSONField')
        
        
          