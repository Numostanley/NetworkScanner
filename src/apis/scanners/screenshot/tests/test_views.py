from django.http import FileResponse
from django.test import TestCase
from django.urls import reverse

from apis.scanners.hosts.models import Host
from apis.scanners.utils.extras import sanitize_host
from core.extras import env_vars


class ScreenShotScannerTest(TestCase):

    def setUp(self) -> None:
        self.host = '193.122.75.144'

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("screenshot:scan")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("screenshot:scan")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_screenshot_scan_is_in_progress(self):
        response = self.client.get(f'{reverse("screenshot:scan")}?host={self.host}')
        self.assertEqual(response.status_code, 200)


class ScreenShotScanResultTest(TestCase):

    def setUp(self) -> None:
        # create host
        Host.create_host('193.122.75.144')
        Host.create_host('193.122.66.53')

        self.found_host_with_result = Host.get_host('193.122.75.144')
        self.found_host_with_no_result_scan = Host.get_host('193.122.66.53')
        self.not_found_host = Host.get_host('112.22.45.210')

    def test_host_key_in_query_params(self):
        response = self.client.get(f'{reverse("screenshot:result")}?')
        self.assertEqual(response.status_code, 400)

    def test_host_key_value_not_specified_in_query_params(self):
        response = self.client.get(f'{reverse("screenshot:result")}?host=')
        self.assertEqual(response.status_code, 400)

    def test_host_not_found(self):
        # test if the host is not found
        self.assertIsNone(self.not_found_host)
        response = self.client.get(f'{reverse("screenshot:result")}?host={self.not_found_host}')
        self.assertEqual(response.status_code, 404)

    def test_zipped_screenshot_scanned_file_not_found(self):
        # retrieve screenshot scanned file from its directory
        file = f'/{env_vars.S3_DIR_PATH}/{sanitize_host(self.found_host_with_no_result_scan.ip_address)}.zip'
        with self.assertRaises(FileNotFoundError):
            FileResponse(open(file, 'rb'), as_attachment=True, filename=file)

    def test_zipped_screenshot_scanned_file_is_found(self):
        # retrieve screenshot scanned file from its directory
        file = f'/{env_vars.S3_DIR_PATH}/{sanitize_host(self.found_host_with_result.ip_address)}.zip'
        self.assertTrue(open(file, 'rb'))
        r = FileResponse(open(file, 'rb'), as_attachment=True, filename=file)
        self.assertIsInstance(r, FileResponse)
