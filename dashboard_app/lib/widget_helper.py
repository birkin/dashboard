# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, pprint
from django.core.urlresolvers import reverse


log = logging.getLogger(__name__)


class WidgetPrepper(object):
    """ Assists preparation of views.widgets() data. """

    def __init__(self):
        pass

    def build_context( self, widget, scheme, host ):
        """ Preps widget context.
            Called by views.widget() """
        data_lst = json.loads( widget.data_points )
        context = {
            'title': widget.title,
            'contact_email': 'birkin_diana@brown.edu',
            'more_info_url': '',
            'widget_url': '{scm}://{hst}/{url}'.format( scm=scheme, hst=host, url=reverse('widget_url', kwargs={'identifier': widget.slug}) ),
            'data': data_lst
            }
        log.debug( 'context, ```{}```'.format(pprint.pformat(context)) )
        return context

    def build_json_widget_output( self, widget, callback, context ):
        """ Preps json for response.
            Called by views.widget() """
        output = json.dumps( context, sort_keys=True, indent=2 )
        if callback:
            output = '{v_callback}({v_output})'.format( v_callback=callback, v_output=output )
        return output

