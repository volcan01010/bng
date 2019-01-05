# bng

Python functions to convert `osgb36` (EPSG:27700) coordinates to/from 4, 6, 8, or 10 figure grid references

This script was originally published on of the [Easily change coordinate projection systems in Python with pyproj](http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/) blog post.
See blog post for more information and for details on converting other coordinate systems to `osbg36`.

# Installation

bng can be installed for Python 2.7 or Python 3 using pip:

```
pip install git+git://github.com/volcan01010/bng
```

# Instructions

The function converts between a bng grid references as strings, and a tuple of OSGB36 (x,y) coordinates.
It can also handle lists, tuples or numpy arrays of grid reference strings and lists of coord tuples.
When converting to bng coordinates, there is an opportunity to specify how many figures to use.

bng coordinates can be converted to osbg36 (EPSG:27700) coordinates as follows:

```python
>>> import bng # import the bng module
>>> bng.to_osgb36('NT2755072950')
(327550, 672950)
```

Combined with `pyproj` (see [blog post](http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/)), this can be converted to GPS coordinates.
```python
>>> x, y = bng.to_osgb36('NT2755072950')
>>> pyproj.transform(osgb36, wgs84, x, y)
(-3.1615548588213667, 55.944109545140932)
```

Use Python’s zip function handle multiple values:
```python
>>> gridrefs = ['HU431392', 'SJ637560', 'TV374354']
>>> xy = bng.to_osgb36(gridrefs)
>>> x, y = zip(*xy)
>>> x
(443100, 363700, 537400)
>>> y
(1139200, 356000, 35400)
```

You can convert OSGB36 coordinates to bng coordinates like this:
```python
>>> bng.from_osgb36((327550, 672950))
'NT276730'
```

Again, use the zip function for multiple values. You can also specify the number of figures:
```python
>>> x = [443143, 363723, 537395]
>>> y = [1139158, 356004, 35394]
>>> xy = list(zip(x, y))
>>> bng.from_osgb36(xy, figs=4)
['HU4339', 'SJ6456', 'TV3735']
```

# For Developers

Install developer dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest -vs test_bng.py
```
