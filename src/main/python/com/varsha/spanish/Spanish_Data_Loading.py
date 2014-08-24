#!/usr/local/python2.7
from traceback import print_exc
import sqlite3
from pandas.io.parsers import read_csv

SOURCE = '../../../../resources/'


def _load(data, into=None, db=SOURCE + 'climate.db'):

    place_holders = ','.join(['?'] * len(data[0]))

    with sqlite3.connect(db) as cnxn:
        cnxn.execute('PRAGMA foreign_keys = ON;')
        cnxn.cursor().executemany('INSERT INTO % VALUES($);'.replace('%', into).replace('$', place_holders), data)


def _read(from_location):

    return map(tuple, read_csv(from_location, encoding='utf-8', low_memory=False).values)


def _create_tables(db=SOURCE + 'climate.db', script_file=SOURCE + 'create_spanish_tables.sql'):

    script = None
    with open (script_file, 'r') as sql:
        script = sql.read().replace('\n', '')

    with sqlite3.connect(db) as cnxn:
        cnxn.cursor().executescript(script)


if __name__ == '__main__':

    try:

        _create_tables()
        _load(_read(SOURCE + 'wind_directions.csv'), into='DIRECTIONS')
        _load(_read(SOURCE + 'stations.csv'), into='STATIONS')
        _load(_read(SOURCE + 'spanish_daily.csv'), into='SPANISH_DAILY')
        _load(_read(SOURCE + 'spanish_monthly.csv'), into='SPANISH_MONTHLY')

    except:

        print_exc()


