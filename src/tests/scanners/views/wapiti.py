from django.test import TestCase


class WapitiTest(TestCase):

    def test_wapiti(self):
        view = self.client.get('/api/v1/scanners/wapiti-scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
