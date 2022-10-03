from django.test import TestCase


class CVEScannerTest(TestCase):

    def test_CVEscanner(self):
        view = self.client.get('/api/v1/scanners/cve-scan?ip_address=193.122.66.53')
        self.assertEqual(view.status_code, 200)
