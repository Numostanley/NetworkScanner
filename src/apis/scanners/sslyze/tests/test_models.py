import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.sslyze.models import SSLyze


class SSLyzeModelTest(TestCase):

    def setUp(self):
        with open('fixtures/sslyze.json') as f:
            data = json.load(f)

        sslyze_data = []
        for datum in data:
            sslyze_data.append(datum)

        self.host = Host.create_host('193.122.66.53')
        self.sslyze = SSLyze.create_sslyze_scan(self.host, sslyze_data[0]['fields'])

    def test_sslyze_creation(self):
        self.assertIsInstance(self.sslyze, SSLyze)

    def test_host_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_connection_type_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('connection_type').verbose_name
        self.assertEqual(field_label, 'connection type')

    def test_connection_type_max_length(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        max_length = sslyze_scan._meta.get_field('connection_type').max_length
        self.assertEqual(max_length, 10)

    def test_connectivity_error_trace_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('connectivity_error_trace').verbose_name
        self.assertEqual(field_label, 'connectivity error trace')

    def test_connectivity_error_trace_max_length(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        max_length = sslyze_scan._meta.get_field('connectivity_error_trace').max_length
        self.assertEqual(max_length, 10)

    def test_connectivity_result_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('connectivity_result').verbose_name
        self.assertEqual(field_label, 'connectivity result')

    def test_connectivity_status_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('connectivity_status').verbose_name
        self.assertEqual(field_label, 'connectivity status')

    def test_connectivity_status_max_length(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        max_length = sslyze_scan._meta.get_field('connectivity_status').max_length
        self.assertEqual(max_length, 20)

    def test_network_configuration_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('network_configuration').verbose_name
        self.assertEqual(field_label, 'network configuration')

    def test_port_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('port').verbose_name
        self.assertEqual(field_label, 'port')

    def test_scan_result_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('scan_result').verbose_name
        self.assertEqual(field_label, 'scan result')

    def test_scan_status_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('scan_status').verbose_name
        self.assertEqual(field_label, 'scan status')

    def test_scan_status_max_length(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        max_length = sslyze_scan._meta.get_field('scan_status').max_length
        self.assertEqual(max_length, 20)

    def test_uuid_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('uuid').verbose_name
        self.assertEqual(field_label, 'uuid')

    def test_uuid_max_length(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        max_length = sslyze_scan._meta.get_field('uuid').max_length
        self.assertEqual(max_length, 30)

    def test_date_created_label(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_id(1)
        field_label = sslyze_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_sslyze_scan_by_host(self):
        sslyze_scan = SSLyze.get_sslyze_scan_by_host(self.host)
        self.assertIsInstance(sslyze_scan, QuerySet)

    def test_sslyze_str(self):
        self.assertEqual(self.sslyze.__str__(), self.sslyze.host.ip_address)
