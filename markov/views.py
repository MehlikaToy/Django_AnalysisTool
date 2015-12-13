from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from flowchart import *
from markov_cy_e1 import *
from markov_cy_e2 import *
from markov_cy_e3 import *
import json
import decimal

# Create your views here.

def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

from django.shortcuts import render_to_response, RequestContext

# def questionnaire(request):
#     template = loader.get_template('markov/questionnaire.html')
#     return render_to_response('markov/questionnaire.html', locals(), context_instance = RequestContext(request))

def questionnaire(request):
    template = loader.get_template('markov/form.html')
    return render_to_response('markov/form.html', locals(), context_instance = RequestContext(request))


def resultsView(request):

    # returns finalDict from getAPI.py
    # ie. {'How old is your patient?': '38', ... }

    endemicity = parse()
    parse2()
    g1, g2, g3 = getInitNodes()
    age, stage = ageStage()
    answer, ALT, HBV_DNA = cirrALT_DNA()



    if endemicity == 1:
        response1 = markovMain1(age=age, initialList=g1)
    elif endemicity == 2:
        response1 = markovMain2(age=age, initialList=g1)
    else: 
        response1 = markovMain3(age=age, initialList=g1)

    # response1 = markovMain(age=age, initialList=g1)
    # print response1

    if endemicity == 1:
        response2 = markovMain1(age=age, initialList=g2)
    elif endemicity == 2:
        response2 = markovMain2(age=age, initialList=g2)
    else: 
        response2 = markovMain3(age=age, initialList=g2)

    # response2 = markovMain(age=age, initialList=g2)
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

    deathHBV_Final = [['Stages','Natural History', 'Treatment']]
    cirrhosis_Final = [['Stages','Natural History', 'Treatment']]
    hcc_Final = [['Stages','Natural History', 'Treatment']]
    for i in range(0, len(deathHBV1)-1):
        deathHBV_Final.append([i, deathHBV2[i+1][2], deathHBV1[i+1][1]])
        hcc_Final.append([i,hcc2[i+1][2], hcc1[i+1][1]])
        cirrhosis_Final.append([i,cirrhosis2[i+1][2], cirrhosis1[i+1][1]])
    
    # tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Rx', 'Liver Cancer NH', 'Liver Cancer Rx', 'Cirrhosis NH', 'Cirrhosis Rx']]
    # getStage = 5
    # while getStage <= 40:
    #     tableArr.append([getStage,
    #                     str(round(deathHBV2[getStage+1][2],2))+"%",
    #                     str(round(deathHBV1[getStage+1][1],2))+"%",
    #                     str(round(hcc2[getStage+1][2],2))+"%",
    #                     str(round(hcc1[getStage+1][1],2))+"%",
    #                     str(round(cirrhosis2[getStage+1][2],2))+"%",
    #                     str(round(cirrhosis1[getStage+1][1],2))+"%"]
    #                     )
    #     getStage = getStage*2

    # print tableArr

    recommendation = getWhoRec()

    inputs = "Your " + str(age) + " year old patient "
    if(answer == 'Yes'):              # if yes cirrhosis
        inputs += "has Cirrhosis."
        answer = 1
        getStage = 5
        if(recommendation == "Monitoring"):
            tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Mx', 'Liver Cancer NH', 'Liver Cancer Mx']]
        else:
            tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Rx', 'Liver Cancer NH', 'Liver Cancer Rx']]
        while getStage <= 40:
            tableArr.append([getStage,
                            str(round(deathHBV2[getStage+1][2],2))+"%",
                            str(round(deathHBV1[getStage+1][1],2))+"%",
                            str(round(hcc2[getStage+1][2],2))+"%",
                            str(round(hcc1[getStage+1][1],2))+"%"]
                            )
            getStage = getStage*2
    else:
        inputs += "doesn't have Cirrhosis with a " + ALT + " ALT level and an HBV DNA level that is " + HBV_DNA + '.'
        answer = 0
        getStage = 5
        if(recommendation == "Monitoring"):
            tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Mx', 'Liver Cancer NH', 'Liver Cancer Mx', 'Cirrhosis NH', 'Cirrhosis Mx']]
        else:
            tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Rx', 'Liver Cancer NH', 'Liver Cancer Rx', 'Cirrhosis NH', 'Cirrhosis Rx']]
        while getStage <= 40:
            tableArr.append([getStage,
                            str(round(deathHBV2[getStage+1][2],2))+"%",
                            str(round(deathHBV1[getStage+1][1],2))+"%",
                            str(round(hcc2[getStage+1][2],2))+"%",
                            str(round(hcc1[getStage+1][1],2))+"%",
                            str(round(cirrhosis2[getStage+1][2],2))+"%",
                            str(round(cirrhosis1[getStage+1][1],2))+"%"]
                            )
            getStage = getStage*2

    whoRec = 'Your Patient Needs ' + recommendation
    t_heading = recommendation

    # Print test:
    # print deathHBV2

    # deathHBV3 = []
    # cirrhosis3 = []
    # hcc3 = []
    # lt3 = []

    # print json.dumps(deathHBV1)
    # print '#####'
    # print json.dumps(deathHBV_Final)

    dumpDict = {
        'deathHBV_Final': json.dumps(deathHBV_Final),
        'hcc_Final': json.dumps(hcc_Final),
        'cirrhosis_Final': json.dumps(cirrhosis_Final),
        # 'deathHBV1': json.dumps(deathHBV1),
        # 'deathHBV2': json.dumps(deathHBV2),
        # 'cirrhosis1': json.dumps(cirrhosis1),
        # 'cirrhosis2': json.dumps(cirrhosis2),
        # 'hcc1': json.dumps(hcc1),
        # 'hcc2': json.dumps(hcc2),
        # 'lt1': json.dumps(lt1),
        # 'lt2': json.dumps(lt2),
        'inputStr': inputs,
        'whoRec': whoRec,
        'tableArr': tableArr,
        'ifCirr': answer,
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
