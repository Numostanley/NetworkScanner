from django.test import TestCase
from django.urls import reverse
# from .utils import sslyze_scan


# class CVEScannerTest(TestCase):

#     def test_CVEscanner(self):
#         view = self.client.get(reverse('cvescan'))
#         response = self.client.post(reverse('cvescan'), data={"IP": "193.122.66.53"})
#         self.assertEqual(view.status_code, 200)
#         self.assertEqual(response.status_code, 200)

 
class SslyzeTest(TestCase):
     
    def test_sslyze(self):
        
        view = self.client.get(reverse('sslyze_scan'))
        response = self.client.post(reverse('sslyze_scan'), data={"IP": "193.122.67.133"})
        self.assertEqual(view.status_code, 200)
        self.assertEqual(response.status_code, 200)
        
        