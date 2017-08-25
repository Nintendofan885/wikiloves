# -*- coding: utf-8  -*-
"""Unit tests for database.py."""

import unittest

import database


class TestGetWikilovesCategoryName(unittest.TestCase):

    def test_get_wikiloves_category_name(self):
        result = database.get_wikiloves_category_name("earth2016", "France")
        expected = u'Images_from_Wiki_Loves_Earth_2016_in_France'
        self.assertEqual(result, expected)

    def test_get_wikiloves_category_name_using_exception(self):
        result = database.get_wikiloves_category_name("earth2016", "Netherlands")
        expected = u'Images_from_Wiki_Loves_Earth_2016_in_the_Netherlands'
        self.assertEqual(result, expected)


class TestReData(unittest.TestCase):

    def test_reData_event_line(self):
        input_data = 'wl["monuments"][2010] = {'
        result = database.reData(input_data)
        expected = {
            u'country': None,
            u'year': '2010',
            u'end': None,
            u'event': 'monuments',
            u'start': None
        }
        self.assertEqual(result, expected)

    def test_reData_country_line(self):
        input_data = '''
    ["az"] = {["start"] = 20170430200000, ["end"] = 20170531195959},
    '''
        result = database.reData(input_data)
        expected = {
            u'country': 'az',
            u'year': None,
            u'end': '20170531195959',
            u'event': None,
            u'start': '20170430200000'
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
