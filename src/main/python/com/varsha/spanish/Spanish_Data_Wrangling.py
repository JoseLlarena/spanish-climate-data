#!/usr/local/python2.7
# -*- coding: latin-1 -*-

from pandas.io.parsers import read_csv
from pandas.tools.merge import concat
from fnmatch import fnmatch
import os
from os.path import join
from Listo import L
from numpy import nan
import gzip
import re

province_region = \
{
'A CORUÑA':'GALICIA',
'ALBACETE':'CASTILLA-LA MANCHA',
'ALICANTE':'COMUNIDAD VALENCIANA',
'ALMERIA':'ANDALUCIA',
'ARABA/ALAVA':'PAIS VASCO',
'ASTURIAS':'PRINCIPADO DE ASTURIAS',
'AVILA':'CASTILLA Y LEON',
'BADAJOZ':'EXTREMADURA',
'BARCELONA':'CATALUÑA',
'BIZKAIA':'PAIS VASCO',
'BURGOS':'CASTILLA Y LEON',
'CACERES':'EXTREMADURA',
'CADIZ':'ANDALUCIA',
'CANTABRIA':'CANTABRIA',
'CASTELLON':'COMUNIDAD VALENCIANA',
'CEUTA':'CEUTA',
'CIUDAD REAL':'CASTILLA-LA MANCHA',
'CORDOBA':'ANDALUCIA',
'CUENCA':'CASTILLA-LA MANCHA',
'GIPUZKOA':'PAIS VASCO',
'GIRONA':'CATALUÑA',
'GRANADA':'ANDALUCIA',
'GUADALAJARA':'CASTILLA-LA MANCHA',
'HUELVA':'ANDALUCIA',
'HUESCA':'ARAGON',
'ILLES BALEARS':'ILLES BALEARS',
'JAEN':'ANDALUCIA',
'LA RIOJA':'LA RIOJA',
'LAS PALMAS':'CANARIAS',
'LEON':'CASTILLA Y LEON',
'LLEIDA':'CATALUÑA',
'LUGO':'GALICIA',
'MADRID':'COMUNIDAD DE MADRID',
'MALAGA':'ANDALUCIA',
'MELILLA':'MELILLA',
'MURCIA':'REGION DE MURCIA',
'NAVARRA':'COMUNIDAD FORAL DE NAVARRA',
'OURENSE':'GALICIA',
'PALENCIA':'CASTILLA Y LEON',
'PONTEVEDRA':'GALICIA',
'SALAMANCA':'CASTILLA Y LEON',
'SEGOVIA':'CASTILLA Y LEON',
'SEVILLA':'ANDALUCIA',
'SORIA':'CASTILLA Y LEON',
'STA. CRUZ DE TENERIFE':'CANARIAS',
'TARRAGONA':'CATALUÑA',
'TERUEL':'ARAGON',
'TOLEDO':'CASTILLA-LA MANCHA',
'VALENCIA':'COMUNIDAD VALENCIANA',
'VALLADOLID':'CASTILLA Y LEON',
'ZAMORA':'CASTILLA Y LEON',
'ZARAGOZA':'ARAGON'
}


DMS_SUFFIX, MS_TO_KMH, TO_DEGREES, TO_360, MIN_PRECIP = re.compile(r'[NWE]'), 3.6, 1e4, 10, '0,05'


def _to_decimal_degrees(x):

    dms = DMS_SUFFIX.sub('', str(x))

    return (float(dms[:2]) + float(dms[2:4]) / 60 + float(dms[4:]) / 3600) * (-1 if 'W' in str(x) else  1)

def _normalise_stations(stations):

    del stations['INDSINOP']

    stations.columns = ['id', 'place', 'province', 'height', 'lat', 'long']

    stations = stations.replace({'place':{'"':'', ',':':'}})
    stations.insert(3, 'region', stations['province'].map(province_region))

    for text in ['place', 'province', 'region']:
        stations[text] = stations[text].apply(lambda x: str(x).decode('iso-8859-1').encode('utf-8'))

    for coordinates in ['lat', 'long']:
        stations[coordinates] = stations[coordinates].map(_to_decimal_degrees)

    return stations


