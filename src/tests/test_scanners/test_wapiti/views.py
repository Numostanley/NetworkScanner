from django.test import TestCase

from tests.test_scanners import BASE_URL


class WapitiTest(TestCase):

    def test_wapiti(self):
        view = self.client.get(f'{BASE_URL}/wapiti/scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
