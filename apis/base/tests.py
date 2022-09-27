from django.test import TestCase
from django.urls import reverse


class VulnScanTest(TestCase):

    def test_scan(self):
        view = self.client.get(reverse('scan'))
        response = self.client.post(reverse('scan'), data={"IP": "193.122.66.53"})
        self.assertEqual(view.status_code, 200)
        self.assertEqual(response.status_code, 200)
