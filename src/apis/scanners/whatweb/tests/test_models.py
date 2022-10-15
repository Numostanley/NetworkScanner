import json

from django.test import TestCase
from django.db.models import QuerySet

from apis.scanners.hosts.models import Host
from apis.scanners.whatweb.models import WhatWeb


class WhatWebModelTest(TestCase):

    def setUp(self):
        with open('fixtures/whatweb.json') as f:
            data = json.load(f)

        whatweb_data = []
        for datum in data:
            whatweb_data.append(datum)

        self.host = Host.create_host('193.122.66.53')
        self.whatweb = WhatWeb.create_whatweb_scan(self.host,
                                                   whatweb_data[0]['fields']['data']['data'])

    def test_whatweb_creation(self):
        self.assertIsInstance(self.whatweb, WhatWeb)

    def test_host_label(self):
        whatweb_scan = WhatWeb.get_whatweb_scan_by_id(1)
        field_label = whatweb_scan._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')

    def test_data_label(self):
        whatweb_scan = WhatWeb.get_whatweb_scan_by_id(1)
        field_label = whatweb_scan._meta.get_field('data').verbose_name
        self.assertEqual(field_label, 'data')

    def test_date_created_label(self):
        whatweb_scan = WhatWeb.get_whatweb_scan_by_id(1)
        field_label = whatweb_scan._meta.get_field('date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_get_whatweb_scan_by_id(self):
        whatweb_scan = WhatWeb.get_whatweb_scan_by_id(1)
        self.assertEqual(whatweb_scan.id, 1)
        self.assertIsInstance(whatweb_scan, WhatWeb)

    def test_get_whatweb_scan_by_host(self):
        whatweb_scan = WhatWeb.get_whatweb_scan_by_host(self.host)
        self.assertIsInstance(whatweb_scan, QuerySet)

    def test_get_whatweb_by_id_does_not_exist(self):
        whatweb_scan = WhatWeb.get_whatweb_scan_by_id(20)
        self.assertIsNone(whatweb_scan)

    def test_whatweb_str(self):
        self.assertEqual(self.whatweb.__str__(), self.whatweb.host.ip_address)
