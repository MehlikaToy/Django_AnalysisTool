'''
Author: Calvin Yin, Gerry MeiXiong, Jasmine Kim
Made July 2015
Markov Model Emulator of Hepatitis B
'''


from nodes_monitor_e3 import *

def markovMain(age = 49, total_stages = 40, endemicity = 3, stage_timeFrame = 1, initialList=[]):


    print '>>> INITIAL LIST Stage: BASE, Age: %s' % (age)
    printList(initialList)
    print '>>> COST'
    printCost(initialList, 0, total_stages)
    print '>>> UTILITY'
    printUtility(initialList, 0, total_stages, age)

    # Don't touch this part
    cummDict = {}
    oldList = initialList
    newList = []

    guacDict = {}

    DeathHBV = [['Stages', 'Treatment (dotted)', 'Natural History (solid)'],[0,0,0]]
    Cirrhosis = [['Stages', 'Treatment (dotted)', 'Natural History (solid)'],[0,0,0]]
    HCC = [['Stages', 'Treatment (dotted)', 'Natural History (solid)'],[0,0,0]]
    LT = [['Stages', 'Treatment (dotted)', 'Natural History (solid)'],[0,0,0]]

    assert 1 == getOrginValSum(oldList), 'Initial List is %.2f not 1' % (getOrginValSum(oldList))

    cummCirr = 0;
    cumulativeCost = sumCost(oldList, 0, total_stages)
    cumulativeQALY = sumUtility(oldList, 0, age, total_stages)

    for curr_stage in range(1, total_stages+2):

        age += 1

        if curr_stage != 1:
            oldList = newList
            newList = []

        for node in oldList:

            # The try function are so that Django doesn't somehow mess everything up.
            try:
                temp = node.getProbValUT()
            except:
                pass
            try:
                if age - 1 >= 50 and node.getProbValAFF():
                    temp = node.getProbValAFF()
            except:
                pass
            try:
                if age - 1 >= 40 and node.getProbValAFR():
                    temp = node.getProbValAFR()
            except:
                pass
            try:
                if age - 1 > 25 and node.getProbValATF():
                    temp = node.getProbValATF()
            except:
                pass
            try:
                if age - 1 <= 25 and node.getProbValUTF():
                    temp = node.getProbValUTF()
            except:
                pass
            try:
                if age - 1 <= 30 and node.getProbValLET():
                    temp = node.getProbValLET()
            except:
                pass
            try:
                if age - 1 <= 30 and node.getProbValLET():
                    temp = node.getProbValLET()
            except:
                pass
            try:
                if age - 1 >= 30 and node.getProbValAT():
                    temp = node.getProbValAT()
            except:
                pass

            try:
                for i in range(0, len(temp)):
                    temp[i] = temp[i] * node.secBranch[i]
            except:
                pass

            temp = dVarReplace(temp, age)
            temp = pVarReplace(temp)
            temp, cummCirr = node.nextStage(node.getDestStates(), node.getOriginValue(), temp, cummCirr, currNode = node)

            for i in temp:
                if i.getGuac() != 0:
                    guacDict[i.getVarName()] = i.getGuac()

            for i in temp:
                newList.append(i)

        newList = trimList(newList)


        def getCummDict(query):
            try:
                return cummDict[query]
            except:
                return 0

        t_death = [curr_stage ,0, 0]
        t_cirr = [curr_stage ,0, 0]
        t_hcc = [curr_stage ,0, 0]
        t_lt =[curr_stage ,0, 0]

        for node in newList:
            try:
                cummDict[node.getVarName()] += (node.getOriginValue() - guacDict[node.getVarName()]) * cohortPop
            except:
                try:
                    cummDict[node.getVarName()] += node.getOriginValue() * cohortPop
                except:
                    cummDict[node.getVarName()] = node.getOriginValue() * cohortPop

        t_death[1] = round(getCummDict('Death HBV'), 3)
        t_death[2] = round(getCummDict('Death HBV NH'), 3)

        t_cirr[1] = round(cummCirr * cohortPop, 3)
        t_cirr[2] = round(getCummDict('Cirrhosis NH'), 3)

        t_hcc[1] = round(getCummDict('HCC'), 3)
        t_hcc[2] = round(getCummDict('HCC NH'), 3)

        t_lt[1] = round(getCummDict('Liver Transplantation'), 3)
        t_lt[2] = round(getCummDict('Liver Transplantation NH'), 3)

        DeathHBV.append(t_death)
        Cirrhosis.append(t_cirr)
        HCC.append(t_hcc)
        LT.append(t_lt)

        cumulativeCost += sumCost(newList, curr_stage, total_stages)
        cumulativeQALY += sumUtility(newList, curr_stage, age, total_stages)

        # print '\nCUMM Current Stage:', curr_stage-1, 'Age:', age
        # try:
        #     print 'HCC : ', getCummDict('HCC')
        #     print 'HCC NH : ', getCummDict('HCC NH')
        #     print 'Death HBV: ', getCummDict('Death HBV')
        #     print 'Death HBV NH:', getCummDict('Death HBV NH')
        #     print 'Cirrhosis: ', cummCirr * cohortPop
        #     print 'Cirrhosis NH: ', getCummDict('Cirrhosis NH')
        #     print 'Cirrhosis Total:', (cummCirr * cohortPop) + getCummDict('Cirrhosis NH')
        # except:
        #     pass

        # print '\n#######################'


    output = {}
    for i in newList:
        output[i.getVarName()] = i.getOriginValue()

    finalList = [['Cirrhosis', 0, 0], ['HCC', 0, 0], ['Liver Transplantation', 0, 0], ['Death HBV', 0, 0]]
    try:
        finalList[0][1] = cummCirr * cohortPop
        finalList[0][2] = (getCummDict('Cirrhosis NH'))
    except:
        pass
    try:
        finalList[1][1] = (getCummDict('HCC'))
        finalList[1][2] = (getCummDict('HCC NH'))
    except:
        pass
    try:
        finalList[2][1] = (getCummDict('Liver Transplantation'))
        finalList[2][2] = (getCummDict('Liver Transplantation NH'))
    except:
        pass
    try:
        finalList[3][1] = (getCummDict('Death HBV'))
        finalList[3][2] = (getCummDict('Death HBV NH'))
    except:
        pass



    return {'output': output, 'finalList': finalList, 'DeathHBV': DeathHBV, 'Cirrhosis': Cirrhosis, 'HCC': HCC, 'LT': LT}

