"""
Sorry for the derp in naming, django testing is derped
The testing framework generates a new test database before running tests
"""
from catalog.models import Category, BoxName
import unittest

class CategoryTest(unittest.TestCase):
    def setUp(self):
        Category.objects.create(letter="B", name="Mother and Child")
        self.category_csv = "B,Mother and Child"
        self.test_csv = "T,Test"

    def test_category_export(self):
        mother = Category.objects.get(letter="B")
        csv = mother.to_csv()
        self.assertTrue(csv == self.category_csv)

    def test_category_import(self):
        csv = Category.create_from_csv(self.test_csv)
        self.assertTrue(Category.objects.get(letter="T") is not None)

class BoxNameTest(unittest.TestCase):
    def setUp(self):
        self.cat = Category(letter="C", name="Mother and Child")
        self.cat.save()
        self.data = BoxName.objects.create(category=self.cat, name="Data")

    def test_box_name_export(self):
        test = self.data
        csv = test.to_csv()
        self.assertTrue(csv=="C,Data")

    #fix
    def test_box_name_import(self):
        data = "C,Test"
        csv = BoxName.create_from_csv(data)
        self.assertTrue(BoxName.objects.get(name="Test") is not None)
