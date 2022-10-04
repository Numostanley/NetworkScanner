from django.test import TestCase

from .test_base import BASE_URL


class DirbyTest(TestCase):

    def test_dirby(self):
        view = self.client.get(f'{BASE_URL}/dirby-scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
