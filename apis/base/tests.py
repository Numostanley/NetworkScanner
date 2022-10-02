from django.test import TestCase
from django.urls import reverse


class CVEScannerTest(TestCase):

    def test_CVEscanner(self):
        view = self.client.get('/api/v1/cves_can?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
       

 
class SslyzeTest(TestCase):
     
    def test_sslyze(self):
        view = self.client.get('/api/v1/sslyze_scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
        
        
 
 
class WapitiTest(TestCase):
    
    def test_wapiti(self):
        view = self.client.get('/api/v1/wapiti_scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
        
        