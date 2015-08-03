'''
Author: Calvin Yin, Gerry MeiXiong, Jasmine Kim
Made July 2015
Markov Model Emulator of Hepatitis B
'''

from nodes_monitor import *


# Touch this part
age = 35
total_stages = 15
endemicity = 1
stage_timeFrame = 1  # in years
# The initial Probabilities



# initialList = [Node04(0.019), Node05(0.012), Node06(0.013), Node26(0.611), Node28(0.148), Node29(0.094), Node30(0.103)]

# initialList = getInitialNodes(flowchart)

def markovMain(age = 35, total_stages = 15, endemicity = 1, stage_timeFrame = 1, initialList=[]):
    # Don't touch this part
    cummDict = {}
    oldList = initialList
    newList = []

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

        for node in newList:
            if not str(node.getVarName()) in cummDict:
                cummDict[str(node.getVarName())] = node.getOriginValue()
            else:
                # cummDict[str(node.getVarName())] += (node.getOriginValue())
                # TODO somehow implement to actual cumm here.
                for i in oldList:
                    if node.getVarName() == i.getVarName():
                        temp = node.getOriginValue() - i.getOriginValue()
                        if temp > 0:
                            cummDict[str(node.getVarName())] += temp
        print ""
        print age, "!!!!!!!"
        printCummTestValues(newList)
        print ''
        try:
            print 'Cirrhosis NH Cumm:                         ', round(cummDict['Cirrhosis NH'],5)
            print 'Cirrhosis Initial Rx Cumm:                 ', round(cummDict['Cirrhosis Initial Rx'],5)
        except:
            pass
        try:
            print 'HCC Cumm:                                  ', round(cummDict['HCC'],5)
            print 'HCC NH Cumm                                ', round(cummDict['HCC NH'],5)
        except:
            pass
        try:
            print 'Liver Transplantation Cumm:                ', round(cummDict['Liver Transplantation'],5)
            print 'Liver Transplantation NH Cumm              ', round(cummDict['Liver Transplantation NH'],5)
        except:
            pass
        try:
            print 'Death HBV Cumm:                            ', round(cummDict['Death HBV'],5)
            print 'Death HBV NH Cumm                          ', round(cummDict['Death HBV NH'],5)
        except:
            pass
        print "*******"
        age += stage_timeFrame

    print cummDict
    sum = 0
    for value in cummDict.values():
        sum += value
    print sum

    output = {}
    for i in newList:
        output[i.getVarName()] = i.getOriginValue()
    return output

