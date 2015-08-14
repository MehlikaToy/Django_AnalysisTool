'''
Author: Calvin Yin, Gerry MeiXiong, Jasmine Kim
Made July 2015
Markov Model Emulator of Hepatitis B
'''

from nodes_monitor import *

# The initial Probabilities



# initialList = [Node04(0.019), Node05(0.012), Node06(0.013), Node26(0.611), Node28(0.148), Node29(0.094), Node30(0.103)]
# initialList = [Node06(1)]
# initialList = getInitialNodes(flowchart)

def markovMain(age = 35, total_stages = 5, endemicity = 1, stage_timeFrame = 1, initialList=[]):
    # Don't touch this part
    cummDict = {}
    oldList = initialList
    newList = []

    guacDict = {}

    DeathHBV = [['Stages', 'Treatment', 'Natural History'],[0,0,0]]
    Cirrhosis = [['Stages', 'Treatment', 'Natural History'],[0,0,0]]
    HCC = [['Stages', 'Treatment', 'Natural History'],[0,0,0]]
    LT = [['Stages', 'Treatment', 'Natural History'],[0,0,0]]

    age += 1

    for curr_stage in range(1, total_stages+1):

        if curr_stage != 1:
            oldList = newList
            newList = []

        for node in oldList:

            if age - 1 >= 50 and node.getProbValAFF():
                temp = node.getProbValAFF()
            elif age - 1 >= 40 and node.getProbValAFR():
                temp = node.getProbValAFR()
            elif age - 1 <= 30 and node.getProbValLET():
                temp = node.getProbValLET()
            elif age - 1 >= 30 and node.getProbValAT():
                temp = node.getProbValAT()
            else:
                temp = node.getProbValUT()

            try:
                for i in range(0, len(temp)):
                    temp[i] = temp[i] * node.secBranch[i]
            except:
                pass

            temp = dVarReplace(temp, age)
            temp = pVarReplace(temp)
            temp = node.nextStage(node.getDestStates(), node.getOriginValue(), temp, currNode = node.getID())

            for i in temp:
                if i.getGuac() != 0:
                    guacDict[i.getVarName()] = i.getGuac()

            for i in temp:
                newList.append(i)

        newList = trimList(newList)

        for node in newList:
            try: # for this part if it is just (=) then it is the amount of people that enter in that state
                 # if it is (+=) then it is instead the cumulative amount of people   
                cummDict[node.getVarName()] += node.getOriginValue() - guacDict[node.getVarName()]
            except:
                cummDict[node.getVarName()] = node.getOriginValue()

        t_death = [curr_stage ,0, 0]
        t_cirr = [curr_stage ,0, 0]
        t_hcc = [curr_stage ,0, 0]
        t_lt =[curr_stage ,0, 0]

        for i in newList:
            if i.getVarName() == 'Death HBV':
                t_death[1] = round(i.getOriginValue()*100,3)
            if i.getVarName() == 'Death HBV NH':
                t_death[2] = round(i.getOriginValue()*100,3)

            if i.getVarName() == 'Cirrhosis Initial Rx':
                t_cirr[1] = round(i.getOriginValue()*100,3)
            if i.getVarName() == 'Cirrhosis NH':
                t_cirr[2] = round(i.getOriginValue()*100,3)

            if i.getVarName() == 'HCC':
                t_hcc[1] = round(i.getOriginValue()*100,3)
            if i.getVarName() == 'HCC NH':
                t_hcc[2] = round(i.getOriginValue()*100,3)

            if i.getVarName() == 'Liver Transplantation':
                t_lt[1] = round(i.getOriginValue()*100,3)
            if i.getVarName() == 'Liver Transplantation NH':
                t_lt[2] = round(i.getOriginValue()*100,3)
        DeathHBV.append(t_death)
        Cirrhosis.append(t_cirr)
        HCC.append(t_hcc)
        LT.append(t_lt)

    output = {}
    for i in newList:
        output[i.getVarName()] = i.getOriginValue()

    finalList = [['Cirrhosis', 0, 0], ['HCC', 0, 0], ['Liver Transplantation', 0, 0], ['Death HBV', 0, 0]]
    try:
        finalList[0][1] = (cummDict['Cirrhosis Initial Rx'])
        finalList[0][2] = (cummDict['Cirrhosis NH'])
    except:
        pass
    try:
        finalList[1][1] = (cummDict['HCC'])
        finalList[1][2] = (cummDict['HCC NH'])
    except:
        pass
    try:
        finalList[2][1] = (cummDict['Liver Transplantation'])
        finalList[2][2] = (cummDict['Liver Transplantation NH'])
    except:
        pass
    try:
        finalList[3][1] = (cummDict['Death HBV'])
        finalList[3][2] = (cummDict['Death HBV NH'])
    except:
        pass

    print 'CUMM', finalList
    print '########################'


    return {'output': output, 'finalList': finalList, 'DeathHBV': DeathHBV, 'Cirrhosis': Cirrhosis, 'HCC': HCC, 'LT': LT}

