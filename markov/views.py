from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
import os
from getAPI import stuff
from django.views import generic


# # Create your views here.

# def index(request):
#     template = loader.get_template('home/index.html')
#     return HttpResponse(template.render())


from django.shortcuts import render_to_response, RequestContext, render

from .forms import NameForm

def questionnaire(request):
    template = loader.get_template('markov/questionnaire.html')
    return render_to_response('markov/questionnaire.html', locals(), context_instance = RequestContext(request))

def resultsView(request):
    template = loader.get_template('markov/results.html')
    output = stuff()
    output = ",  ".join(["=".join([key, str(val)]) for key, val in output.items()])
    context = RequestContext(request,{
        'stuff': output,
        })
    return HttpResponse(template.render(context))
    # return render_to_response('markov/results.html', locals(), context_instance = RequestContext(request))
