# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json


class WidgetPrepper(object):
    """ Assists preparation of views.widgets() data. """

    def __init__(self):
        pass

    def build_context( self, widget ):
        """ Preps widget context.
            Called by views.widget() """
        data_lst = json.loads( widget.data_points )
        context = {
            'contact_email': widget.data_contact_email_address,
            'data': data_lst
            }
        return context

    def build_json_widget_output( self, widget, callback, context ):
        """ Preps json for response.
            Called by views.widget() """
        output = json.dumps( context, sort_keys=True, indent=2 )
        if callback:
            output = '{v_callback}({v_output})'.format( v_callback=callback, v_output=output )
        return output

