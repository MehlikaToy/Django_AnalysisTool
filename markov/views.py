from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from flowchart import *
from markov_cy import *
import json
import decimal
# # Create your views here.

def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

from django.shortcuts import render_to_response, RequestContext

def questionnaire(request):
    template = loader.get_template('markov/questionnaire.html')
    return render_to_response('markov/questionnaire.html', locals(), context_instance = RequestContext(request))

def resultsView(request):
    output = stuff()
    parse(output)
    g1, g2, g3 = getInitNodes()
    age, stage = ageStage()
    output1, output1A = markovMain(age=age, total_stages=stage, initialList=g1)

    # dictionary to list
    dictList =[['Health States', 'Percentage']]
    # convert the dict to the nested list
    for key, value in output1.iteritems():
        temp = [key,value]
        dictList.append(temp)

    cummList = [['State', 'Treatment', 'Natural History']]
    sortedOutput1A = sorted(output1A)
    for i in range(len(sortedOutput1A)/2):
        temp = [sortedOutput1A[i*2], output1A[sortedOutput1A[i*2]]*1000000, output1A[sortedOutput1A[i*2+1]]*1000000]
        cummList.append(temp)

    cumm = 0
    for i in output1.values():
        cumm += i
    # print cumm


    return render_to_response('markov/results.html',
                              {'array': json.dumps(dictList),
                                'array1': json.dumps(cummList)
                              })
