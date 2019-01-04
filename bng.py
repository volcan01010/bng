# -*- coding: utf-8 -*-
# ##########################################################################
#
#  COPYRIGHT:  (C) 2012-2019 John A Stevenson / @volcan01010
#                            Magnus Hagdorn / @mhagdorn
#                            Jumy Elǝrossë / @realjumy
#  WEBSITE: http://all-geo.org/volcan01010
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  http://www.gnu.org/licenses/gpl-3.0.html
#
# ############################################################################

import re

try:
    import numpy as np
except ImportError:
    msg = ("Numpy not installed.  Numpy comes with most scientific/geospatial"
           " Python packages.")
    raise ImportError(msg)

__version__ = '1.0.0'
__all__ = ['to_osgb36', 'from_osgb36']


class BNGError(Exception):
    """Exception raised by bng.py module"""
    pass


# Region codes for 100 km grid squares.
_regions = [['HL', 'HM', 'HN', 'HO', 'HP', 'JL', 'JM'],
            ['HQ', 'HR', 'HS', 'HT', 'HU', 'JQ', 'JR'],
            ['HV', 'HW', 'HX', 'HY', 'HZ', 'JV', 'JW'],
            ['NA', 'NB', 'NC', 'ND', 'NE', 'OA', 'OB'],
            ['NF', 'NG', 'NH', 'NJ', 'NK', 'OF', 'OG'],
            ['NL', 'NM', 'NN', 'NO', 'NP', 'OL', 'OM'],
            ['NQ', 'NR', 'NS', 'NT', 'NU', 'OQ', 'OR'],
            ['NV', 'NW', 'NX', 'NY', 'NZ', 'OV', 'OW'],
            ['SA', 'SB', 'SC', 'SD', 'SE', 'TA', 'TB'],
            ['SF', 'SG', 'SH', 'SJ', 'SK', 'TF', 'TG'],
            ['SL', 'SM', 'SN', 'SO', 'SP', 'TL', 'TM'],
            ['SQ', 'SR', 'SS', 'ST', 'SU', 'TQ', 'TR'],
            ['SV', 'SW', 'SX', 'SY', 'SZ', 'TV', 'TW']]
# Reshuffle so indices correspond to offsets
_regions = np.array([_regions[x] for x in range(12, -1, -1)])
_regions = _regions.transpose()


def to_osgb36(gridref):
    """Reformat British National Grid references to OSGB36 numeric coordinates.
    Grid references can be 4, 6, 8 or 10 figures.  Returns a tuple of x, y.

    Examples:

    Single value
    >>> to_osgb36('NT2755072950')
    (327550, 672950)

    For multiple values, use the zip function
    >>> gridrefs = ['HU431392', 'SJ637560', 'TV374354']
    >>> xy=to_osgb36(gridrefs)
    >>> x, y = zip(*xy)
    >>> x
    (443100, 363700, 537400)
    >>> y
    (1139200, 356000, 35400)
    """
    # Process iterables
    if isinstance(gridref, list):
        return [to_osgb36(c) for c in gridref]
    elif isinstance(gridref, tuple):
        return tuple([to_osgb36(c) for c in gridref])
    elif isinstance(gridref, type(np.array('string'))):
        return np.array([to_osgb36(str(c)) for c in list(gridref)])

    # Catch invalid input
    bad_input_message = (
        'Valid gridref inputs are 4, 6, 8 or 10-fig references as strings '
        'e.g. "NN123321", or lists/tuples/arrays of strings. '
        '[{}]'.format(gridref))
    try:
        if not re.match(r'^[A-Za-z]{2}(\d{4}|\d{6}|\d{8}|\d{10})$', gridref):
            raise BNGError(bad_input_message)
    except TypeError:
        # Non-string values will throw error
        raise BNGError(bad_input_message)

    # Process grid reference
    region = gridref[0:2].upper()
    x_box, y_box = np.where(_regions == region)
    try:  # Catch bad region codes
        # Convert index in 'regions' to offset
        x_offset = 100000 * x_box[0]
        y_offset = 100000 * y_box[0]
    except IndexError:
        raise BNGError('Invalid 100 km grid square code: {}'.format(region))
    figs = int((len(gridref) - 2) / 2.0)
    factor = 10 ** (5 - figs)
    x, y = (int(gridref[2:2 + figs]) * factor + x_offset,
            int(gridref[2 + figs:2 + 2 * figs]) * factor + y_offset)
    return x, y


def from_osgb36(coords, figs=6):
    """Reformat osgb36 numeric coordinates to British National Grid references.
    Grid references can be 4, 6, 8 or 10 fig, specified by the figs keyword.

    Examples:

    Single value
    >>> from_osgb36((327550, 672950))
    'NT275729'

    For multiple values, use the zip function to create list of tuples
    >>> x = [443143, 363723, 537395]
    >>> y = [1139158, 356004, 35394]
    >>> xy = list(zip(x, y))
    >>> from_osgb36(xy, figs=4)
    ['HU4339', 'SJ6356', 'TV3735']
    """
    # Process items individually if a list if passed
    if isinstance(coords, list):
        return [from_osgb36(c, figs=figs) for c in coords]

    # Throw error if other input is bad
    bad_input_message = ('Valid inputs are x, y tuple e.g. (651409, 313177),'
                         ' or list of x, y tuples. [{}]'.format(coords))

    if not isinstance(coords, tuple):
        raise BNGError(bad_input_message)

    try:
        x, y = coords
    except ValueError:
        raise BNGError(bad_input_message)

    out_of_region_message = (
        'Coordinate location outside UK region: {}'.format(coords))
    if (x < 0) or (y < 0):
        raise BNGError(out_of_region_message)

    # Convert offset to index in 'regions'
    x_box = int(np.floor(x / 100000.0))
    y_box = int(np.floor(y / 100000.0))
    x_offset = 100000 * x_box
    y_offset = 100000 * y_box
    try:  # Catch coordinates outside the region
        region = _regions[x_box, y_box]
    except IndexError:
        raise BNGError(out_of_region_message)

    # Format the output based on figs
    formats = {4: '%s%02i%02i', 6: '%s%03i%03i', 8: '%s%04i%04i',
               10: '%s%05i%05i'}
    factors = {4: 1000.0, 6: 100.0, 8: 10.0, 10: 1.0}
    try:  # Catch bad number of figures
        coords = formats[figs] % (
            region, np.floor((x - x_offset) / factors[figs]),
            np.floor((y - y_offset) / factors[figs]))
    except KeyError:
        raise BNGError('Valid inputs for figs are 4, 6, 8 or 10')
    return coords
