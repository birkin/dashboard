import json, logging, os, pprint

from dashboard_app import models, settings_app
from dashboard_app.lib import misc
from dashboard_app.lib.shib_auth import shib_login  # decorator
from dashboard_app.lib.widget_helper import WidgetPrepper
from dashboard_app.models import Tag, Widget
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

log = logging.getLogger(__name__)
# chart_maker = models.ChartMaker()
minichart_maker = misc.MinichartMaker()
shib_view_helper = models.ShibViewHelper()
widget_helper = models.WidgetHelper()
widget_prepper = WidgetPrepper()


def info( request ):
    """ Returns info page. """
    log.debug( '\n\nstarting info()' )
    widget = Widget.objects.get( id=1 )
    trend_direction_dict = { 1:'up', -1:'down', 0:'flat' }
    trend_color_dict = { 1:'blue', -1:'red', 0:'blank' }
    minichart_dcts = misc.extractMinichartData( eval(widget.data_points) )
    # minichart_values = [ minichart_tuples[0][1], minichart_tuples[1][1], minichart_tuples[2][1], minichart_tuples[3][1]  ]
    minichart_values = []
    for dct in minichart_dcts:
        value = list( dct.items() )[0][1]
        minichart_values.append( value )
    minichart_percentages = misc.makeChartPercentages( minichart_values )
    minichart_range = misc.makeChartRanges( minichart_percentages )
    widget_detail_url = reverse( "widget_detail_url", kwargs={"identifier": "foo"} )
    widget_detail_url_root = widget_detail_url.replace( 'foo/', '' )
    # trend_image_url = f'{}/images/{trend_direction}_{trend_color}.png'
    log.debug( f'widget.trend_direction, `{widget.trend_direction}`; widget.trend_color, `{widget.trend_color}`' )
    trend_image = f'{trend_direction_dict[widget.trend_direction]}_{trend_color_dict[widget.trend_color]}.png'
    log.debug( f'trend_image, `{trend_image}`' )
    page_dict = {
        'trend_image': trend_image,
        'media_directory':project_settings.MEDIA_URL,
        'widget':widget,
        'trend_direction':trend_direction_dict[ widget.trend_direction ],
        'trend_color':trend_color_dict[ widget.trend_color ],
        'minichart_percentages':minichart_percentages,
        'minichart_range':minichart_range,
        'widget_detail_url_root': widget_detail_url_root
        }
    return render( request, 'dashboard_app_templates/info.html', page_dict )


def widgets_redirect( request ):
    """ Redirects to all-widgets display. """
    return_url = reverse( "widgets_url", kwargs={"identifier": "all"} )
    log.debug( f'return_url, ```{return_url}```' )
    return HttpResponseRedirect( return_url )


def widgets( request, identifier ):
    """ Displays default page of widgets. """
    context = {}
    # get widgets
    widgets = []
    if identifier == 'all':
        query = Widget.objects.all()
    else:
        tag = Tag.objects.get( slug=identifier )
        query = tag.widget_set.all().order_by('title')
    for widget in query:
        if 'INVALID_DATA' not in widget.data_points:
            widgets.append( widget )
    tags = Tag.objects.all()
    page_dict = {
        'media_directory':project_settings.MEDIA_URL,
        'project_settings':project_settings,
        'widget_settings':settings_app,
        'widgets':widgets,
        'tags':tags,
        }
    # return render_to_response( 'dashboard/widget_list.html', page_dict )
    return render( request, 'dashboard_app_templates/widget_list.html', page_dict )


def widget_detail( request, identifier, data_index=0 ):
    """ Displays requested widget.
        TODO -- only go through the detailchart_tuples (which aren't tuples) once, and break out the key/values in the same loop. """
    widget = get_object_or_404( Widget, slug=identifier )
    log.debug( 'widget found for identifier, `{}`'.format(identifier) )
    detailchart_tuples = eval( widget.data_points )

    detailchart_values = []
    for element_dct in detailchart_tuples:
        value = list( element_dct.items() )[0][1]
        detailchart_values.append( value )

    detailchart_percentages = misc.makeChartPercentages( detailchart_values )
    detailchart_range = misc.makeChartRanges( detailchart_percentages )

    detailchart_keys = []
    for element_dct in detailchart_tuples:
        key = list( element_dct.items() )[0][0]
        detailchart_keys.append( key )

    page_dict = {
        'host': 'FOO_HOST',
        'widget': widget,
        'detailchart_percentages': detailchart_percentages,
        'detailchart_range': detailchart_range,
        'detailchart_keys': detailchart_keys,
        'detailchart_values': detailchart_values,
        'data_index':int(data_index)
        # 'data_index':int(data_index) - 1 # so url can look 1-based, whereas google chart-api is zero-based
        }
    return render( request, 'dashboard_app_templates/widget_detail.html', page_dict )


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
