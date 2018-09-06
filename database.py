#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import json
import re
import sys
import time
from collections import defaultdict
from urllib import urlopen

from commons_database import DB
from functions import EVENTS, get_wikiloves_category_name

updateLog = []


def reData(txt, year):
    """
    Parser para linha da configuração
    """
    events = '|'.join(EVENTS)
    regex = ur'''
        \s*wl\["(?P<event>%s)"\]\[(?P<year>20\d\d)]\ ?=\ ?\{|
        \s*\["(?P<country>[-a-z]+)"\]\ =\ \{\["start"\]\ =\ (?P<start>%s\d{10}),\ \["end"\]\ =\ (?P<end>%s\d\d{10})\}
        ''' % (events, year, str(year)[:3])
    m = re.search(regex, txt, re.X)
    return m and m.groupdict()


def re_prefix(txt):
    return re.search(u'\s*\["(?P<prefix>[\w-]+)"\] = "(?P<name>[\w\-\' ]+)"|(?P<close>\})', txt, re.UNICODE)


def get_config_from_commons(page):
    api = urlopen('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=revisions&titles=%s&rvprop=content' % page)
    text = json.loads(api.read())['query']['pages'].values()[0]['revisions'][0]['*']
    return unicode(text)


def parse_config(text):
    data, event, prefixes = {}, None, {}
    lines = iter(text.split(u'\n'))
    for l in lines:
        m = re_prefix(l)
        if prefixes and m and m.group('close'):
            break
        elif m and m.group('prefix'):
            prefixes[m.group('prefix')] = m.group('name')

    for l in lines:
        g = reData(l, event[-4:] if event else ur'20\d\d')
        if not g:
            continue
        if g['event']:
            event = g['event'] + g['year']
            data[event] = {}
        elif g['country'] and event:
            if g['country'] not in prefixes:
                updateLog.append(u'Unknown prefix: ' + g['country'])
                continue
            data[event][prefixes[g['country']]] = {'start': int(g['start']), 'end': int(g['end'])}

    return {name: config for name, config in data.items() if config}


def getConfig(page):
    """
    Lê a configuração da página de configuração no Commons
    """
    text = get_config_from_commons(page)
    return parse_config(text)


dbquery = u'''SELECT
 img_timestamp,
 img_name IN (SELECT DISTINCT gil_to FROM globalimagelinks) AS image_in_use,
 user.user_name as name,
 COALESCE(user_registration, "20050101000000") as user_registration
 FROM (SELECT
   cl_to,
   cl_from
   FROM categorylinks
   WHERE cl_to = %s AND cl_type = 'file') cats
 INNER JOIN page ON cl_from = page_id
 INNER JOIN image ON page_title = img_name
 LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
 LEFT JOIN user ON user.user_id = COALESCE(oldimage.oi_user, image.img_user)
'''


def getData(name, data):
    """
    Coleta dados do banco de dados e processa
    """

    default_starttime = min(data[c]['start'] for c in data if 'start' in data[c])
    default_endtime = max(data[c]['end'] for c in data if 'end' in data[c])
    result_data = {}

    for country_name, country_config in data.iteritems():

        event = name[0:-4].title()
        year = name[-4:]
        cat = get_wikiloves_category_name(event, year, country_name)
        if name == 'monuments2010':
            cat = u'Images_from_Wiki_Loves_Monuments_2010'

        start_time = country_config.get('start', default_starttime)
        end_time = country_config.get('end', default_endtime)
        country_data = get_country_data(cat, start_time, end_time)
        if country_data:
            result_data[country_name] = country_data
        else:
            updateLog.append(u'%s in %s is configurated, but no file was found in [[Category:%s]]' %
                             (name, country_name, cat.replace(u'_', u' ')))
    return result_data


def get_country_data(category, start_time, end_time):
    country_data = {}

    dbData = get_data_for_category(category)

    if not dbData:
        return None

    daily_data = defaultdict(int)  # data: {timestamp_day0: n, timestamp_day1: n,...}
    user_data = {}  # users: {'user1': {'count': n, 'usage': n, 'reg': timestamp},...}

    discarded_counter = 0

    for timestamp, usage, user, user_reg in dbData:
        # Desconsidera timestamps fora do período da campanha
        if not start_time <= timestamp <= end_time:
            discarded_counter += 1
            continue
        # Conta imagens por dia
        daily_data[str(timestamp)[0:8]] += 1
        if user not in user_data:
            user_data[user] = {'count': 0, 'usage': 0, 'reg': user_reg}
        user_data[user]['count'] += 1
        if usage:
            user_data[user]['usage'] += 1

    country_data.update(
        {'data': daily_data, 'users': user_data})
    country_data['usercount'] = len(user_data)
    country_data['count'] = sum(u['count'] for u in user_data.itervalues())
    country_data['usage'] = sum(u['usage'] for u in user_data.itervalues())
    country_data['userreg'] = len([user for user in user_data.itervalues() if user['reg'] > start_time])
    country_data['category'] = category
    country_data['start'] = start_time
    country_data['end'] = end_time
    if discarded_counter:
        updateLog.append(u'%s images discarded as out of bounds in [[Category:%s]]' %
                         (discarded_counter, category.replace(u'_', u' ')))

    return country_data


def get_data_for_category(category_name):
    """Query the database for a given category

    Return: Tuple of tuples (<timestamp>, <in use>, <User>, <registration>)
    (20140529121626, False, u'Example', 20140528235032)
    """
    query_data = commonsdb.query(dbquery, (category_name,))
    dbData = tuple(
        (int(timestamp),
         bool(usage),
         user.decode('utf-8'),
         int(user_reg or 0))
        for timestamp, usage, user, user_reg in query_data)
    return dbData


def update_event_data(event_slug, event_configuration, db):
    start = time.time()
    event_data = getData(event_slug, event_configuration)
    db[event_slug] = event_data
    with open('db.json', 'w') as f:
        json.dump(db, f)
    log = 'Saved %s: %dsec, %d countries, %d uploads' % \
        (event_slug, time.time() - start, len(event_data), sum(event_data[c].get('count', 0) for c in event_data))
    print log
    updateLog.append(log)
    return db


if __name__ == '__main__' and 'update' in sys.argv:
    config = getConfig(u'Module:WL_data')
    try:
        with open('db.json', 'r') as f:
            db = json.load(f)
    except Exception as e:
        print u'Erro ao abrir db.json:', repr(e)
        db = {}

    commonsdb = DB()
    for (event_name, event_configuration) in config:
        db = update_event_data(event_name, event_configuration, db)
    commonsdb.conn.close()
    if updateLog:
        with io.open('update.log', 'w', encoding='utf-8') as f:
            f.write(time.strftime('%Y%m%d%H%M%S') + '\n' + '\n'.join(updateLog))
