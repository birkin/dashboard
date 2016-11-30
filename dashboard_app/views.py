# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, os, pprint
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from dashboard_app import models
from dashboard_app.models import Widget

log = logging.getLogger(__name__)
shib_view_helper = models.ShibViewHelper()
widget_helper = models.WidgetHelper()
chart_maker = models.ChartMaker()
minichart_maker = models.MinichartMaker()


def info( request ):
    """ Returns info page. """
    return HttpResponse( 'This page will display "About" info, or redirect to the github ReadMe.' )


def widgets( request ):
    """ Displays default page of widgets. """
    return HttpResponse( 'This page will display a summary "small-view" of all the widgets.' )


def widget( request, identifier ):
    """ Displays requested widget. """
    widget = get_object_or_404( Widget, slug=identifier )
    log.debug( 'widget found for identifier, `{}`'.format(identifier) )
    # ( chart_values, chart_percentages, chart_range, chart_keys ) = chart_maker.prep_data( widget.data_points )
    # gchart_detail_url = chart_maker.prep_gchart_detail_url()
    jdict = widget.get_jdict( request.build_absolute_uri() )
    if request.GET.get( 'format', None ) == 'json':
        output = json.dumps( jdict, sort_keys=True, indent=2 )
        if request.GET.get( 'callback', None ):
            output = '%s(%s)' % ( request.GET.get('callback'), output )
        return HttpResponse( output, content_type = 'application/javascript; charset=utf-8' )
    else:
        # return HttpResponse( jdict['data_main']['title'] )
        # context = {
        #     'widget': widget,
        #     'detailchart_percentages': chart_percentages,
        #     'detailchart_range': chart_range,
        #     'detailchart_keys': chart_keys,
        #     'data_index': 0  # so url can look 1-based, whereas google chart-api is zero-based
        #     }
        context = {}
        return render( request, 'dashboard_app_templates/widget_detail.html', context )


    # widget_instance = Widget.objects.get( slug=identifier )

    # detailchart_tuples = eval( widget_instance.data_points )

    # detailchart_values = []
    # for element in detailchart_tuples:
    #     detailchart_values.append( element[1] )

    # detailchart_percentages = utility_code.makeChartPercentages( detailchart_values )

    # detailchart_range = utility_code.makeChartRanges( detailchart_percentages )

    # detailchart_keys = []
    # for element in detailchart_tuples:
    #     detailchart_keys.append( element[0] )

    # page_dict = {
    #     'host':settings_app.HOST_URL_BASE,
    #     'widget':widget_instance,
    #     'detailchart_percentages':detailchart_percentages,
    #     'detailchart_range':detailchart_range,
    #     'detailchart_keys':detailchart_keys,
    #     'detailchart_values':detailchart_values,
    #     'data_index':int(data_index)
    #     # 'data_index':int(data_index) - 1 # so url can look 1-based, whereas google chart-api is zero-based
    #     }
    # return render_to_response( 'dashboard/info.html', page_dict )


def request_widget( request ):
    """ STUB
        Displays/handles form for requesting a widget. """
    return HttpResponse( 'This page will bring up a form for a user to request a widget.' )


def tag( request, tag ):
    """ STUB
        Displays set of widgets for given tag. """
    # minichart_data = minichart_maker.prep_data( json.loads(widget.data_points) )  # will be used here, not in widget view
    return HttpResponse( 'tag url' )


def shib_login( request ):
    """ Examines shib headers, sets session-auth, & returns user to request page. """
    log.debug( 'in views.shib_login(); starting' )
    if request.method == 'POST':  # from request_login.html
        log.debug( 'in views.shib_login(); post detected' )
        return HttpResponseRedirect( os.environ['DSHBRD__SHIB_LOGIN_URL'] )  # forces reauth if user clicked logout link
    request.session['shib_login_error'] = ''  # initialization; updated when response is built
    ( validity, shib_dict ) = shib_view_helper.check_shib_headers( request )
    return_url = request.GET.get('return_url', reverse('info_url') )
    return_response = shib_view_helper.build_response( request, validity, shib_dict, return_url )
    log.debug( 'in views.shib_login(); about to return response' )
    return return_response


def shib_logout( request ):
    """ Clears session, hits shib logout, and redirects user to landing page. """
    request.session['authz_info']['authorized'] = False
    logout( request )
    scheme = 'https' if request.is_secure() else 'http'
    redirect_url = '%s://%s%s' % ( scheme, request.get_host(), reverse('request_url') )
    if request.get_host() == '127.0.0.1' and project_settings.DEBUG == True:
        pass
    else:
        encoded_redirect_url =  urlquote( redirect_url )  # django's urlquote()
        redirect_url = '%s?return=%s' % ( os.environ['DSHBRD__SHIB_LOGOUT_URL_ROOT'], encoded_redirect_url )
    log.debug( 'in vierws.shib_logout(); redirect_url, `%s`' % redirect_url )
    return HttpResponseRedirect( redirect_url )
