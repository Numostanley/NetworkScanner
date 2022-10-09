from django.test import TestCase

from apis.scanners.base.tests import BASE_URL


class WafW00fTest(TestCase):

    def test_wafw00f(self):
        view = self.client.get(f'{BASE_URL}/wafwoof/scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)

    def test_wafw00f_scan_result_api_view(self):
        response_400 = self.client.get(f'{BASE_URL}/wafwoof/get-result?ip_address=')
        self.assertEqual(response_400.status_code, 400)

        # host = Host.get_host()
        # self.assertEqual()

        response = self.client.get(f'{BASE_URL}/dirby/get-result?ip_address=193.122.67.133')
        self.assertEqual(response.status_code, 200)
