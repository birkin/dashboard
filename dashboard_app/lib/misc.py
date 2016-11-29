# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals

import numpy


def calculate_slope( x_list, y_list ):
    """ Returns slope, calculated to nearest integer.
        - x_list is simply a series representing the x-value, on a chart, of a date, so it'll be [0, 1, 2, etc].
        - y_list is the array of count values.
        - from <http://stackoverflow.com/a/33873984>
          - confirmed via <http://stackoverflow.com/a/33843502> after downloading and running scipy with tests.py data:
            >>> from scipy.stats import linregress
            >>> linregress( x_list, y_list )
        Called by something or other. """
    x = numpy.array( x_list )
    y = numpy.array( y_list )
    slope_float = ( (len(x)*sum(x*y)) - (sum(x)*sum(y)) ) / ( len(x)*(sum(x**2))-(sum(x)**2) )
    slope_int = int( round(slope_float, 0) )
    return_dct = { 'slope': slope_float, 'slope_rounded': slope_int }
    return return_dct
