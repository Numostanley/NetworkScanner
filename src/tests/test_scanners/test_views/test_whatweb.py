from django.test import TestCase

from .test_base import BASE_URL


class WhatWebTest(TestCase):

    def test_whatweb(self):
        view = self.client.get(f'{BASE_URL}/whatweb/scan?ip_address=193.122.67.133')
        self.assertEqual(view.status_code, 200)
