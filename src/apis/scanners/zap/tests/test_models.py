import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.zap.models import Zap


class ZapModelTest(TestCase):

    def setUp(self) -> None:
        with open('fixtures/zap.json') as f:
            data = json.load(f)

        self.host = Host.create_host('193.122.66.53')
        self.zap = Zap.create_zap_scan(self.host, data[0]['fields']['data'])

    def test_zap_model_creation(self):
        self.assertIsInstance(self.zap, Zap)

    def test_host_label(self):
        zap_scan = Zap.get_zap_scan_by_id(1)
        field_label = zap_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_data_label(self):
        zap_scan = Zap.get_zap_scan_by_id(1)
        field_label = zap_scan._meta.get_field('data').verbose_name
        self.assertEqual(field_label, 'data')

    def test_date_created_label(self):
        zap_scan = Zap.get_zap_scan_by_id(1)
        field_label = zap_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_zap_scan_by_id(self):
        zap_scan = Zap.get_zap_scan_by_id(1)
        self.assertEqual(zap_scan.id, 1)
        self.assertIsInstance(zap_scan, Zap)

    def test_get_zap_scan_by_id_does_not_exist(self):
        zap_scan = Zap.get_zap_scan_by_id(20)
        self.assertIsNone(zap_scan)

    def test_get_zap_scan_by_host(self):
        zap_scan = Zap.get_zap_scan_by_host(self.host)
        self.assertIsInstance(zap_scan, QuerySet)

    def test_zap_str(self):
        self.assertEqual(self.zap.__str__(), self.zap.host.ip_address)
