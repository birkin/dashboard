# -*- coding: utf-8 -*-

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


def extractMinichartData( the_list ):
  '''
  - Called by: views.info()
  - Purpose: to extract 4 datapoints for a small googlechartapi image.
  '''
  list_length = len(the_list)
  if list_length < 5:
    return the_list
  first_position = 0
  if (list_length % 3) > 1:
    second_initial = (list_length // 3) + 1
  else:
    second_initial = (list_length // 3)
  second_position = second_initial - 1
  if ( (list_length * 2) % 3 ) > 1:
    third_initial = ( (list_length * 2) // 3 ) + 1
  else:
    third_initial = ( (list_length * 2) // 3 )
  third_position = third_initial - 1
  fourth_position = list_length - 1
  # make the list
  return_list = []
  return_list.append( the_list[first_position] )
  return_list.append( the_list[second_position] )
  return_list.append( the_list[third_position] )
  return_list.append( the_list[fourth_position] )
  # all set
  return return_list


def makeChartPercentages( data_list ):
  '''
  - Called by: views.info()
  - Purpose: to turn data-points into percentages for display in the google minichart
  '''
  high_number = max(data_list)
  high_number_divisor = high_number * .01
  return_dict = []
  for number in data_list:
    # print '\n- number is: %s' % number
    if high_number_divisor == 0:
      raw_percentage = 0
    else:
      raw_percentage = number / high_number_divisor
    # print '- raw_percentage is: %s' % raw_percentage
    rounded_raw_percentage = round( raw_percentage )
    # print '- rounded_raw_percentage is: %s' % rounded_raw_percentage
    return_dict.append( rounded_raw_percentage )
  # print '- return_dict is: %s' % return_dict
  return return_dict


def makeChartRanges( data_list ):
  '''
  - Called by: views.info()
  - Purpose: to turn percentage data-points into minimum and maximum ranges for display in the google minichart
  '''
  high = max(data_list) + 5
  low = min(data_list) - 5
  return [ low, high ]
