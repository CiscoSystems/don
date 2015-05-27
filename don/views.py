from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import os
from .forms import PingForm


from plot import DotGenerator
import analyzer
import path

# Create your views here.

def index(request):
    return HttpResponse('I am DON')

def view(request):
    pwd = settings.BASE_DIR
    JSON_FILE = pwd + '/don/don.json'
    COMPUTE_DOT_FILE = pwd + '/don/static/compute.dot'
    COMPUTE_SVG_FILE = pwd + '/don/static/compute.svg'
    NETWORK_DOT_FILE = pwd + '/don/static/network.dot'
    NETWORK_SVG_FILE = pwd + '/don/static/network.svg'
    COMBINED_DOT_FILE = pwd + '/don/static/don.dot'
    COMBINED_SVG_FILE = pwd + '/don/static/don.svg'

    plotter = DotGenerator(JSON_FILE,
                           COMPUTE_DOT_FILE,
                           COMPUTE_SVG_FILE,
                           NETWORK_DOT_FILE,
                           NETWORK_SVG_FILE,
                           COMBINED_DOT_FILE,
                           COMBINED_SVG_FILE,
                           None
                           )
    plotter.plot_compute_node()
    plotter.generate_compute_svg()

    plotter.plot_network_node()
    plotter.generate_network_svg()

    plotter.plot_combined()
    plotter.generate_combined_svg()

    return HttpResponseRedirect('/static/view.html')

def analyze(request):
    pwd = settings.BASE_DIR
    JSON_FILE = pwd + '/don/don.json'

    params = {
            'error_file'        : pwd + '/don/static/don.error.txt',
            'test:all'          : True,
            'test:ping'         : False,
            'test:ping_count'   : 1,
            'test:ovs'          : True,
            'test:report_file'  : pwd + '/don/static/don.report.html',
            }

    analyzer.analyze(JSON_FILE, params)
    #output = analyzer.analyze(JSON_FILE, params)
    #html = '<html><body>Output: %s</body></html>' % output
    #return HttpResponse(html)
    return HttpResponseRedirect('/static/don.report.html')

def test(request):
    return HttpResponse('Testing the setup')

def ping(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            src_ip = form.cleaned_data['src_ip']
            dst_ip = form.cleaned_data['dst_ip']
            router = form.cleaned_data['router']
            #html = '<html><body>SIP: %s DIP: %s router: %s</body></html>' % (src_ip, dst_ip, router)
            #return HttpResponse(html)

            pwd = settings.BASE_DIR
            JSON_FILE = pwd + '/don/don.json'

            params = {
                    'json_file' : pwd + '/don/don.json',
                    'src_ip'    : src_ip,
                    'dst_ip'    : dst_ip,
                    'router'    : router,
                    'path_file' : pwd + '/don/static/ping.html',
                    'username'  : 'cirros',
                    'passwd'    : 'cubswin:)',
                    'count'     : 2,
                    'timeout'   : 2,
                    'debug'     : True,
                    'plot'      : False,
                    }
            path.path(params)

            JSON_FILE = pwd + '/don/don.json'
            COMPUTE_DOT_FILE  = None
            COMPUTE_SVG_FILE  = None
            NETWORK_DOT_FILE  = None
            NETWORK_SVG_FILE  = None
            COMBINED_DOT_FILE = pwd + '/don/static/ping.dot'
            COMBINED_SVG_FILE = pwd + '/don/static/ping.svg'
            HIGHLIGHT_FILE    = pwd + '/don/static/ping.html'

            plotter = DotGenerator(JSON_FILE,
                                   COMPUTE_DOT_FILE,
                                   COMPUTE_SVG_FILE,
                                   NETWORK_DOT_FILE,
                                   NETWORK_SVG_FILE,
                                   COMBINED_DOT_FILE,
                                   COMBINED_SVG_FILE,
                                   HIGHLIGHT_FILE,
                                   )
            plotter.plot_combined()
            plotter.generate_combined_svg()

            return HttpResponseRedirect('/static/path.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PingForm()

    return render(request, 'ping.html', {'form': form})

