from django.test import TestCase


class SslyzeTest(TestCase):

    def test_sslyze(self):
        view = self.client.get('/api/v1/scanners/sslyze-scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
