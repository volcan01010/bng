# BNG

> Convert between BNG grid refs (e.g. NT123456) OSGB36 (EPSG:27700) coords

Coordinates in the [Ordnance Survey National Grid](https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid) or British National Grid are often defined by alphanumeric grid references.
These are based on the `osgb36` (EPSG:27700) coordinate reference system.
This module contains Python functions to convert `osgb36` coordinates to/from 4, 6, 8, or 10 figure alphanumeric grid references.

This code was originally published on the [Easily change coordinate projection systems in Python with pyproj](http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/) blog post.
See it for more information and for details on converting between coordinate systems using Python.

## Installation

BNG can be installed for Python 2.7 or Python 3 using pip:

```
pip install bng
```

## Instructions

The `to_osbg36` and `from_osbg36` functions are used to convert between tuples of OSGB36 (x, y) coordinates and alphanumeric grid references.

### to_osbg36

BNG grid references can be converted to `osbg36` coordinates as follows.

Single values:

```python
import bng
bng.to_osgb36('NT2755072950')
# (327550, 672950)
```

For multiple values, use Python's zip function and list comprehension:

```python
import bng
gridrefs = ['HU431392', 'SJ637560', 'TV374354']
x, y = zip(*[bng.to_osgb36(g) for g in gridrefs])
x
# (443100, 363700, 537400)
y
# (1139200, 356000, 35400)
```

### from_osbg36

`osbg36` coordinates can be converted to BNG grid references as follows.

Single values:
```python
import bng
bng.to_osgb36('NT2755072950')
# (327550, 672950)
```

The number of figures in the grid reference can be specified.

For multiple values, use Python's zip function and list comprehension:
```python
import bng
x = [443143, 363723, 537395]
y = [1139158, 356004, 35394]
[bng.from_osgb36(coords, figs=4) for coords in zip(x, y)]
# ['HU4339', 'SJ6356', 'TV3735']
```

### Converting grid references to GPS coordinates

`BNG` can be combined with `pyproj` (see [blog post](http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/)) to convert grid references to many different coordinate systems.

BNG grid references can be converted to lat/lon as used by GPS systems (EPSG:4326) as follows:

```python
import bng
import pyproj

# Define coordinate systems
wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
osgb36=pyproj.Proj("+init=EPSG:27700") # UK Ordnance Survey, 1936 datum

# Transform
x, y = bng.to_osgb36('NT2755072950')
pyproj.transform(osgb36, wgs84, x, y)
# (-3.1615548588213667, 55.944109545140932)
```

GPS coordinates can be converted to BNG grid references as follows:

```python
import bng
import pyproj

# Define coordinate systems
wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
osgb36=pyproj.Proj("+init=EPSG:27700") # UK Ordnance Survey, 1936 datum

# Transform
lon = -3.1615548588213667
lat = 55.944109545140932
x, y = pyproj.transform(wgs84, osgb36, lon, lat)
bng.from_osgb36((x, y))
# 'NT275729'
```

Note that for surveying work (i.e. < 1 m) it is necessary to make a geoid correction.
The OSTN2 transformation model used to do this is available on the [Ordnance Survey website](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html).
Proj [is able to use](https://proj4.org/resource_files.html) grid correction files in NTv2 format.


## For Developers

Install developer dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest -vs test_bng.py
```
