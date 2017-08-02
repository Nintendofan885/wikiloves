# -*- coding: utf-8  -*-
"""Unit tests for database.py."""

import unittest

import database


class TestGetCategoryName(unittest.TestCase):

    def test_get_category_name(self):
        result = database.get_category_name("earth2016", "France")
        expected = u'Images_from_Wiki_Loves_Earth_2016_in_France'
        self.assertEqual(result, expected)

    def test_get_category_name_using_exception(self):
        result = database.get_category_name("earth2016", "Netherlands")
        expected = u'Images_from_Wiki_Loves_Earth_2016_in_the_Netherlands'
        self.assertEqual(result, expected)
