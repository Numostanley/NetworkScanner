import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.wapiti.models import Wapiti


class WhatWebModelTest(TestCase):

    def setUp(self):
        with open('fixtures/wapiti.json') as f:
            data = json.load(f)

        wapiti_data = []
        for datum in data:
            wapiti_data.append(datum)

        wapiti_data_list = [
            wapiti_data[0]['fields']['vulnerabilities'],
            wapiti_data[0]['fields']['anomalies'],
            wapiti_data[0]['fields']['infos']
        ]

        self.host = Host.create_host('193.122.66.53')
        self.wapiti = Wapiti.create_wapiti_scan(self.host, wapiti_data_list)

    def test_wapiti_creation(self):
        self.assertIsInstance(self.wapiti, Wapiti)

    def test_host_label(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(1)
        field_label = wapiti_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_vulnerabilities_label(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(1)
        field_label = wapiti_scan._meta.get_field('vulnerabilities').verbose_name
        self.assertEqual(field_label, 'vulnerabilities')

    def test_anomalies_label(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(1)
        field_label = wapiti_scan._meta.get_field('anomalies').verbose_name
        self.assertEqual(field_label, 'anomalies')

    def test_infos_label(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(1)
        field_label = wapiti_scan._meta.get_field('infos').verbose_name
        self.assertEqual(field_label, 'infos')

    def test_date_created_label(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(1)
        field_label = wapiti_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_wapiti_scan_by_id(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(1)
        self.assertIsInstance(wapiti_scan, Wapiti)
        self.assertEqual(wapiti_scan.id, 1)

    def test_get_wapiti_scan_by_host(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_host(self.host)
        self.assertIsInstance(wapiti_scan, QuerySet)

    def test_get_wapiti_by_id_does_not_exist(self):
        wapiti_scan = Wapiti.get_wapiti_scan_by_id(20)
        self.assertIsNone(wapiti_scan)

    def test_wapiti_str(self):
        self.assertEqual(self.wapiti.__str__(), self.wapiti.host.ip_address)
