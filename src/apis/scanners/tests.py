from django.test import TestCase
from django.urls import reverse


class CVEScannerTest(TestCase):

    def test_CVEscanner(self):
        view = self.client.get('/api/v1/scanners/cve-scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
       
       
class SslyzeTest(TestCase):
     
    def test_sslyze(self):
        view = self.client.get('/api/v1/scanners/sslyze-scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
        
        
class WapitiTest(TestCase):
    
    def test_wapiti(self):
        view = self.client.get('/api/v1/scanners/wapiti-scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
        
       