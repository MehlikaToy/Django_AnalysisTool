from django.http import HttpResponse
from django.template import loader
from getAPI import stuff
from django.shortcuts import render_to_response, RequestContext

import json
import decimal

import numpy as np
import flowchart as flow
import reader as rd

STAGES = 40

"""
Begin copied code.
"""
STATE_LEN = 31


# State indices.
CHBP_INDEX = 0
CHBN_INDEX = 1
INACTIVE_INDEX = 5
LTDC_INDEX = 8 
LTHCC_INDEX = 18

LTDC_LEN = 10
LTHCC_LEN = 10


# Initial states.
LTDC_STATE = np.zeros(STATE_LEN)
LTDC_STATE[LTDC_INDEX] = 100

INACTIVE_STATE = np.zeros(STATE_LEN)
INACTIVE_STATE[INACTIVE_INDEX] = 100

CHB_STATE = np.zeros(STATE_LEN)
CHB_STATE[CHBP_INDEX] = 50
CHB_STATE[CHBN_INDEX] = 50


def generate_simplifier():
    """
    Generates a matrix that simplifies states.
    """
    s = np.zeros((STATE_LEN-18, STATE_LEN))
    for i in range(STATE_LEN):
        if (i < LTDC_INDEX):
            s[i, i] = 1
        elif (i >= LTDC_INDEX and i < LTHCC_INDEX):
            s[LTDC_INDEX, i] = 1
        elif (i >= LTHCC_INDEX and i < LTHCC_INDEX + LTHCC_LEN):
            s[LTHCC_INDEX - 9, i] = 1
        else:
            s[i-18, i] = 1
    return s


SIMPLIFIER = generate_simplifier()



class Simulation():
    # TODO make empty constrcuctor
    def __init__(self, age, female, start_state):
        """
        Load inital parameters.
        """        
        self.start_age = age
        self.female = female 
        self.start_state =  np.copy(start_state)
        
        self.state = np.copy(start_state)
        self.age = age
        self.history = [np.copy(start_state)]
        
    
    def _advance(self):
        """
        Advance one year.
        """
        # Load data.
        M, labels = rd.generate_model(self.female, min(self.age, 99))
        
        # Advance state.
        next_state = M.dot(self.state)
        
        # Update values.
        self.state = next_state
        self.age = self.age + 1
        self.history += [next_state]
     
        
    def _simplify(self, state):
        """
        Coalesce versions of the same state into a single state.
        """
        return SIMPLIFIER.dot(state)
        
        
    def sim(self, years):
        """
        Advance many years.
        """
        for i in range(years):
            self._advance()
            

    def get_history(self):
        """
        Return simplified version of history.
        """
        simp_history = []
        for state in self.history:
            simp_history += [self._simplify(state)]
            
        return simp_history








"""
End copied code.
"""







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
        start = LTDC_STATE
    elif (ALT == 'Persistently Abnormal' and HBV_DNA == '>20,000 IU/ml'):
        start = CHB_STATE
    else:
        start = INACTIVE_STATE
    
    simulator = Simulation(30, False, INACTIVE_STATE)
    simulator.sim(STAGES)
    history = simulator.get_history()    

    inputs += '\n' + str(history[0])
    inputs += '\n' + str(history[39])
    inputs += '\n' + str(simulator.age)
    
    test_real_history = simulator.history
    test_simplification = SIMPLIFIER


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
