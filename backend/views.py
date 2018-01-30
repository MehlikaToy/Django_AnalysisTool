from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from django.shortcuts import render_to_response, RequestContext

import json
import decimal

import numpy as np
import flowchart as flow
import reader as rd
import model as md

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
   
    inputs = "Your " + str(age) + " year old patient "
    if (cirr == 'Yes'):
        inputs += "with Cirrhosis."
    else:
        inputs += "without Cirrhosis, "
        inputs += str(ALT).lower() + " ALT level, "
        inputs += "and " + str(HBV_DNA) + " HBV DNA."

    #model, labels = rd.generate_model(file='./matrix.xlsx', age=age, female=False)
    #start = np.zeros(len(model[0]))
    
    start = None
    if (cirr == 'Yes'):
        start = md.CIRR_STATE
    elif (ALT == 'Persistently Abnormal' and HBV_DNA == '>20,000 IU/ml'):
        start = md.CHB_STATE
    else:
        start = md.INACTIVE_STATE
    
    simulator = md.Simulation(int(age), False, start)
    simulator.sim(STAGES)
    history = simulator.get_history()


    hbv_data = [['Stages','Natural History', 'Treatment']]
    hcc_data = [['Stages','Natural History', 'Treatment']]
    cirr_data = [['Stages','Natural History', 'Treatment']]
    for t in range(0, STAGES+1):
        state = history[t]
        cirr_data.append([t, state[8], state[8]])
        hcc_data.append([t, state[9], state[9]])
        hbv_data.append([t, state[11], state[11]])
        

    tableArr = [['Years', 'DeathHBV NH', 'DeathHBV Mx', 'Liver Cancer NH', 'Liver Cancer Mx']]
    i = 5
    while (i <= 40):
        tableArr.append([i,
                         str(round(hbv_data[i-1][1],2))+"%",
                         str(round(hbv_data[i-1][1],2))+"%",
                         str(round(hcc_data[i-1][1],2))+"%",
                         str(round(hcc_data[i-1][1],2))+"%"])
        i = i*2


    # Generate recommendation.
    recommendation = flow.getWhoRec(cirr, age, ALT, HBV_DNA)
    whoRec = 'Your Patient Needs ' + recommendation
    t_heading = recommendation


    # Dump data.
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
