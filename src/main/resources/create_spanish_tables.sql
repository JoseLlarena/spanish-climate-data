DROP TABLE IF EXISTS DIRECTIONS;

CREATE TABLE DIRECTIONS
(

name text PRIMARY KEY,

start real NOT NULL UNIQUE CHECK(start >= 0 and start <= 360 ),
finish real NOT NULL UNIQUE CHECK(finish >= 0 and finish <= 360 )

);

DROP TABLE IF EXISTS STATIONS;

CREATE TABLE STATIONS
(

id text PRIMARY KEY,

place text NOT NULL UNIQUE,
province text NOT NULL,
region text NOT NULL,
height real NOT NULL CHECK(height >= -100 and height <= 3800),
lat real NOT NULL CHECK(lat >= 27 and lat <= 45),
long real NOT NULL CHECK(long >= -20 and long <= 15)

);


DROP TABLE IF EXISTS SPANISH_MONTHLY;

CREATE TABLE SPANISH_MONTHLY
(

id text  NOT NULL,

year integer NOT NULL CHECK(year >= 1800 and year <= 2012),
month integer NOT NULL CHECK(month >= 1 and month <= 12),

avg_t real CHECK(avg_t >= -60 and avg_t <= 60),
avg_max_t real CHECK(avg_max_t >= -60 and avg_max_t <= 60),
avg_min_t real CHECK(avg_min_t >= -60 and avg_min_t <= 60) ,
max_t real CHECK(max_t >= -60 and max_t <= 60),
min_t real CHECK(min_t >= -60 and min_t <= 60),
high_min_t real CHECK(high_min_t >= -60 and high_min_t <= 60),
low_max_t real CHECK(low_max_t >= -60 and low_max_t <= 60),

days_frost_p real CHECK(days_frost_p >= 0 and days_frost_p <= 31),
total_p real CHECK(total_p >= 0 and total_p <= 5000),
max_p real CHECK(max_p >= 0),
days_light_p real CHECK(days_light_p >= 0 and days_light_p <= 31),
days_moderate_p real CHECK(days_moderate_p >= 0 and days_moderate_p <= 31),
days_rain_p real CHECK(days_rain_p >= 0 and days_rain_p <= 31),
days_snow_p real CHECK(days_snow_p >= 0 and days_snow_p <= 31),
days_hail_p real CHECK(days_hail_p >= 0 and days_hail_p <= 31),

gust_dir_w real CHECK(gust_dir_w >= 0 and gust_dir_w <= 360 ),
gust_speed_w real CHECK(gust_speed_w >= 0 and gust_speed_w <= 300),
days_strong_w real CHECK(days_strong_w >= 0 and days_strong_w <= 31),
days_very_strong_w real CHECK(days_very_strong_w >= 0 and days_very_strong_w <= 31),
avg_speed_w real CHECK(avg_speed_w >= 0 and avg_speed_w <= 300),

avg_daily_s real CHECK(avg_daily_s >= 0 and avg_daily_s <= 24),
pct_s real CHECK(pct_s >= 0 and pct_s <= 100),

avg_pss real CHECK(avg_pss >= 500 and avg_pss <= 1060),
max_pss real CHECK(max_pss >= 500 and max_pss <= 1060),
min_pss real CHECK(min_pss >= 500 and min_pss <= 1060),
avg_sfc_pss real CHECK(avg_sfc_pss >= 900 and avg_sfc_pss <= 1060),

FOREIGN KEY(id) REFERENCES STATIONS(id)

);


DROP TABLE IF EXISTS SPANISH_DAILY;

CREATE TABLE SPANISH_DAILY
(
id text  NOT NULL,

year integer NOT NULL CHECK(year >= 1800 and year <= 2012),
month integer NOT NULL CHECK(month >= 1 and month <= 12),
day integer NOT NULL CHECK(day >= 1 and day <= 31),

max_t real CHECK(max_t >= -60 and max_t <= 60),
min_t real CHECK(min_t >= -60 and min_t <= 60),

gust_speed_w real CHECK(gust_speed_w >= 0 and gust_speed_w <= 300),
gust_dir_w real CHECK(gust_dir_w >= 0 and gust_dir_w <= 360 ),
avg_speed_w real CHECK(avg_speed_w >= 0 and avg_speed_w <= 300),

precip real CHECK(precip >= 0 and precip <= 5000),

sunshine real CHECK(sunshine >= 0 and sunshine <= 24),

max_pss real CHECK(max_pss >= 500 and max_pss <= 1060),
min_pss real CHECK(min_pss >= 500 and min_pss <= 1060),

FOREIGN KEY(id) REFERENCES STATIONS(id)

);

