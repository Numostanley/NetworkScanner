from django.test import TestCase
from django.urls import reverse


class CVEScannerTest(TestCase):

    def test_CVEscanner(self):
        view = self.client.get(reverse('cvescan'))
        response = self.client.post(reverse('cvescan'), data={"IP": "193.122.66.53"})
        self.assertEqual(view.status_code, 200)
        self.assertEqual(response.status_code, 200)

 
class SslyzeTest(TestCase):
     
    def test_sslyze(self):
        
        view = self.client.get(reverse('sslyze_scan'))
        response = self.client.post(reverse('sslyze_scan'), data={"IP": "193.122.67.133"})
        self.assertEqual(view.status_code, 200)
        self.assertEqual(response.status_code, 200)
        
 
 
class WapitiTest(TestCase):
    
    def test_wapiti(self):
        
        view = self.client.get(reverse('wapiti_scan'))
        response = self.client.post(reverse('wapiti_scan'), data={"IP": "193.122.66.53"})
        self.assertEqual(view.status_code, 200)
        self.assertEqual(response.status_code, 200)

           