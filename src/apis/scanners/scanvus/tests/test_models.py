import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.scanvus.models import Scanvus

class ScanvusModelTest(TestCase):
    
    def setUp(self):
        with open('fixtures/scanvus.json') as f:
            data = json.load(f)

        scanvus_data = []
        for datum in data:
            scanvus_data.append(datum)

        self.host = Host.create_host('3.101.140.30')
        self.scanvus = Scanvus.create_scanvus_scan(self.host, scanvus_data[0]['fields'])
        
    def test_scanvus_creation(self):
        self.assertIsInstance(self.scanvus, Scanvus)
        
    def test_host_label(self):
        scanvus_scan = Scanvus.get_scanvus_scan_by_id(1)
        field_label = scanvus_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')
        
    def test_data_label(self):
        scanvus_scan = Scanvus.get_scanvus_scan_by_id(1)
        field_label = scanvus_scan._meta.get_field('data').verbose_name
        self.assertEqual(field_label, 'data')
        
    def test_date_created_label(self):
        scanvus_scan = Scanvus.get_scanvus_scan_by_id(1)
        field_label = scanvus_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')
        
    def test_get_scanvus_scan_by_id(self):
        scanvus_scan = Scanvus.get_scanvus_scan_by_id(1)
        self.assertEqual(scanvus_scan.id, 1)
        self.assertIsInstance(scanvus_scan, Scanvus)
        
    def test_get_scanvus_scan_by_host(self):
        scanvus_scan = Scanvus.get_scanvus_scan_by_host(self.host)
        self.assertIsInstance(scanvus_scan, QuerySet)
        
    def test_get_scanvus_by_id_does_not_exist(self):
        scanvus_scan = Scanvus.get_scanvus_scan_by_id(20)
        self.assertIsNone(scanvus_scan)
        
    def test_scanvus_str(self):
        self.assertEqual(self.scanvus.__str__(), self.scanvus.host.ip_address)
        