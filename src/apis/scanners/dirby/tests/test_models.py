import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.dirby.models import DirBy


class DirByModelTest(TestCase):

    def setUp(self):
        # with open('fixtures/dirby.json') as f:
        #     data = json.load(f)
        self.host = Host.create_host('193.122.66.53')
        self.dirby = DirBy.create_dirby_scan(self.host, {})

    def test_dirby_creation(self):
        self.assertIsInstance(self.dirby, DirBy)

    def test_host_label(self):
        dirby_scan = DirBy.get_dirby_scan_by_id(1)
        field_label = dirby_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_data_label(self):
        dirby_scan = DirBy.get_dirby_scan_by_id(1)
        field_label = dirby_scan._meta.get_field('data').verbose_name
        self.assertEqual(field_label, 'data')

    def test_date_created_label(self):
        dirby_scan = DirBy.get_dirby_scan_by_id(1)
        field_label = dirby_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_dirby_scan_by_id(self):
        dirby_scan = DirBy.get_dirby_scan_by_id(1)
        self.assertEqual(dirby_scan.id, 1)
        self.assertIsInstance(dirby_scan, DirBy)

    def test_get_dirby_scan_by_host(self):
        dirby_scan = DirBy.get_dirby_scan_by_host(self.host)
        self.assertIsInstance(dirby_scan, QuerySet)

    def test_dirby_str(self):
        self.assertEqual(self.dirby.__str__(), self.dirby.host.ip_address)
