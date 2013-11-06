"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from catalog.models import Category
import unittest

class CategoryTest(unittest.TestCase):
    def setUp(self):
        Category.objects.create(letter="B", name="Mother and Child")
        self.category_csv = "B&&&Mother and Child"
        self.test_csv = "T&&&Test"

    def test_category_export(self):
        mother = Category.objects.get(letter="B")
        csv = mother.to_csv()
        self.assertTrue(csv == self.category_csv)

    def test_category_import(self):
        csv = Category.from_csv(self.test_csv)
        self.assertTrue(Category.objects.get(letter="T") is not None)
