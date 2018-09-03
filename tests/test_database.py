# -*- coding: utf-8  -*-
"""Unit tests for database.py."""

import unittest
from collections import defaultdict

import mock

import database


class TestReData(unittest.TestCase):

    def test_reData_event_line(self):
        input_data = 'wl["monuments"][2010] = {'
        result = database.reData(input_data, 2014)
        expected = {
            u'country': None,
            u'year': '2010',
            u'end': None,
            u'event': 'monuments',
            u'start': None
        }
        self.assertEqual(result, expected)

    def test_reData_event_line_public_art(self):
        input_data = 'wl["public_art"][2012] = {'
        result = database.reData(input_data, 2014)
        expected = {
            u'country': None,
            u'year': '2012',
            u'end': None,
            u'event': 'public_art',
            u'start': None
        }
        self.assertEqual(result, expected)

    def test_reData_country_line(self):
        input_data = '''
    ["az"] = {["start"] = 20170430200000, ["end"] = 20170531195959},
    '''
        result = database.reData(input_data, 2017)
        expected = {
            u'country': 'az',
            u'year': None,
            u'end': '20170531195959',
            u'event': None,
            u'start': '20170430200000'
        }
        self.assertEqual(result, expected)


class TestRePrefix(unittest.TestCase):

    def test_re_prefix_match_ascii_line(self):
        self.assertIsNotNone(database.re_prefix(u'    ["az"] = "Azerbaijan",'))

    def test_re_prefix_match_ascii_line_with_space(self):
        self.assertIsNotNone(database.re_prefix(u'    ["gq"] = "Equatorial Guinea",'))

    def test_re_prefix_match_ascii_line_with_dash(self):
        self.assertIsNotNone(database.re_prefix(u'    ["gw"] = "Guinea-Bissau",'))

    def test_re_prefix_match_ascii_line_with_accents(self):
        self.assertIsNotNone(database.re_prefix(u'    ["re"] = "Réunion",'))

    def test_re_prefix_match_ascii_line_with_apostrophe(self):
        self.assertIsNotNone(database.re_prefix(u'    ["ci"] = "Côte d\'Ivoire",'))


class TestGetDataMixin(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('database.get_data_for_category', autospec=True)
        self.mock_get_data_for_category = patcher.start()
        self.mock_get_data_for_category.return_value = (
            (20140529121626, False, u'Alice', 20140528235032),
            (20140523121626, False, u'Bob', 20130523235032),
        )
        self.addCleanup(patcher.stop)


class TestGetData(TestGetDataMixin):

    def test_GetData(self):
        competition_config = {
            u'Brazil': {'start': 20140501030000, 'end': 20140601025959},
        }

        result = database.getData("Dumplings2014", competition_config)

        expected_timestamp_data = defaultdict(int)
        expected_timestamp_data.update({'20140523': 1, '20140529': 1})

        expected = {
            u'Brazil': {
                'count': 2,
                'usercount': 2,
                'start': 20140501030000,
                'userreg': 1,
                'data': expected_timestamp_data,
                'users': {
                    u'Alice': {
                        'count': 1,
                        'reg': 20140528235032,
                        'usage': 0
                    },
                    u'Bob': {
                        'count': 1,
                        'reg': 20130523235032,
                        'usage': 0
                    }
                },
                'usage': 0,
                'category': u'Images_from_Wiki_Loves_Dumplings_2014_in_Brazil',
                'end': 20140601025959
            }
        }
        self.assertEquals(result, expected)


class TestGetCountryData(TestGetDataMixin):

    def test_get_country_data(self):
        category = u'Images_from_Wiki_Loves_Dumplings_2014_in_Brazil'
        result = database.get_country_data(category, 20140501030000, 20140601025959)

        expected_timestamp_data = defaultdict(int)
        expected_timestamp_data.update({'20140523': 1, '20140529': 1})

        expected = {
            'count': 2,
            'usercount': 2,
            'start': 20140501030000,
            'userreg': 1,
            'data': expected_timestamp_data,
            'users': {
                u'Alice': {
                    'count': 1,
                    'reg': 20140528235032,
                    'usage': 0
                },
                u'Bob': {
                    'count': 1,
                    'reg': 20130523235032,
                    'usage': 0
                }
            },
            'usage': 0,
            'category': category,
            'end': 20140601025959
        }
        self.mock_get_data_for_category.assert_called_once_with(category)
        self.assertEquals(result, expected)


class TestParseConfig(unittest.TestCase):

    def test_parse_config_empty(self):
        config = ''
        result = database.parse_config(config)
        expected = {}
        self.assertEquals(result, expected)

    def test_parse_config(self):
        config = '''
wl["prefixes"] = {
    ["az"] = "Azerbaijan",
    ["gw"] = "Guinea-Bissau"
}

wl["monuments"][2017] = {
    ["az"] = {["start"] = 20170430200000, ["end"] = 20170531195959},
    ["gw"] = {["start"] = 20170430200000, ["end"] = 20170531195959},
}

wl["monuments"][2018] = {
    ["az"] = {["start"] = 20180430200000, ["end"] = 20180531195959},
    ["gw"] = {["start"] = 20180430200000, ["end"] = 20180531195959},
}

'''
        result = database.parse_config(config)
        expected = {
            u'monuments2017': {
                u'Azerbaijan': {
                    'start': 20170430200000,
                    'end': 20170531195959,
                },
                u'Guinea-Bissau': {
                    'start': 20170430200000,
                    'end': 20170531195959,
                },
            },
            u'monuments2018': {
                u'Azerbaijan': {
                    'start': 20180430200000,
                    'end': 20180531195959,
                },
                u'Guinea-Bissau': {
                    'start': 20180430200000,
                    'end': 20180531195959,
                },
            }
        }
        self.assertEquals(result, expected)


if __name__ == "__main__":
    unittest.main()
