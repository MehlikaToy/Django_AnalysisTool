# -*- coding: utf-8 -*-
"""
model.py
This module relies on synthesizes reader.py and simple.py to
compute patient outcomes for different times.
"""

import reader as rd
import numpy as np

STATE_LEN = 31


# State indices.
CHBP_INDEX = 0
CHBN_INDEX = 1
CIRR_INDEX = 2
INACTIVE_INDEX = 5

LTDC_INDEX = 8 
LTHCC_INDEX = 18

LTDC_LEN = 10
LTHCC_LEN = 10


# Initial states.
CIRR_STATE = np.zeros(STATE_LEN)
CIRR_STATE[CIRR_INDEX] = 100

INACTIVE_STATE = np.zeros(STATE_LEN)
INACTIVE_STATE[INACTIVE_INDEX] = 100

CHB_STATE = np.zeros(STATE_LEN)
CHB_STATE[CHBP_INDEX] = 50
CHB_STATE[CHBN_INDEX] = 50


HCC_STATE_INDICES = [4, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]


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
        self.history = []
        
    
    def _advance(self, term='na'):
        """
        Advance one year.
        """
        # Load data.
        M, labels = rd.generate_model(self.female, min(self.age, 99))
        if (term == 'hcc'):
            for i in HCC_STATE_INDICES:
                for row in range(STATE_LEN):
                    M[row, i] = 0
                M[i, i] = 1    

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
        
        
    def _sim(self, years, term='na'):
        """
        Advance many years.
        """
        for i in range(years):
            self._advance(term)
            

    def _get_history(self):
        """
        Return simplified version of history.
        """
        simp_history = []
        for state in self.history:
            simp_history += [self._simplify(state)]
            
        return simp_history
    
    
    def _clear_history(self):
        self.history = []
        self.state = self.start_state
        self.age = self.start_age
        
        
    def get_data(self, years, term='na'):
        self._clear_history()
        self._sim(years, term=term)
        
        return self._get_history()
    
    
if (__name__ == "__main__"):
    start = CIRR_STATE
    age = 45
    female = False
    
    simulator = Simulation(age, female, start)
    hist = simulator.get_data(40, term='hcc')
    
    for t in range(len(hist)):
        print(t, hist[t][4])
        
    print('HBV death')
    for t in range(len(hist)):
        print(t, hist[t][11])
    
    
    
    
    
    