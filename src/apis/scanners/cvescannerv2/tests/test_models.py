import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.cvescannerv2.models import CVEScannerV2


class CVEScannerV2ModelTest(TestCase):

    def setUp(self):
        with open('fixtures/cvescannerv2.json') as f:
            data = json.load(f)

        cve_data = []
        for datum in data:
            cve_data.append(datum)

        self.host = Host.create_host('193.122.66.53')
        self.cvescannerv2 = CVEScannerV2.create_cvescanner_scan(self.host,
                                                                cve_data[0]['fields']['cve_data']['cve_data'])

    def test_cvescannerv2_creation(self):
        self.assertIsInstance(self.cvescannerv2, CVEScannerV2)

    def test_host_label(self):
        cvescannerv2_scan = CVEScannerV2.get_cvescannerv2_scan_by_id(1)
        field_label = cvescannerv2_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_data_label(self):
        cvescannerv2_scan = CVEScannerV2.get_cvescannerv2_scan_by_id(1)
        field_label = cvescannerv2_scan._meta.get_field('cve_data').verbose_name
        self.assertEqual(field_label, 'cve data')

    def test_date_created_label(self):
        cvescannerv2_scan = CVEScannerV2.get_cvescannerv2_scan_by_id(1)
        field_label = cvescannerv2_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_cvescannerv2_scan_by_id(self):
        cvescannerv2_scan = CVEScannerV2.get_cvescannerv2_scan_by_id(1)
        self.assertEqual(cvescannerv2_scan.id, 1)
        self.assertIsInstance(cvescannerv2_scan, CVEScannerV2)

    def test_get_cvescannerv2_scan_by_host(self):
        cvescannerv2_scan = CVEScannerV2.get_cvescannerv2_by_host(self.host)
        self.assertIsInstance(cvescannerv2_scan, QuerySet)

    def test_cvescannerv2_str(self):
        self.assertEqual(self.cvescannerv2.__str__(), self.cvescannerv2.host.ip_address)
