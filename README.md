# BNG

> Convert between BNG grid refs (e.g. NT123456) and OSGB36 (EPSG:27700) coords

Coordinates in the [Ordnance Survey National Grid](https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid) or British National Grid are often defined by alphanumeric grid references that refer to grid squares.
These are based on the `osgb36` (EPSG:27700) coordinate reference system but are not understood by most GIS software.
This module contains Python functions to convert 4, 6, 8, or 10 figure alphanumeric grid references to/from pure `osgb36` coordinates.

This code was originally published on a blog post: [Easily change coordinate projection systems in Python with pyproj](http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/).
The blog post contains more information and instructions for converting between coordinate systems using Python.

## Installation

BNG can be installed for Python 2.7 or Python 3 using pip:

```
pip install bng
```

## Instructions

The `to_osgb36` and `from_osgb36` functions are used to convert between tuples of OSGB36 (x, y) coordinates and alphanumeric grid references.

### to_osgb36

BNG grid references can be converted to `osgb36` coordinates as follows.

Single values:

```python
import bng
bng.to_osgb36('NT2755072950')
# (327550, 672950)
```

The coordinates correspond to the southwest corner of the grid square described by the grid reference.

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

### from_osgb36

BNG grid references can be created from`osgb36` coordinates as follows.

Single values:
```python
import bng
bng.from_osgb36((327550, 672950), figs=6)
# 'NT275729'
```

The number of figures in the grid reference can be specified.
The coordinates correspond to the southwest corner of the grid square containing the (x, y) coordinates.

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
wgs84=pyproj.CRS("EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
osgb36=pyproj.CRS("EPSG:27700") # UK Ordnance Survey, 1936 datum

# Transform
x, y = bng.to_osgb36('NT2755072950')
pyproj.transform(osgb36, wgs84, x, y)
# (55.94410954187127, -3.1615548049941133i)
```

**Note**: older versions of pyproj use `pyproj.Proj("+init=EPSG:4326")` syntax
and [return coordinates in lon, lat
order](https://pyproj4.github.io/pyproj/stable/gotchas.html#axis-order-changes-in-proj-6).

GPS coordinates can be converted to BNG grid references as follows:

```python
import bng
import pyproj

# Define coordinate systems
wgs84=pyproj.CRS("EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
osgb36=pyproj.CRS("EPSG:27700") # UK Ordnance Survey, 1936 datum

# Transform
lon = -3.1615548588213667
lat = 55.944109545140932
x, y = pyproj.transform(wgs84, osgb36, lat, lon)
bng.from_osgb36((x, y))
# 'NT275729
```

Note that for surveying work (i.e. < 1 m accuracy) it is necessary to make a geoid correction.
Proj [uses](https://proj4.org/resource_files.html) grid correction files in NTv2 format to make this correction.
The Ordnance Survey provide these files (OSTN2 transformation model) [on their website](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/formats-for-developers.html).


## For Developers

Install developer dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest -vs test_bng.py
```
