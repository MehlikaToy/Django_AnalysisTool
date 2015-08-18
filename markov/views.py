from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from flowchart import *
from markov_cy import *
import json
import decimal
# Create your views here.

def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

from django.shortcuts import render_to_response, RequestContext

def questionnaire(request):
    template = loader.get_template('markov/questionnaire.html')
    return render_to_response('markov/questionnaire.html', locals(), context_instance = RequestContext(request))

def resultsView(request):

    # returns finalDict from getAPI.py
    # ie. {'How old is your patient?': '38', ... }
    output = stuff()

    parse(output)
    g1, g2, g3 = getInitNodes()
    age, stage = ageStage()
    answer, ALT, HBV_DNA = cirrALT_DNA()
    print 'g1:'
    # printList(g1)
    # response1 = markovMain(age=age, total_stages=stage, initialList=g1)
    response1 = markovMain(initialList=[Node28(0.5), Node29(0.5)])
    # print response1
    print 'g2:'
    # response2 = markovMain(age=age, total_stages=stage, initialList=g2)
    response2 = markovMain(initialList=[Node04(0.5), Node05(0.5)])
    # print "response 1:",response1
    # print ""
    # print "g2:",g2
    # print ""
    # print "response 2:",response2
    # print ""

    deathHBV1 = response1['DeathHBV']
    deathHBV2 = response2['DeathHBV']

    cirrhosis1 = response1['Cirrhosis']
    cirrhosis2 = response2['Cirrhosis']

    hcc1 = response1['HCC']
    hcc2 = response2['HCC']
    
    lt1 = response1['LT']
    lt2 = response2['LT']
    
    inputs = "Your " + str(age) + " year old patient "
    if(int(answer)):              # if no cirrhosis
        inputs += "has Cirrhosis."
    else:
        inputs += "doesn't have Cirrhosis with a " + ALT + " ALT level and an HBV DNA level that is " + HBV_DNA + '.'


    # Print test:
    # print deathHBV2

    # deathHBV3 = []
    # cirrhosis3 = []
    # hcc3 = []
    # lt3 = []
    dumpDict = {
        'deathHBV1': json.dumps(deathHBV1),
        'deathHBV2': json.dumps(deathHBV2),
        'cirrhosis1': json.dumps(cirrhosis1),
        'cirrhosis2': json.dumps(cirrhosis2),
        'hcc1': json.dumps(hcc1),
        'hcc2': json.dumps(hcc2),
        'lt1': json.dumps(lt1),
        'lt2': json.dumps(lt2),
        'inputStr': inputs
    }

    # dictionary to list
    # dictList =[['Health States', 'Percentage']]
    # convert the dict to the nested list
    # for key, value in output1.iteritems():
    #     temp = [key,value]
    #     dictList.append(temp)

    # cummList1 = [['State', 'Treatment', 'Natural History']]
    # cummList2 = [['State', 'Treatment', 'Natural History']]
    # cummList3 = [['State', 'Treatment', 'Natural History']]
    # for i in output1A:
    #     cummList1.append(i)
    # for j in output2A:
    #     cummList2.append(j)
    # for k in output3A:
    #     cummList3.append(k)



    

    return render_to_response('markov/results.html', dumpDict)
