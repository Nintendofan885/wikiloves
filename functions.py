# -*- coding: utf-8  -*-


def get_country_summary(country_data):
    return {c: [(country_data[c]['earth'].keys() if 'earth' in country_data[c] else None),
                (country_data[c]['monuments'].keys() if 'monuments' in country_data[c] else None),
                (country_data[c]['africa'].keys() if 'africa' in country_data[c] else None),
                (country_data[c]['public_art'].keys() if 'public_art' in country_data[c] else None)]
            for c in country_data}


def get_wikiloves_category_name(event, year, country):
    if (event, year, country) in special_exceptions:
        return special_exceptions[(event, year, country)]
    template = get_event_category_template()
    country_name = catExceptions.get(country, country.replace(' ', u'_'))
    return template.format(event=event, year=year, country=country_name)


def get_event_category_template():
    return u'Images_from_Wiki_Loves_{event}_{year}_in_{country}'


catExceptions = {
    u'Armenia': u'Armenia_&_Nagorno-Karabakh',
    u'Netherlands': u'the_Netherlands',
    u'Central African Republic': u'the_Central_African_Republic',
    u'Comoros': u'the_Comoros',
    u'Czech Republic': u'the_Czech_Republic',
    u'Democratic Republic of the Congo': u'the_Democratic_Republic_of_the_Congo',
    u'Republic of the Congo': u'the_Republic_of_the_Congo',
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
