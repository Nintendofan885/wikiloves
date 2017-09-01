# -*- coding: utf-8  -*-

def get_wikiloves_category_name(event, year, country):
    if (event, year, country) in special_exceptions:
        return special_exceptions[(event, year, country)]
    category = u'Images_from_Wiki_Loves_%s_%s_in_' % (event, year)
    return category + catExceptions.get(country, country.replace(' ', u'_'))

catExceptions = {
    u'Armenia': u'Armenia_&_Nagorno-Karabakh',
    u'Netherlands': u'the_Netherlands',
    u'Czech Republic': u'the_Czech_Republic',
    u'Dutch Caribbean': u'the_Dutch_Caribbean',
    u'Philippines': u'the_Philippines',
    u'Seychelles': u'the_Seychelles',
    u'United Kingdom': u'the_United_Kingdom',
    u'United States': u'the_United_States'
}

special_exceptions = {
    ("Monuments", "2017", "Austria"): 'Media_from_WikiDaheim_2017_in_Austria/Cultural_heritage_monuments',
    ("Monuments", "2013", "Armenia"): 'Images_from_Wiki_Loves_Monuments_2013_in_Armenia',
}
