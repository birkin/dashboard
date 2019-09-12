import json, logging


log = logging.getLogger(__name__)


class WidgetHelper( object ):
    """ Contains helpers for processing Widget() data. """

    # def process_data( self, widget ):
    #     """ Ensures data points are valid, and calculates and sets values for certain fields.
    #         Called by Widget.save() """
    #     self.validate_data( widget.data_points )
    #     # widget.baseline_value = lst[0].values()[0]
    #     # log.debug( 'hereA' )
    #     # widget.best_value = self.get_best_value( widget.best_goal, lst )
    #     # widget.current_value = lst[-1].values()[0]
    #     # widget.trend_direction = self.get_trend_direction( widget.current_value, lst )
    #     # widget.trend_color = self.get_trend_color( widget.trend_direction, widget.best_goal )
    #     log.debug( 'dir(widget), `{}`'.format( dir(widget) ) )
    #     return widget

    def process_data( self, widget_instance ):
      '''
      - Called by: models.Widget()
      - Purpose: to turn the input list of tuples into appropriate values.
      '''

      try:

        # a bit of cleanup in case user entered data with returns
        # print '- widget_instance.data_points is: %s' % widget_instance.data_points
        start_data = widget_instance.data_points
        # print '- start_data is: %s' % start_data
        # print '--'
        # print '\r' in start_data
        # print '--'
        start_data.replace( '\r\n', '' ) # none of this works (trying to allow data with newlines to be pasted in; don't seem to be able to remove 'em)
        start_data.replace( '\n', '' )
        start_data.replace( '\r', '' )
        start_data.replace( '\r', '' )
        start_data.replace( '\r', '' )
        # print '- start_data is now: %s' % start_data
        # print '--'
        # print '\r' in start_data
        # print '--'
        # print '- type(start_data) is: %s' % type(start_data)
        widget_instance.data_points = start_data
        # print '- widget_instance.data_points is: %s' % widget_instance.data_points
        # data = eval( widget_instance.data_points )
        data = json.loads( widget_instance.data_points )
        # print '- data is: %s' % data
        widget_instance.best_goal = int( widget_instance.best_goal ) # dunno why this was a unicode value; should've been an int; this fixes

        # baseline value
        # first_tuple = data[0]
        # widget_instance.baseline_value = first_tuple[1]
        first_dct = data[0]
        (key, value) = list( first_dct.items() )[0]
        log.debug( f'value, `{value}`' )
        widget_instance.baseline_value = value

        # 'best' value
        best_value = None
        if widget_instance.best_goal == 1:  # best is higher
          for the_tuple in data:
            if best_value == None:
              best_value = the_tuple[1]
            if the_tuple[1] > best_value:
              best_value = the_tuple[1]
        else:                               # best is lower
          for the_tuple in data:
            if best_value == None:
              best_value = the_tuple[1]
            if the_tuple[1] < best_value:
              best_value = the_tuple[1]
        widget_instance.best_value = best_value
        # best_value = None
        # for the_tuple in data:
        #   if best_value == None:
        #     best_value = the_tuple[1]
        #   if the_tuple[1] > best_value:
        #     best_value = the_tuple[1]
        # widget_instance.best_value = best_value

        # current value
        last_tuple = data[ len(data)-1 ]
        widget_instance.current_value = last_tuple[1]

        # trend value
        next_to_last_tuple = data[ len(data)-2 ]
        previous_value = next_to_last_tuple[1]
        if widget_instance.current_value > previous_value:
          widget_instance.trend_direction = 1
        elif widget_instance.current_value == previous_value:
          widget_instance.trend_direction = 0
        else:
          widget_instance.trend_direction = -1

        # trend color
        if widget_instance.trend_direction == 0:
          widget_instance.trend_color = 0
        elif widget_instance.trend_direction == widget_instance.best_goal:
          widget_instance.trend_color = 1
        else:
          widget_instance.trend_color = -1

        # all set
        return widget_instance

      except Exception as e:
        log.exception( 'problem in processData(); traceback follows' )
        raise Exception('problem with entered data; check it')

      # end def processData()


    def validate_data( self, data ):
        """ Ensures data is a list of dicts.
            Called by process_data() """
        validity = False
        try:
            lst = json.loads( data )
            for dct in lst:
                assert type( dct ) == dict
            validity = True
        except Exception as e:
            log.error( 'error validating data on save; exception, ```{ex}```; problematic data, ```{da}```'.format( ex=e, da=data ) )
            raise Exception( 'bad_data' )  # needed for model's try-except block to trigger
        log.debug( 'validity, `{}`'.format(validity) )
        return validity

    ## end class WidgetHelper
