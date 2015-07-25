from django.http import HttpResponse
from django.template import RequestContext, loader


# # Create your views here.

# def index(request):
#     template = loader.get_template('markov/index.html')
#     return HttpResponse(template.render())


from django.shortcuts import render_to_response, RequestContext

def index(request):
    template = loader.get_template('markov/index.html')
    return render_to_response('markov/index.html', locals(), context_instance = RequestContext(request))