# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, pprint
from django.conf import settings
from django.core.urlresolvers import reverse


log = logging.getLogger(__name__)


class WidgetPrepper(object):
    """ Assists preparation of views.widgets() data. """

    def __init__(self):
        pass

    def build_context( self, widget, scheme, host ):
        """ Preps widget context.
            Called by views.widget() """
        log.debug( 'starting build_context()' )
        try:
            data_lst = json.loads( widget.data_points )
        except Exception as e:
            log.error( 'error loading widget data, ```{}```'.format(e) )
            context = { 'error': 'problem loading widget data; admin notified' }
            return context
        log.debug( 'data_lst loaded' )
        widget_url = '{scm}://{hst}{url}'.format( scm=scheme, hst=host, url=reverse('widget_url', kwargs={'identifier': widget.slug}) )
        log.debug( 'widget_url, ```{}```'.format(widget_url) )

        context = {
            'line_title': widget.title,  # the 'line' title; will appear in legend
            'chart_title': widget.title_info,
            'dashboard_info': settings.DOCUMENTATION_URL,
            'more_widget_info_url': '',
            'widget_url': widget_url,
            'widget_data_url': '{}?format=json'.format( widget_url ),
            'data': data_lst,
            # 'template_row_data': [ [0, 3974], [1, 2923], [2, 3138], [3, 1660], [4, 3631], [5, 3054] ],
            'template_row_data': self.make_template_row_data( data_lst ),
            'widget_tick_data': [ "{v:0, f:'2014-09'}", "{v:1, f:'2014-10'}", "{v:2, f:'2014-11'}", "{v:3, f:'2014-12'}", "{v:4, f:'2015-01'}", "{v:5, f:'2015-02'}" ],
            'max_y': 4172,  #5% over max count
            # 'max_y': 100000,
            }

        # context = {
        #     'line_title': widget.title,  # the 'line' title; will appear in legend
        #     'chart_title': 'monthly count of easyBorrow requests \\n(disposed of either through a josiah-redirect, or borrowdirect, or illiad)',
        #     'dashboard_info': settings.DOCUMENTATION_URL,
        #     'more_widget_info_url': '',
        #     'widget_url': widget_url,
        #     'widget_data_url': '{}?format=json'.format( widget_url ),
        #     'data': data_lst,
        #     'template_row_data': [ [0, 3974], [1, 2923], [2, 3138], [3, 1660], [4, 3631], [5, 3054] ],
        #     'widget_tick_data': [ "{v:0, f:'2014-09'}", "{v:1, f:'2014-10'}", "{v:2, f:'2014-11'}", "{v:3, f:'2014-12'}", "{v:4, f:'2015-01'}", "{v:5, f:'2015-02'}" ],
        #     'max_y': 4172,  #5% over max count
        #     # 'max_y': 100000,
        #     }
        log.debug( 'context, ```{}```'.format(pprint.pformat(context)) )
        return context

    def make_template_row_data( self, data_lst ):
        """ Creates the list of sub-lists for context['template_row_data'].
            Called by build_context() """
        log.debug( 'data_lst, ```{}```'.format( pprint.pformat(data_lst) ) )
        template_row_data_lst = [ [0, 3974], [1, 2923], [2, 3138], [3, 1660], [4, 3631], [5, 3054] ]
        return template_row_data_lst

    def build_json_widget_output( self, widget, callback, context ):
        """ Preps json for response.
            Called by views.widget() """
        output = json.dumps( context, sort_keys=True, indent=2 )
        if callback:
            output = '{v_callback}({v_output})'.format( v_callback=callback, v_output=output )
        return output
