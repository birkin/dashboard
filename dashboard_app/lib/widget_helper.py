# -*- coding: utf-8 -*-


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
            'data_contact_name': widget.data_contact_name,
            'data_contact_email': widget.data_contact_email_address,
            'line_title': widget.title,  # the 'line' title; will appear in legend
            'chart_title': widget.title_info,
            'dashboard_info': settings.DOCUMENTATION_URL,
            'more_widget_info_url': widget.more_info_url,
            'widget_url': widget_url,
            'widget_data_url': '{}?format=json'.format( widget_url ),
            'data': data_lst,
            # 'template_row_data': [ [0, 3974], [1, 2923], [2, 3138], [3, 1660], [4, 3631], [5, 3054] ],
            'template_row_data': self.make_template_row_data( data_lst ),
            # 'widget_tick_data': [ "{v:0, f:'2014-09'}", "{v:1, f:'2014-10'}", "{v:2, f:'2014-11'}", "{v:3, f:'2014-12'}", "{v:4, f:'2015-01'}", "{v:5, f:'2015-02'}" ],
            'widget_tick_data': self.make_widget_tick_data( data_lst ),
            #
            'max_y': self.make_max_count( data_lst ),
            # 'max_y': 100000,
            }
        log.debug( 'context, ```{}```'.format(pprint.pformat(context)) )
        return context

        # end def build_context()

    def make_template_row_data( self, data_lst ):
        """ Creates the list of sub-lists for context['template_row_data'].
            So for `[ {'Jan': 20}, {'Feb':25} ]`, the return would be `[ [0, 20], [1, 25] ]`,
            Called by build_context() """
        log.debug( 'data_lst, ```{}```'.format( pprint.pformat(data_lst) ) )
        new_lst = []
        for ( i, mini_dct) in enumerate( data_lst ):
            kv_tpl = list( mini_dct.items() )[0]
            ( label, value ) = ( kv_tpl[0], kv_tpl[1] )
            new_lst.append( [i, value] )
        log.debug( 'new_lst, ```{}```'.format( pprint.pformat(new_lst) ) )
        return new_lst

    def make_widget_tick_data( self, data_lst ):
        """ Creates the list of mini_dcts for context['widget_tick_data'], for the x-axis labels.
            So for `[ {'Jan': 20}, {'Feb':25} ]`, the return would be, as odd as this appears, `[ "{v:0, f:'Jan'}", "{v:1, f:'Jan'}" ]`,
            Called by build_context() """
        log.debug( 'data_lst, ```{}```'.format( pprint.pformat(data_lst) ) )
        new_lst = []
        for ( i, mini_dct) in enumerate( data_lst ):
            kv_tpl = list( mini_dct.items() )[0]
            ( label, value ) = ( kv_tpl[0], kv_tpl[1] )
            weird_string = "{v:%s, f:'%s'}" % ( i, label )
            new_lst.append( weird_string )
        log.debug( 'new_lst, ```{}```'.format( pprint.pformat(new_lst) ) )
        return new_lst

    def make_max_count( self, data_lst ):
        """ Creates the int for build_context['max_y'].
            Called by build_context() """
        log.debug( 'data_lst, ```{}```'.format( pprint.pformat(data_lst) ) )
        max_count = 0
        for mini_dct in data_lst:
            kv_tpl = list( mini_dct.items() )[0]
            ( label, value ) = ( kv_tpl[0], kv_tpl[1] )
            if value > max_count:
                max_count = value
        max_count_plus = max_count + (max_count * .05)
        log.debug( 'max_count_plus, ```{}```'.format(max_count_plus) )
        return max_count_plus

    def build_json_widget_output( self, widget, callback, context ):
        """ Preps json for response.
            Called by views.widget() """
        output = json.dumps( context, sort_keys=True, indent=2 )
        if callback:
            output = '{v_callback}({v_output})'.format( v_callback=callback, v_output=output )
        return output
