import bng

# Original tests from documented examples


def test_to_osgb36_arthurs_seat_example():
    x, y = bng.to_osgb36('NT2755072950')
    assert (x, y) == (327550, 672950)


def test_to_osgb36_zipped_example():
    gridrefs = ['HU431392', 'SJ637560', 'TV374354']
    xy = bng.to_osgb36(gridrefs)
    x, y = zip(*xy)
    assert x == (443100, 363700, 537400)
    assert y == (1139200, 356000, 35400)


def test_from_osbg36_single_example():
    gridref = bng.from_osgb36((327550, 672950))
    assert gridref == 'NT275729'


def test_from_osbg36_zipped_example():
    x = [443143, 363723, 537395]
    y = [1139158, 356004, 35394]
    xy = zip(x, y)
    gridrefs = bng.from_osgb36(xy, nDigits=4)
    assert gridrefs == ['HU4339', 'SJ6356', 'TV3735']


def test_floor_example_from_dan_harasty():
    # See blog post comment for details of this example
    gridref = bng.from_osgb36((529900, 199900), nDigits=4)
    assert gridref == 'TQ2999'
