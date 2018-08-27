# -*- coding: utf-8  -*-
"""Unit tests for functions.py."""

import json
import os
import unittest

import functions


class TestGetWikilovesCategoryName(unittest.TestCase):

    def test_get_wikiloves_category_name(self):
        result = functions.get_wikiloves_category_name("Earth", "2016", "France")
        expected = u'Images_from_Wiki_Loves_Earth_2016_in_France'
        self.assertEqual(result, expected)

    def test_get_wikiloves_category_name_using_exception(self):
        result = functions.get_wikiloves_category_name("Earth", "2016", "Netherlands")
        expected = u'Images_from_Wiki_Loves_Earth_2016_in_the_Netherlands'
        self.assertEqual(result, expected)

    def test_get_wikiloves_category_name_using_special_exception(self):
        result = functions.get_wikiloves_category_name("Monuments", "2017", "Austria")
        expected = u'Media_from_WikiDaheim_2017_in_Austria/Cultural_heritage_monuments'
        self.assertEqual(result, expected)


class TestGetEventName(unittest.TestCase):

    def test_get_event_name_wikiloves(self):
        data = {
            'earth': 'Wiki Loves Earth',
            'africa': 'Wiki Loves Africa',
            'monuments': 'Wiki Loves Monuments',
            'monuments': 'Wiki Loves Monuments',
        }
        for (event_slug, event_name) in data.items():
            result = functions.get_event_name(event_slug)
            self.assertEqual(result, event_name)

    def test_get_event_name_wikiloves_several_words(self):
        result = functions.get_event_name('public_art')
        expected = 'Wiki Loves Public Art'
        self.assertEqual(result, expected)


class TestGetCountrySummary(unittest.TestCase):

    def test_get_country_summary(self):
        country_data = {
            "Turkey": {
                "earth": {
                    "2015": {
                        "count": 5,
                        "usage": 0,
                        "userreg": 0,
                        "usercount": 1
                    }
                },
                "monuments": {
                    "2016": {
                        "count": 5,
                        "usage": 0,
                        "userreg": 0,
                        "usercount": 1
                    },
                    "2017": {
                        "count": 8,
                        "usage": 0,
                        "userreg": 0,
                        "usercount": 1
                    }
                }
            },
            "Panama": {
                "earth": {
                    "2016": {
                        "count": 26,
                        "usage": 0,
                        "userreg": 2,
                        "usercount": 2
                    }
                },
                "monuments": {
                    "2016": {
                        "count": 22,
                        "usage": 0,
                        "userreg": 2,
                        "usercount": 2
                    }
                }
            },
            "Benin": {
                "africa": {
                    "2014": {
                        "count": 5,
                        "usage": 0,
                        "userreg": 0,
                        "usercount": 1
                    }
                }
            }
        }
        result = functions.get_country_summary(country_data)
        expected = {
            'Benin': [None, None, ['2014'], None],
            'Panama': [['2016'], ['2016'], None, None],
            'Turkey': [['2015'], ['2016', '2017'], None, None]
        }
        self.assertEqual(result, expected)


class TestProcessDataMixin(unittest.TestCase):

    def setUp(self):
        current_path = os.path.abspath(os.path.curdir)
        data_file = os.path.join(current_path, 'conf/db.dump.json')
        self.data = json.load(open(data_file, 'r'))


class TestProcessData(TestProcessDataMixin):

    def test_get_country_data(self):
        result = functions.get_country_data(self.data)
        expected = {
            u'Austria': {
                u'public_art': {
                    u'2013': {
                        'count': 5,
                        'usage': 0,
                        'usercount': 1,
                        'userreg': 0
                    }
                }
            },
            u'Benin': {
                u'africa': {
                    u'2014': {
                        'count': 5,
                        'usage': 0,
                        'usercount': 1,
                        'userreg': 0
                    }
                }
            },
            u'Panama': {
                u'earth': {
                    u'2015': {
                        'count': 26,
                        'usage': 0,
                        'usercount': 2,
                        'userreg': 2
                    }
                },
                u'monuments': {
                    u'2016': {
                        'count': 26,
                        'usage': 0,
                        'usercount': 2,
                        'userreg': 2
                    }
                }
            },
            u'Turkey': {
                u'earth': {
                    u'2015': {
                        'count': 5,
                        'usage': 0,
                        'usercount': 1,
                        'userreg': 0
                    }
                },
                u'monuments': {
                    u'2016': {
                        'count': 5,
                        'usage': 0,
                        'usercount': 1,
                        'userreg': 0
                    }
                }
            }
        }
        self.assertEqual(result, expected)

    def test_get_events_data(self):
        result = functions.get_events_data(self.data)
        expected = {
            u'africa': {
                u'2014': {
                    'count': 5,
                    'country_count': 1,
                    'usage': 0,
                    'usercount': 1,
                    'userreg': 0
                }
            },
            u'earth': {
                u'2015': {
                    'count': 31,
                    'country_count': 2,
                    'usage': 0,
                    'usercount': 3,
                    'userreg': 2
                }
            },
            u'monuments': {
                u'2016': {
                    'count': 31,
                    'country_count': 2,
                    'usage': 0,
                    'usercount': 3,
                    'userreg': 2
                }
            },
            u'public_art': {
                u'2013': {
                    'count': 5,
                    'country_count': 1,
                    'usage': 0,
                    'usercount': 1,
                    'userreg': 0
                }
            }
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
