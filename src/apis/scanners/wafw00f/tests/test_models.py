import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.wafw00f.models import WafWoof


class WafW00fModelTest(TestCase):
    data = """
    [{
        "url": "https://193.122.75.144",
        "detected": false,
        "firewall": "None",
        "manufacturer": "None"
    }]
    """

    def setUp(self):
        self.host = Host.create_host('193.122.66.53')
        self.wafw00f = WafWoof.create_wafwoof_scan(self.host, json.loads(self.data))

    def test_wafw00f_creation(self):
        self.assertIsInstance(self.wafw00f, WafWoof)

    def test_host_label(self):
        wafw00f_scan = WafWoof.get_wafw00f_scan_by_id(1)
        field_label = wafw00f_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_data_label(self):
        wafw00f_scan = WafWoof.get_wafw00f_scan_by_id(1)
        field_label = wafw00f_scan._meta.get_field('data').verbose_name
        self.assertEqual(field_label, 'data')

    def test_date_created_label(self):
        wafw00f_scan = WafWoof.get_wafw00f_scan_by_id(1)
        field_label = wafw00f_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_wafw00f_scan_by_id(self):
        wafw00f_scan = WafWoof.get_wafw00f_scan_by_id(1)
        self.assertEqual(wafw00f_scan.id, 1)
        self.assertIsInstance(wafw00f_scan, WafWoof)

    def test_get_wafw00f_scan_by_host(self):
        wafw00f_scan = WafWoof.get_wafw00f_scan_by_host(self.host)
        self.assertIsInstance(wafw00f_scan, QuerySet)

    def test_get_wafw00f_by_id_does_not_exist(self):
        wafw00f_scan = WafWoof.get_wafw00f_scan_by_id(20)
        self.assertIsNone(wafw00f_scan)

    def test_wafw00f_str(self):
        self.assertEqual(self.wafw00f.__str__(), self.wafw00f.host.ip_address)
