from django.test import TestCase
from django.urls import reverse

from apis.scanners.base.tests import BASE_URL


class ScreenShotTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(reverse('screenshot:scan', kwargs={}))
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(reverse('screenshot:scan', kwargs={'host': ''}))
        self.assertEqual(response.status_code, 400)

    def test_screenshot_scan_is_in_progress(self):
        response = self.client.get(f'{BASE_URL}/screenshot/scan?host={self.host}')
        self.assertEqual(response.status_code, 200)
