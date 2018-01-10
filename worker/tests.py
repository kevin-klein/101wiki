from django.test import TestCase

from .models import JavaExtractor
import os

def read_test_data(name):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'test_data', name)
    with open(path, 'r') as f:
        return f.read()

class JavaTestCase(TestCase):
    def setUp(self):
        self.e = JavaExtractor()

    def test_java_class(self):
        """Fragments contain package and imports"""
        code = read_test_data('Total.java')
        fragments = self.e.extract(code)

        self.assertEqual(fragments['package'], 'org.softlang.company.features')
        self.assertEqual(fragments['imports'], ['org.softlang.company.xjc'])
        self.assertEqual(fragments['fragments'][0]['name'], 'Total')
