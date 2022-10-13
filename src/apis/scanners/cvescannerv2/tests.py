from django.test import TestCase

from apis.scanners.base.tests import BASE_URL
from .models import CVEScannerV2
from apis.scanners.hosts.models import Host
import json



class CVEScannerTest(TestCase):

    def setUp(self):
        
        self.host = Host.create_host(ip_address='193.122.66.53')
        self.none_host = Host.get_host('122.121.33.45')
        with open('fixtures/cvescannerv2.json', 'r') as f:
           data = json.load(f)
           
        for datum in data:
            CVEScannerV2.create_cvescanner_scan(host=self.host, data=datum['fields']['cve_data']['cve_data'])  
        self.cve_scan = CVEScannerV2.get_cvescanner_by_host(host=self.host)

    def test_cvescanner(self):
        response = self.client.get(f'{BASE_URL}/cvescanner/scan?ip_address=193.122.66.53')
        self.assertEqual(response.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/cvescanner/scan?ip_address=')
        self.assertEqual(response_400.status_code, 400)
        
    
    def test_scan_result(self):
        self.assertIsNone(self.none_host)
        
        found_host = Host.get_host(self.host.ip_address)
        self.assertIsNotNone(found_host)
        
        response = self.client.get(f'{BASE_URL}/cvescanner/get-result?ip_address=193.122.66.53')
        if self.cve_scan.count() < 1:
            self.assertEqual(response.status_code, 404)
        if self.cve_scan.count() > 0:
            self.assertEqual(response.status_code, 200)
        
        response_400 = self.client.get(f'{BASE_URL}/cvescanner/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)


    def test_model_field_type(self):
        cvescanner= CVEScannerV2.objects.get(id=1)
        
        cve_data= cvescanner._meta.get_field('cve_data').get_internal_type()
        self.assertEqual(cve_data, 'JSONField')
        