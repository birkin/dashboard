# -*- coding: utf-8 -*-

import logging
import numpy
# from dashboard_app.models import Widget, WidgetHelper, ChartMaker, MinichartMaker
from django.test import TestCase
from dashboard_app.models import Widget, WidgetHelper
from dashboard_app.lib import misc


log = logging.getLogger(__name__)

widget_helper = WidgetHelper()


class SlopeCalculatorTest(TestCase):
    """ Tests lib.misc.calculate_slope() """

    def test_calculate_slope__simple(self):
        """ Tests simple array. """
        x_list = [ 1, 2, 3 ]
        y_list = [ 1, 2, 3 ]
        return_dct = misc.calculate_slope( x_list, y_list )
        self.assertEqual( int, type(return_dct['slope_rounded']) )
        self.assertEqual( numpy.float64, type(return_dct['slope']) )
        self.assertEqual( {'slope': 1.0, 'slope_rounded': 1}, return_dct  )

    def test_calculate_slope__real(self):
        """ Tests simple array. """
        x_list = [ 0, 1, 2, 3, 4, 5 ]
        y_list = [ 3974, 2923, 3138, 1660, 3631, 3054 ]
        self.assertEqual( {'slope': -112.97142857142858, 'slope_rounded': -113}, misc.calculate_slope(x_list, y_list) )

    # end class SlopeCalculatorTest


class WidgetHelperTest(TestCase):
    """ Tests for non-django models.WidgetHelper() """

    def test_validate_data__good_json(self):
        """ Checks good json detection. """
        jsn = '[ {"97/98": 183179}, {"98/99": 178095}, {"99/00": 172425}, {"00/01": 159397}, {"01/02": 168697}, {"02/03": 191740}, {"03/04": 188981}, {"04/05": 188298}, {"05/06": 198735}, {"06/07": 183533} ]'
        self.assertEqual( True, widget_helper.validate_data(jsn) )

    def test_validate_data__bad_json(self):
        """ Checks bad json detection. """
        jsn = '[ {"97/98": zzz 183179}, {"98/99": 178095} ]'
        try:
            validity = widget_helper.validate_data(jsn)
        except Exception as e:
            # print( 'oops!, ```{}```'.format(e) )
            validity = False
        self.assertEqual( False, validity )

    # def test_process_data(self):
    #     """ Tests process_data(). """
    #     w = Widget()
    #     w.best_goal = 1  # best is higher -- think higher circulation being good
    #     w.data_points = '[ {"97/98": 183179}, {"98/99": 178095}, {"99/00": 172425}, {"00/01": 159397}, {"01/02": 168697}, {"02/03": 191740}, {"03/04": 188981}, {"04/05": 188298}, {"05/06": 198735}, {"06/07": 183533} ]'
    #     processed_w = widget_helper.process_data( w )
    #     ## baseline
    #     self.assertEqual( 183179, processed_w.baseline_value )
    #     ## best
    #     self.assertEqual( 198735, processed_w.best_value )
    #     ## current
    #     self.assertEqual( 183533, processed_w.current_value )
    #     ## trend direction
    #     self.assertEqual( -1, processed_w.trend_direction )
    #     ## trend color
    #     self.assertEqual( -1, processed_w.trend_color )
    #     ## tests 'best' when best is 'lower', think missing books
    #     w2 = Widget()
    #     w2.best_goal = -1
    #     w2.data_points = '[ {"97/98": 183179}, {"98/99": 178095}, {"99/00": 172425}, {"00/01": 159397}, {"01/02": 168697}, {"02/03": 191740}, {"03/04": 188981}, {"04/05": 188298}, {"05/06": 198735}, {"06/07": 183533} ]'
    #     processed_w2 = widget_helper.process_data( w2 )
    #     ## best
    #     self.assertEqual( 159397, processed_w2.best_value )

    # end class WidgetHelperTest


# class ChartMakerTest(TestCase):
#     """ Tests for non-django models.ChartMaker() """

#     def test_make_percentages(self):
#         """ Tests example lists. """
#         cm = ChartMaker()
#         lst = [ 1, 2, 3, 4, 5, 6, 7 ]
#         self.assertEqual(
#             [ 14.0, 29.0, 43.0, 57.0, 71.0, 86.0, 100.0 ], cm.make_percentages(lst) )

#     # end class ChartMakerTest


# class MinichartMakerTest(TestCase):
#     """ Tests for non-django models.MinichartMaker() """

#     def test_extract_minichart_data(self):
#         """ Tests the four expected datapoints. """
#         minichart_maker = MinichartMaker()
#         lst = [ 1, 2, 3, 4, 5, 6, 7 ]
#         self.assertEqual(
#             [ 1, 3, 5, 7 ], minichart_maker.extract_data_elements(lst) )
#         lst = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
#         self.assertEqual(
#             [ 1, 4, 7, 10 ], minichart_maker.extract_data_elements(lst) )
#         lst = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ]
#         self.assertEqual(
#             [ 1, 4, 8, 11 ], minichart_maker.extract_data_elements(lst) )
#         lst = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ]
#         self.assertEqual(
#             [ 1, 5, 9, 12 ], minichart_maker.extract_data_elements(lst) )

#     # end class MinichartMakerTest
