from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from flowchart import *
from markov_cy import *
import json
import decimal

# # Create your views here.

# def index(request):
#     template = loader.get_template('home/index.html')
#     return HttpResponse(template.render())


from django.shortcuts import render_to_response, RequestContext

def questionnaire(request):
    template = loader.get_template('markov/questionnaire.html')
    return render_to_response('markov/questionnaire.html', locals(), context_instance = RequestContext(request))

def resultsView(request):
    # template = loader.get_template('markov/results.html')

    output = stuff()

    parse(output)
    g1, g2, g3 = getInitNodes()
    age, stage = ageStage()
    output1 = markovMain(age=age, total_stages=stage, initialList=g1)
    # print output1

    #dictionary to list
    dictList =[]
    for key, value in output1.iteritems():
        temp = [key,value]
        dictList.append(temp)
    print dictList

    cumm = 0
    for i in output1.values():
        cumm += i
    print cumm

    # output1 = ", ".join(["=".join([key, str(val)]) for key, val in output1.items()])
    # context = RequestContext(request,{
    #     'stuff': dictList,
    #     })

    # return HttpResponse(template.render(context))
    return render_to_response('markov/results.html', {
        'array': json.dumps(dictList, cls=DecimalEncoder),
    })

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)