import json, logging, os, pprint

from dashboard_app import models
from dashboard_app.lib.shib_auth import shib_login  # decorator
from dashboard_app.lib.widget_helper import WidgetPrepper
from dashboard_app.models import Widget
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

log = logging.getLogger(__name__)
# chart_maker = models.ChartMaker()
minichart_maker = models.MinichartMaker()
shib_view_helper = models.ShibViewHelper()
widget_helper = models.WidgetHelper()
widget_prepper = WidgetPrepper()


def info( request ):
    """ Returns info page. """
    return HttpResponse( 'This page will display "About" info, or redirect to the github ReadMe.' )


def widgets_redirect( request ):
    """ Redirects to all-widgets display. """
    return_url = reverse( "widgets_url", kwargs={"identifier": "all"} )
    log.debug( f'return_url, ```{return_url}```' )
    return HttpResponseRedirect( return_url )


def widgets( request, identifier ):
    """ Displays default page of widgets. """
    context = {}
    return render( request, 'dashboard_app_templates/widgets.html', context )
    # return HttpResponse( 'This page will display a summary "small-view" of all the widgets.' )


def widget( request, identifier ):
    """ Displays requested widget. """
    widget = get_object_or_404( Widget, slug=identifier )
    log.debug( 'widget found for identifier, `{}`'.format(identifier) )
    context = widget_prepper.build_context( widget, request.scheme, request.get_host() )
    if request.GET.get( 'format', None ) == 'json':
        output = widget_prepper.build_json_widget_output( widget, request.GET.get('callback', None), context )
        return HttpResponse( output, content_type = 'application/javascript; charset=utf-8' )
    else:
        return render( request, 'dashboard_app_templates/widget_detail.html', context )


def request_widget( request ):
    """ STUB
        Displays/handles form for requesting a widget. """
    return HttpResponse( 'This page will bring up a form for a user to request a widget.' )


def tag( request, tag ):
    """ STUB
        Displays set of widgets for given tag. """
    # minichart_data = minichart_maker.prep_data( json.loads(widget.data_points) )  # will be used here, not in widget view
    return HttpResponse( 'tag url' )


def bul_search( request ):
    """ Triggered by user entering search term into banner-search-field.
        Redirects query to search.library.brown.edu """
    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    redirect_url = 'https://search.library.brown.edu?%s' % request.META['QUERY_STRING']
    return HttpResponseRedirect( redirect_url )


@shib_login
def login( request ):
    """ Handles authNZ, & redirects to admin.
        Called by click on login or admin link. """
    next_url = request.GET.get( 'next', None )
    if not next_url:
        redirect_url = reverse( 'admin:bul_cbp_app_tracker_changelist' )
    else:
        redirect_url = request.GET['next']  # will often be same page
    return HttpResponseRedirect( redirect_url )


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
