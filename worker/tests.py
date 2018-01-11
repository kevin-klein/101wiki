from django.test import TestCase

from .models import JavaExtractor, PythonExtractor, HaskellExtractor, SqlExtractor
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

    def __init__(self, *args):
        TestCase.__init__(self, *args)

        self.maxDiff = None

    def extractor(self):
        pass

    def extract(self, name):
        code = read_test_data(name)
        fragments = self.extractor().extract(code)

        # print(fragments)
        # print(json.dumps(fragments, indent=4))

        expected = read_test_result(name)

        self.assertEqual(fragments, expected)

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


class HaskellTestCase(ExtractorTestCase):
    def extractor(self):
        return HaskellExtractor()

    def test_extractor(self):
        self.extract('main.hs')

# class SqlTest(ExtractorTestCase):
#
#     def extractor(self):
#         return SqlExtractor()
#
#     def test_company(self):
#         self.extract('sql/Company.sql')
#
#     def test_cut(self):
#         self.extract('sql/Cut.sql')
#
#     def test_sample(self):
#         self.extract('sql/sampleCompany.sql')
#
#     def test_median(self):
#         self.extract('sql/median.sql')
#
#     def test_setup(self):
#         self.extract('sql/setup.sql')
#
#     def test_arrays(self):
#         self.extract('sql/array.sql')
