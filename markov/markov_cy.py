'''
Author: Calvin Yin, Gerry MeiXiong, Jasmine Kim
Made July 2015
Markov Model Emulator of Hepatitis B
'''

from nodes_monitor import *

# The initial Probabilities



# initialList = [Node04(0.019), Node05(0.012), Node06(0.013), Node26(0.611), Node28(0.148), Node29(0.094), Node30(0.103)]

# initialList = getInitialNodes(flowchart)

def markovMain(age = 35, total_stages = 15, endemicity = 1, stage_timeFrame = 1, initialList=[]):
    # Don't touch this part
    cummDict = {}
    oldList = initialList
    newList = []

    DeathHBV = []


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


            temp = node.nextStage(node.getDestStates(), node.getOriginValue(), temp)

            for i in temp:
                newList.append(i)

        newList = trimList(newList)

        print '########################'
        printList(newList)

        temp = [curr_stage ,0, 0]
        for i in newList:
            if i.getVarName() == 'Death HBV':
                temp[1] = i.getOriginValue()
            if i.getVarName() == 'Death HBV NH':
                temp[2] = i.getOriginValue()
        DeathHBV.append(temp)

        print DeathHBV


        for node in newList:
            if not str(node.getVarName()) in cummDict:
                cummDict[str(node.getVarName())] = node.getOriginValue()
            else:
                for i in oldList:
                    if node.getVarName() == i.getVarName():
                        temp = node.getOriginValue() - i.getOriginValue()
                        if temp > 0:
                            cummDict[str(node.getVarName())] += temp


    tempDict = {}
    for key in cummDict.keys():
        if key == 'Cirrhosis NH' or\
            key == 'Cirrhosis Initial Rx' or\
            key == 'HCC NH' or\
            key == 'HCC' or\
            key == 'Liver Transplantation NH' or\
            key == 'Liver Transplantation' or\
            key == 'Death HBV NH' or\
            key == 'Death HBV':
                tempDict[key] = round(cummDict[key], 5)

    print tempDict


        # print ""
        # print age, "!!!!!!!"
        # printCummTestValues(newList)
        # print ''
        # try:
        #     print 'Cirrhosis NH Cumm:                         ', round(cummDict['Cirrhosis NH'],5)
        #     print 'Cirrhosis Initial Rx Cumm:                 ', round(cummDict['Cirrhosis Initial Rx'],5)
        # except:
        #     pass
        # try:
        #     print 'HCC Cumm:                                  ', round(cummDict['HCC'],5)
        #     print 'HCC NH Cumm                                ', round(cummDict['HCC NH'],5)
        # except:
        #     pass
        # try:
        #     print 'Liver Transplantation Cumm:                ', round(cummDict['Liver Transplantation'],5)
        #     print 'Liver Transplantation NH Cumm              ', round(cummDict['Liver Transplantation NH'],5)
        # except:
        #     pass
        # try:
        #     print 'Death HBV Cumm:                            ', round(cummDict['Death HBV'],5)
        #     print 'Death HBV NH Cumm                          ', round(cummDict['Death HBV NH'],5)
        # except:
        #     pass
        # print "*******"
        # age += stage_timeFrame

    # finalDict = {}
    # for j in sorted(tempDict):
    #     finalDict[j] = tempDict[j]
    output = {}
    for i in newList:
        output[i.getVarName()] = i.getOriginValue()

    finalList = [['Cirrhosis', 0, 0], ['HCC', 0, 0], ['Liver Transplantation', 0, 0], ['Death HBV', 0, 0]]
    try:
        finalList[0][1] = (tempDict['Cirrhosis Initial Rx'])
        finalList[0][2] = (tempDict['Cirrhosis NH'])
    except:
        pass
    try:
        finalList[1][1] = (tempDict['HCC'])
        finalList[1][2] = (tempDict['HCC NH'])
    except:
        pass
    try:
        finalList[2][1] = (tempDict['Liver Transplantation'])
        finalList[2][2] = (tempDict['Liver Transplantation NH'])
    except:
        pass
    try:
        finalList[3][1] = (tempDict['Death HBV'])
        finalList[3][2] = (tempDict['Death HBV NH'])
    except:
        pass

    print 'CUMM', finalList
    print '########################'


    return {'output': output, 'finalList': finalList, 'DeathHBV': DeathHBV}

