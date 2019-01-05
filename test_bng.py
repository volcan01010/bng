# -*- coding: utf-8 -*-
import pytest

import bng


@pytest.mark.parametrize("x, y, figs, expected", [
    (1234, 1234, 4, 'SV0101'),
    (1234, 1234, 6, 'SV012012'),
    (1234, 1234, 8, 'SV01230123'),
    (1234, 1234, 10, 'SV0123401234'),
    (56789, 56789, 4, 'SV5656'),
    (56789, 56789, 6, 'SV567567'),
    (56789, 56789, 8, 'SV56785678'),
    (56789, 56789, 10, 'SV5678956789'),
])
def test_from_osgb36_rounds_figs_down(x, y, figs, expected):
    gridref = bng.from_osgb36((x, y), figs=figs)
    assert gridref == expected


@pytest.mark.parametrize("x, y, expected", [
    (0, 0, 'SV0000'),
    (500000, 0, 'TV0000'),
    (0, 900000, 'NA0000'),
    (400000, 1200000, 'HP0000'),
])
def test_from_osgb36_selects_correct_square(x, y, expected):
    gridref = bng.from_osgb36((x, y), figs=4)
    assert gridref == expected


@pytest.mark.parametrize("gridref, expected", [
    ('SV0156', (1000, 56000)),
    ('SV012567', (1200, 56700)),
    ('SV01235678', (1230, 56780)),
    ('SV0123456789', (1234, 56789)),
])
def test_to_osgb36_expands_figures_correctly(gridref, expected):
    # Test covers numbers below and over 5
    coords = bng.to_osgb36(gridref)
    assert coords == expected


def test_to_osgb36_handles_lower_case_input():
    coords = bng.to_osgb36('sv0101')
    assert coords == (1000, 1000)


@pytest.mark.parametrize("gridref, expected", [
    ('SV0000', (0, 0)),
    ('TV0000', (500000, 0)),
    ('NA0000', (0, 900000)),
    ('HP0000', (400000, 1200000)),
])
def test_to_osgb36_calculates_correct_offset(gridref, expected):
    coords = bng.to_osgb36(gridref)
    assert coords[:2] == expected[:2]


@pytest.mark.parametrize('coords', [
    'string_input',
    ['list', 'of', 'strings'],
    1,
    1.1,
    (1,),
    (1, 2, 3),
])
def test_from_osgb36_throws_bng_error_on_bad_coords_type(coords):
    with pytest.raises(bng.BNGError, match=r'Valid inputs are .*'):
        bng.from_osgb36(coords)


@pytest.mark.parametrize('coords', [
    (-1, 0),
    (0, -1),
    (-1, -1),
    (8e5, 0),
    (0, 13e5),
    (8e5, 13e5),
])
def test_from_osgb36_throws_bng_error_on_coords_out_of_range(coords):
    with pytest.raises(bng.BNGError, match=r'Coordinate location outside .*'):
        bng.from_osgb36(coords)


@pytest.mark.parametrize('figs', [-1, 1, 3, 11])
def test_from_osgb36_throws_bng_error_on_bad_figs_value(figs):
    with pytest.raises(bng.BNGError, match=r'Valid inputs for figs are .*'):
        bng.from_osgb36((123456, 123456), figs=figs)


@pytest.mark.parametrize('gridref', [
    'Not a grid reference',
    1234,
    ])
def test_to_osgb36_throws_bng_error_on_bad_gridref_type(gridref):
    with pytest.raises(bng.BNGError, match=r'Valid gridref inputs are.*'):
        bng.to_osgb36(gridref)


@pytest.mark.parametrize('gridref', ['AA1234', 'ZZ1234', 'NI1234'])
def test_to_osgb36_throws_bng_error_on_invalid_100km_square(gridref):
    with pytest.raises(bng.BNGError, match=r'Invalid 100 km grid square.*'):
        bng.to_osgb36(gridref)
