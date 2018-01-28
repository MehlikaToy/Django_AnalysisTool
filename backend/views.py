from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from django.shortcuts import render_to_response, RequestContext

import json
import decimal

import numpy as np
import flowchart as flow
import matrixoperations as mop
import reader as rd

STAGES = 40

# Create your views here.

def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())



# def questionnaire(request):
#     template = loader.get_template('markov/questionnaire.html')
#     return render_to_response('markov/questionnaire.html', locals(), context_instance = RequestContext(request))

def questionnaire(request):
    template = loader.get_template('markov/form.html')
    return render_to_response('markov/form.html', locals(), context_instance = RequestContext(request))


def resultsView(request):

    # returns finalDict from getAPI.py
    # ie. {'How old is your patient?': '38', ... }
    endem, age, cirr, ALT, HBV_DNA = flow.parse()
   
    
    recommendation = flow.getWhoRec(cirr, age, ALT, HBV_DNA)

    inputs = "Your " + str(age) + " year old patient "
    if (cirr == 'Yes'):
        inputs += "with Cirrhosis"
    else:
        inputs += "without Cirrhosis, "
        inputs += str(ALT) + 'ALT, '
        inputs += 'and HBV DNA ' + str(HBV_DNA) + "."
    

    model, labels = rd.generate_model(file='./matrix.xlsx', age=age, female=False)
    start = np.zeros(len(model[0]))
    
    # for now, always start from cirrhosis
    if (cirr == 'Yes'):
        start[2] = 100
    else:
        start[2] = 100


    hbv_data = [['Stages','Natural History', 'Treatment']]
    hcc_data = [['Stages','Natural History', 'Treatment']]
    cirr_data = [['Stages','Natural History', 'Treatment']]
    for i in range(0, STAGES+1):
        state = mop.pwr(model, i).dot(start)
        hbv_data.append([i, state[11], state[11]])
        hcc_data.append([i, state[4], state[4]])
        cirr_data.append([i, state[2], state[2]])
        

    tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Mx', 'Liver Cancer NH', 'Liver Cancer Mx']]
    i = 5
    while (i <= 40):
        tableArr.append([i,
                         str(round(hbv_data[i-1][1],2))+"%",
                         str(round(hbv_data[i-1][1],2))+"%",
                         str(round(hcc_data[i-1][1],2))+"%",
                         str(round(hcc_data[i-1][1],2))+"%"])
        i = i*2

    whoRec = 'Your Patient Needs ' + recommendation
    t_heading = recommendation

    dumpDict = {
        'deathHBV_Final': json.dumps(hbv_data),
        'hcc_Final': json.dumps(hcc_data),
        'cirrhosis_Final': json.dumps(cirr_data),
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
        'ifCirr': "true",
        't_heading': t_heading,
    }
    

    return render_to_response('markov/results.html', dumpDict)
