from django.test import TestCase

from .test_base import BASE_URL


class CVEScannerTest(TestCase):

    def test_cvescanner(self):
        view = self.client.get(f'{BASE_URL}/cve-scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
