from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from apis.scanners.hosts.models import Host
import json
from .models import Wapiti

class WapitiTest(TestCase):
    
    def setUp(self):
        
        host = Host.create_host(ip_address='193.122.66.53')
       
        with open('test_db_data/wapiti.json', 'r') as f:
           json_data = f.read()
           
           data = json.loads(json_data)
         
        for datum in data:
            Wapiti.objects.create(
                host=host, 
                vulnerabilities=datum['fields']['vulnerabilities'],
                anomalies=datum['fields']['anomalies'],
                infos=datum['fields']['infos']
                )

    def test_wapiti(self):
        view = self.client.get(f'{BASE_URL}/wapiti/scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
        
        
    def test_scan_result(self):
        response = self.client.get(f'{BASE_URL}/wapiti/get-result?ip_address=193.122.66.53')
        self.assertEqual(response.status_code, 200)


    def test_model_field_type(self):
        wapiti = Wapiti.objects.get(id=1)
        
        vulnerabilities= wapiti._meta.get_field('vulnerabilities').get_internal_type()
        anomalies= wapiti._meta.get_field('anomalies').get_internal_type()
        infos= wapiti._meta.get_field('infos').get_internal_type()
        self.assertEqual(vulnerabilities, 'JSONField')
        self.assertEqual(anomalies, 'JSONField')
        self.assertEqual(infos, 'JSONField')
        
        
        
        
        
        