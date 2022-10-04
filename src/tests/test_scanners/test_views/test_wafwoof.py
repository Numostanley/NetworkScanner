from django.test import TestCase

from .test_base import BASE_URL


class WafW00fTest(TestCase):

    def test_wafw00f(self):
        view = self.client.get(f'{BASE_URL}/wafwoof-scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
