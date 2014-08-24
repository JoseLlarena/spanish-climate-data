Spanish Climate data
====================


What's this?
------------

It's a lightly processed version of the daily and monthly summaries climate dataset released by the Spanish metoffice ([AEMET](http://www.aemet.es))
during 2011 and up until November 2012. It contains basic weather observations like precipitation and temperature for 114 Spanish weather stations for
the period between 1920 and 2012, in a format that makes it easier to use for data analysis.

This dataset was available free of charge during 2011 and most of 2012 but due to a change in government policy it's now only accessible for a fee, see [here]
(https://sede.aemet.gob.es/AEMET/en/GestionPeticiones/solicitudes) for how to access an updated version of these data, subject to charge.

The original raw data this dataset is derived from is available [here](http://usuarios.meteored.com/fotosusuarios/vigorro/series.zip).
Its a copy hosted by a trusted member of the Spanish stormchaser community. I cannot 100% guarantee its integrity or provenance, however myself and others
who have made use of it have found no issues so far.


What else?
----------

I've also included the python scripts I used to process the original data into standard format csv files, as well as scripts to load these csv files into
Sqlite.


Details
----------

Here's a field by field description of the changes I made:

stations.csv (description of each weather station):

indisinop:	id, removed as redundant
lat,long:	converted from degrees, minutes, seconds to [decimal degrees](http://en.wikipedia.org/wiki/Decimal_degrees)
place:		replaced commas with colons and removed inverted commas
region:		added Spanish region each stations is in

spanish_daily.csv:

place, province, altitude:	removed, redundant as present in stations file
average temperature:	removed , redundant as derived from min and max
times of max and min temperature and pressure and gust speed: removed as too detail for most analyses
precipitation: replaced the string 'trace' with .05, half way between 0 and .1, the minimum quantity non-zero recorded
also replaced string 'Acum' with empty, unsure what this is meant to be ( presumably 'Accumulated')
direction of strongest gust: converted from tens of degree to degrees
also there were some fields with values 99 and 88, outside the allowed range 0-36, that appear to mark days where gust direction was variable
highest gust speed, average wind speed: converted from m/s to km/hr


spanish_monthly.csv:

place, province, altitude:	same as above
times of max and min temperature, pressure, precipitation, highest wind speed : removed as too detail for most analyses
direction of strongest gust: same as above
highest gust speed, average wind speed: same as above


All files:

converted to utf-8 from the original latin-1 encoding
replaced continental decimal point , to .
replaced field separator ; with ,
translated original Spanish to English


wind_directions.csv : added csv file (and corresponding db table) to map wind direction degrees to compass directions, for convenience


License
-------

The code is MIT-licensed. The license for the original data was none of the well known ones but my reading of it is that it was essentially a
permissive MIT-style one. My translation of the Spanish original:



'''
The collection and processing of meteorological information, the result of
scientific and technical work by the State Meteorological Agency
 (AEMET), in line with scientific and technological progress,
are a form of intellectual property governed by Article
10 of Royal Legislative Decree 1/1996 of 12 April (Intellectual Property Law).
AEMET retains ownership and exercise of all rights,
both moral and economic, which form the exclusive right to
exploitation and dissemination of such information.

The information obtained and processed by AEMET is created with the highest
reliability afforded by current technology. This service is provided
with the means available at the time.

The information on this server is provided free to
citizens so that it can be freely used by them, with the sole
commitment to explicitly mention AEMET as processors of it
each time it is used for purposes other than individual and private ones.
AEMET declines all responsibility for damages that may
be incurred by the interpretation and use of the information made
available to the public on this server.

AEMET does not guarantee the full presentation of data on a continuous basis on the server,
also it reserves the right to modify, add or delete information contained thereon.
'''











