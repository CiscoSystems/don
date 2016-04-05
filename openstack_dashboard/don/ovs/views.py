from horizon import views
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from plot import DotGenerator
import os,subprocess
from .forms import PingForm
from django.shortcuts import render_to_response
from horizon import messages

import analyzer
# import path


from django.shortcuts import render

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'don/ovs/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


def index(request):
    return HttpResponse('I am DON')


def view(request):
    # import pdb
    # pdb.set_trace()
    pwd = settings.ROOT_PATH#+'/openstack_dashboard/dashboards/admin/don/'

    JSON_FILE = pwd + '/don/ovs/don.json'
    static_path = settings.STATIC_URL
    '''
    COMPUTE_DOT_FILE = pwd + '/don/ovs/static/compute.dot'
    COMPUTE_SVG_FILE = pwd + '/don/ovs/static/compute.svg'
    NETWORK_DOT_FILE = pwd + '/don/ovs/static/network.dot'
    NETWORK_SVG_FILE = pwd + '/don/ovs/static/network.svg'
    COMBINED_DOT_FILE = pwd + '/don/ovs/static/don.dot'
    COMBINED_SVG_FILE = pwd + '/don/ovs/static/don.svg'
    '''
    COMPUTE_DOT_FILE = pwd + '/static/don/compute.dot'
    COMPUTE_SVG_FILE = pwd + '/static/don/compute.svg'
    NETWORK_DOT_FILE = pwd + '/static/don/network.dot'
    NETWORK_SVG_FILE = pwd + '/static/don/network.svg'
    COMBINED_DOT_FILE = pwd + '/static/don/don.dot'
    COMBINED_SVG_FILE = pwd + '/static/don/don.svg'
    
    macro = {}
    # return HttpResponseRedirect('static/view.html')

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
    # return HttpResponseRedirect('static/view.html')
    return render(request,"don/ovs/views.html", macro)

def analyze(request):
    # pwd = settings.BASE_DIR
    pwd = settings.ROOT_PATH
    JSON_FILE = pwd + '/don/ovs/don.json'

    params = {
            'error_file'        : pwd + '/don/templates/don/don.error.txt',
            'test:all'          : True,
            'test:ping'         : False,
            'test:ping_count'   : 1,
            'test:ovs'          : True,
            'test:report_file'  : pwd + '/don/templates/don/don.report.html',
            }
    print "params ====> ",params
    analyzer.analyze(JSON_FILE, params)
    #output = analyzer.analyze(JSON_FILE, params)
    #html = '<html><body>Output: %s</body></html>' % output
    #return HttpResponse(html)
    # return HttpResponseRedirect('/static/don.report.html')
    return render(request,"don/ovs/analyze.html")
    # return render_to_response('don/ovs/analyze.html')

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
            JSON_FILE = pwd + '/ovs/don.json'

            params = {
                    'json_file' : pwd + '/ovs/don.json',
                    'src_ip'    : src_ip,
                    'dst_ip'    : dst_ip,
                    'router'    : router,
                    'path_file' : pwd + '/ovs/static/ping.html',
                    'username'  : 'cirros',
                    'passwd'    : 'cubswin:)',
                    'count'     : 2,
                    'timeout'   : 2,
                    'debug'     : True,
                    'plot'      : False,
                    }
            path.path(params)

            JSON_FILE = pwd + '/ovs/don.json'
            COMPUTE_DOT_FILE  = None
            COMPUTE_SVG_FILE  = None
            NETWORK_DOT_FILE  = None
            NETWORK_SVG_FILE  = None
            COMBINED_DOT_FILE = pwd + '/ovs/static/ping.dot'
            COMBINED_SVG_FILE = pwd + '/ovs/static/ping.svg'
            HIGHLIGHT_FILE    = pwd + '/ovs/static/ping.html'

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

    return render(request, 'don/ovs/ping.html', {'form': form})


def collect(request):
    macro = {'collect_status':'Collection failed'}
    status = 0
    
    BASE_DIR = settings.ROOT_PATH
    CUR_DIR = os.getcwd()
    os.chdir(BASE_DIR + '/don/ovs')
    cmd = 'sudo python collector.py'
    ps = subprocess.Popen('sudo python collector.py',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print ps
    for line in iter(ps.stdout.readline, ''):
        print line
        if line.startswith('STATUS:') and line.find('Writing collected info'):
            status = 1
            macro['collect_status'] = "Collecton successful. Click visualize to display"

    # res = collector.main()
    os.chdir(BASE_DIR)
    # return render(request,'static/don.html',macro)
    if status:
      messages.success(request, macro['collect_status'])
    else:
      messages.error(request,macro['collect_status'])
    return render(request,"don/ovs/index.html", macro)
