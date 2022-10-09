from django.test import TestCase

from apis.scanners.base.tests import BASE_URL


class SslyzeTest(TestCase):

    def test_sslyze(self):
        view = self.client.get(f'{BASE_URL}/sslyze/scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
