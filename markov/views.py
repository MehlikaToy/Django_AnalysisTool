from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
import os
from getAPI import stuff
from django.views import generic
from flowchart import *
from markov_cy import *

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

    parse(output)
    g1, g2, g3 = getInitNodes()
    age, stage = ageStage()
    print age, stage
    output1 = markovMain(age = age, total_stages = stage , initialList=g1)
    # print output1

    output1 = ", ".join(["=".join([key, str(val)]) for key, val in output1.items()])
    context = RequestContext(request,{
        'stuff': output1,
        })

    return HttpResponse(template.render(context))
    # return render_to_response('markov/results.html', locals(), context_instance = RequestContext(request))