def _normalise_monthly_obs(data):

    for c in ['Nombre', 'Provincia', 'Altitud' , u'Día', u'Día.1', u'Día.2', u'Día.3', u'Día.4', 'Dia', 'Hora']:
        del data[c]

    when = ['year', 'month']
    temp = ['avg_t', 'avg_max_t', 'avg_min_t', 'max_t', 'min_t', 'high_min_t', 'low_max_t']
    precip = [ 'days_frost', 'total_p', 'max_p', 'days_light_p', 'days_moderate_p', 'days_rain_p', 'days_snow_p', 'days_hail_p']
    wind = ['gust_dir_w', 'gust_speed_w', 'days_strong_w', 'days_very_strong_w', 'avg_speed_w']
    sunshine = ['avg_daily_s', 'pct_s']
    pressure = ['avg_pss', 'max_pss', 'min_pss', 'avg_sfc_pss']

    data.columns = ['id'] + when + temp + precip + wind + sunshine + pressure

    data = data.replace({'total_p':{'Ip':MIN_PRECIP, ',':'.'}, 'max_p':{'Ip':MIN_PRECIP, ',':'.'}})
    for p in ['total_p', 'max_p']:
        data[p] = data[p].astype(float)

    data['gust_dir_w'] = data['gust_dir_w'].map(lambda w: nan if w == 99 else w * TO_360)

    for w in ['gust_speed_w', 'avg_speed_w']:
        data[w] = data[w] * MS_TO_KMH

    return data

def _normalise_daily_obs(data):

    for c in ['Nombre', 'Provincia', 'Altitud' , 'T.Med', 'Hora', 'Hora.1', 'Hora.2', 'Hora.3', 'Hora.4']:
        del data[c]

    data.columns = ['id', 'year', 'month', 'day', 'max_t', 'min_t', 'gust_speed_w', 'gust_dir_w', 'avg_speed_w', 'precip', 'sunshine', 'max_pss', 'min_pss']

    data = data.replace({'precip':{'Ip':MIN_PRECIP, ',':'.', 'Acum': nan, ' ': nan}})

    data['precip'] = data['precip'].astype(float)

    data['gust_dir_w'] = data['gust_dir_w'].map(lambda w: nan if w in{99, 88} else w * TO_360)

    for w in ['gust_speed_w', 'avg_speed_w']:
        data[w] = data[w] * MS_TO_KMH

    return data


def _normalise_obs(_dir, norm_function):

    return L(os.listdir(_dir)) \
        .where(lambda in_dir: fnmatch(in_dir, '*.CSV')) \
        .map(lambda _file: norm_function(read_csv(join(_dir, _file), sep=';', decimal=',', dtype={'Indicativo':str}, low_memory=False))) \
        .agg(lambda sofar, data: concat([sofar, data]))


def _zip(data, location):

    data.to_csv(location, index=False, float_format='%.2f', encoding='utf-8')

    with open(location, 'rb') as raw:
        with gzip.open(location + '.gz', 'wb') as zipped:
            zipped.writelines(raw)

if __name__ == '__main__':

    OUT_DIR = '../../../../resources/'
    BASE_DIR = '../../../../resources/'
    MONTHLY_DIR, DAILY_DIR = BASE_DIR + 'mensuales/estaciones/', BASE_DIR + 'diarios/estaciones/'

    _normalise_stations(read_csv(BASE_DIR + 'maestro.csv', sep=';')).to_csv(OUT_DIR + 'stations.csv', index=False, encoding='utf-8')
#     _zip(_normalise_obs(MONTHLY_DIR, _normalise_monthly_obs), OUT_DIR + 'spanish_monthly.csv')
#     _zip(_normalise_obs(DAILY_DIR, _normalise_daily_obs), OUT_DIR + 'spanish_daily.csv')


