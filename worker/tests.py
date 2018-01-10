from django.test import TestCase

from .models import JavaExtractor, PythonExtractor
import os
import json

def read_test_data(name):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'test_data', name)
    with open(path, 'r') as f:
        return f.read()

def read_test_result(name):
    name = name + '.fragments.json'
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'test_data', name)
    with open(path, 'r') as f:
        return json.load(f)

class ExtractorTestCase(TestCase):

    def extractor(self):
        pass

    def extract(self, name):
        code = read_test_data(name)
        fragments = self.extractor().extract(code)

        # print(json.dumps(fragments, indent=4))

        expected = read_test_result(name)

        self.assertDictEqual(fragments, expected)

class JavaTestCase(ExtractorTestCase):
    def extractor(self):
        return JavaExtractor()

    def test_java_class(self):
        self.extract('Total.java')

class PythonTestCase(ExtractorTestCase):
    def extractor(self):
        return PythonExtractor()

    def test_total(self):
        self.extract('total.py')

    def test_company(self):
        self.extract('company.py')
