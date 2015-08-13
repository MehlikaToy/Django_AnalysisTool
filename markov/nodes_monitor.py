'''
Author: Gerry Meixiong
Made July 2015
Markov States of Hepatitis B
'''

pVar = -1.0
dVar = -2.0

class BasicNode(object):

    def __init__(self, OV):
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = None
        self.destStates = []
        self.probValUT =  None
        self.probValLET = None
        self.probValAT =  None
        self.probValAFR = None
        self.probValAFF = None
        self.guac = 0


    def __str__(self):
        return str(self.originValue)

    def getID(self):
        return self.ID

    def getOriginValue(self):
        return self.originValue

    def getVarName(self):
        return self.varName

    def getDestStates(self):
        return self.destStates

    def getProbValUT(self):
        return self.probValUT

    def getProbValLET(self):
        return self.probValLET

    def getProbValAT(self):
        return self.probValAT

    def getProbValAFR(self):
        return self.probValAFR

    def getProbValAFF(self):
        return self.probValAFF

    def getGuac(self):
        return self.guac

    def nextStage(self,destStates, originVal, probList, currNode = None):
        temp = []
        for i in range(0, len(destStates)):
            tempNode = destStates[i](originVal * probList[i])
            temp.append(tempNode)
            if tempNode.getID() == currNode:
                tempNode.guac = tempNode.getOriginValue()
        return temp

def getMort(age):
    dic = {'5': 3.5524154231776503E-4,
    '6': 3.24892148620962E-4,
	'7':    	2.94793646610664E-4,
	'8':        3.26603531762132E-4,
	'9':        2.8740823957970705E-4,
	'10':    	3.0267705509876903E-4,
	'11':      2.5905876615459604E-4,
	'12':    2.66982492556994E-4,
	'13': 	2.78406064602952E-4,
	'14': 	2.65765160159904E-4,
	'15':    	2.53793134346329E-4,
	'16':     	2.30420924321776E-4,
	'17':     	2.44613530905745E-4,
	'18':     3.0019797314705403E-4,
	'19':    3.28430469086282E-4,
	'20':	4.08827647295609E-4,
	'21':    	4.26235216085443E-4,
	'22': 	5.07025588382995E-4,
	'23':    	5.21059392326374E-4,
	'24':  	5.632017887907071E-4,
	'25':  	5.75426416701374E-4,
	'26': 	5.51657990424024E-4,
	'27':  	5.95479804879228E-4,
	'28':    	6.19822923488153E-4,
	'29': 	6.51856928229169E-4,
	'30':    	7.697867151943E-4,
	'31':    	7.38227702784667E-4,
	'32':      8.105338922907301E-4,
	'33': 	7.95802648075423E-4,
	'34':     8.952020120277392E-4,
	'35':    9.83258021818251E-4,
	'36':    0.0010133072306520098,
	'37':    0.0011385071608541499,
	'38':    0.00119970841672734,
	'39':    	0.00137838757715068,
	'40':    0.00158442105480963,
	'41':    	0.00150127049968808,
	'42':    0.00175161910175672,
	'43':    0.00180539761251498,
	'44':    	0.00192590140999178,
	'45':    0.00215583540449704,
	'46':    0.0022933517195538305,
	'47':    0.00254778095906509,
	'48':    0.0028139353836786,
	'49': 	0.00307570149317932,
	'50':    	0.00357971851618876,
	'51':    	0.00364645238710761,
	'52':     0.00406714543137299,
	'53':    	0.00438005235121396,
	'54':    0.00492466661903979,
	'55':    0.00535962758921878,
	'56':    0.00561273118347368,
	'57':    0.00640040188936275,
	'58':    0.00691103146516015,
	'59':    	0.00793355833568796,
	'60':   0.0090719760391385,
	'61':   0.009604755580461241,
	'62':    	0.0109945252921273,
	'63':    	0.012027060671793,
	'64': 	0.0135510274842608,
	'65':    	0.015523784232532,
	'66': 	0.0167529832880834,
	'67':  	0.0191182592451417,
	'68': 	0.021850916579883403,
	'69': 	0.0250658877516502,
	'70':	   0.0285969094280849,
	'71': 	0.0301342028975468,
	'72':    	0.03544789664458,
	'73':    	0.0385111733416117,
	'74':    	0.0413275093978832,
	'75':     	0.045047555391277194,
	'76':  	0.0500102330667639,
	'77': 	0.0539264724704678,
	'78':    	0.062330140986592106,
	'79':    	0.0701073308852807,
	'80':    	0.08041543236583211,
	'81':    0.0858010523222881,
	'82':    0.0947121987894145,
	'83': 	0.103710807400137,
	'84': 	0.1128958502564,
	'85': 	0.119097971499834,
	'86':    	0.129851509769094,
	'87':    	0.142393333182364,
	'88': 	0.156406490377638,
	'89':    0.17278062096809,
	'90': 	0.191907623880937,
	'91': 	0.20647552670781,
	'92': 	0.222510073080958,
	'93': 	0.243502217534102,
	'94': 	0.252464742280994,
	'95': 	0.253624014245739,
	'96':    0.250068058335716,
	'97': 	0.258538503893652,
	'98':    	0.281490470283072,
	'99':  	0.28170781671159,
	'100':    	0.380397506925208
    }
    if str(age) in dic.keys():
        return dic[str(age)]
    elif age >= 111 :
        return 1
    else:
        return dic['100']

def getInitialNodes(age):
    HBsAg = None
    CHB = None
    CHBneg = None
    Cirr = None
    population = None
    if (age <= 14):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956
    if (age >= 15 and age <= 24):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956
    if (age >= 25 and age <= 34):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956
    if (age >= 35 and age <= 44):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956
    if (age >= 45 and age <= 54):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956
    if (age >= 55 and age <= 64):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956
    if (age >= 65):
        HBsAg = 195054
        CHB = 53165
        CHBneg = 33825
        Cirr = 36912
        population = 318956

    tested_rate = 0.58
    followup_rate = 0.587
    treatment_rate = 0.33

    PHBsAg = 0 																								#2
    PHBsAgNH = round(float(HBsAg) / population, 3) 																#26
    PCHB = round((CHB * tested_rate * followup_rate * treatment_rate) / population, 3) 						#4
    PCHBNH = round((CHB - CHB * tested_rate * followup_rate * treatment_rate) / population, 3) 				#28
    PCHBneg = round((CHBneg * tested_rate * followup_rate * treatment_rate) / population, 3)				#5
    PCHBnegNH = round((CHBneg - CHBneg * tested_rate * followup_rate * treatment_rate) / population, 3)		#29
    Pcirr = round((Cirr * tested_rate * followup_rate * treatment_rate) / population, 3)					#6
    PcirrNH = round((Cirr - Cirr * tested_rate * followup_rate * treatment_rate) / population, 3) 			#30

    return [Node26(PHBsAgNH), Node04(PCHB), Node15(PCHBNH), Node05(PCHBneg), Node29(PCHBnegNH), Node06(Pcirr), Node30(PcirrNH)]

#Basic Calculation Functions
def printCummTestValues(list):
    for i in list:
        if i.getVarName() == 'Cirrhosis NH' or i.getVarName() == 'Cirrhosis Initial Rx' or i.getVarName() == 'HCC' or i.getVarName() == 'HCC NH':
            print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue(),5),))
        if i.getVarName() == 'Liver Transplantation NH' or i.getVarName() == 'Death HBV NH' or i.getVarName() == 'Liver Transplantation' or i.getVarName == 'Death HBV':
            print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue(),5),))

def printList(list):
    for i in list:
        print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue(),5),))

def sumList(list):
    sum = 0
    for i in list:
        sum += i.getOriginValue()
    return sum

#Prob List Manipulation Functions
def pVarReplace(list):
    pVarOcc = 0

    for i in range(0, len(list)):
        if list[i] < 0:
            pVarOcc += 1

    if pVarOcc is not 0:
        total = sum(list)
        for i in range(0, len(list)):
            if  list[i] < 0:
               list[i] *= total

    return list

def dVarReplace(list, age):
    if dVar in list:
        dIndex = list.index(dVar)
        dRate = getMort(age-1)
        if dRate == 1:
            for i in range(0,len(list)):
                list[i] = 0.0
        list[dIndex] = dRate
    return list

def trimList(array):   # sums up all nodes with same name to create a neat array
    resultList = sorted(array, key=lambda array: array.ID)
    i = 0
    while i < len(resultList)-1:
        if resultList[i].getID() == resultList[i+1].getID():
            resultList[i].originValue = (resultList[i].getOriginValue() + resultList[i+1].getOriginValue())
            del resultList[i+1]
        else:
            i += 1
    return resultList


#The Nodes
class Node01(BasicNode):

    def __init__(self, OV):
        super(Node01, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg Seroclearance"
        self.destStates = [Node01, Node08, Node24]
        self.probValUT =  [pVar  , 0     , dVar]
        self.probValAFF = [pVar  , 0.01  , dVar]



class Node02(BasicNode):

    def __init__(self, OV):
        super(Node02, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg +"
        self.destStates = [Node36    ,       Node26]
        self.probValUT =  [0.35  , 1 - 0.35]

class Node03(BasicNode):

    def __init__(self, OV):
        super(Node03, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBeAg Seroconversion"
        self.destStates = [Node03, Node01, Node18, Node29,  Node24]
        self.probValUT =  [pVar  , 0.008 , 0.029 , 0.029 ,  dVar]
        self.probValAT =  [pVar  , 0.007 , 0.038 , 0.038 ,  dVar]
        self.probValAFR = [pVar  , 0.003 , 0.086 , 0.086 ,  dVar]
        self.secBranch =  [1     , 1     , 0.65  , 0.35  ,  1]

class Node04(BasicNode):

    def __init__(self, OV):
        super(Node04, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe+"
        self.destStates = [Node11, Node28 , Node03 , Node17 , Node29 , Node14 , Node30 , Node24]
        self.probValLET = [pVar  , pVar   , 0.09   , 0.019  , 0.019  , 0.001  , 0.001  ,  dVar ]
        self.probValAT =  [pVar  , pVar   , 0.07   , 0.019  , 0.019  , 0.0235 , 0.0235 ,  dVar ]
        self.secBranch =  [0.65  , 0.35   , 1      , 0.65   , 0.35   , 0.65   , 0.35   ,  1]

class Node05(BasicNode):

    def __init__(self, OV):
        super(Node05, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- disease"
        self.destStates = [Node17, Node29, Node14, Node30, Node24]
        self.probValUT =  [pVar  , pVar  , 0.0235, 0.0235, dVar]
        self.secBranch =  [0.65  , 0.35  , 0.65  , 0.35  , 1 ]

class Node06(BasicNode):

    def __init__(self, OV):
        super(Node06, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis"
        self.destStates = [Node14, Node30, Node24]
        self.probValUT =  [pVar  , pVar  , dVar]
        self.secBranch =  [0.65  , 0.35  , 1 ]

class Node07(BasicNode):

    def __init__(self, OV):
        super(Node07, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "DecompCirr"
        self.destStates = [Node07, Node08, Node09, Node23, Node24]
        self.probValUT =  [pVar  , 0.0710,   0.12, 0.1495,   dVar]
        self.probValAT =  [pVar  , 0.0710,   0.12, 0.1495,   dVar]

class Node08(BasicNode):

    def __init__(self, OV):
        super(Node08, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HCC"
        self.destStates = [Node08,  Node09, Node23, Node24]
        self.probValUT =  [pVar  ,   0.047,  0.545,   dVar]
        self.probValAT =  [pVar  ,   0.047,  0.545,   dVar]

class Node09(BasicNode):

    def __init__(self, OV):
        super(Node09, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Liver Transplantation"
        self.destStates = [Node09, Node23, Node24]
        self.probValUT =  [pVar  ,  0.066,   dVar]
        self.probValAT =  [pVar  ,  0.066,   dVar]

class Node10(BasicNode):
    def __init__(self, OV):
        super(Node10, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Sustained Virological Response"
        self.destStates = [Node10, Node24]
        self.probValUT  = [pVar  , dVar]

class Node11(BasicNode):

    def __init__(self, OV):
        super(Node11, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB initial Rx"
        self.destStates = [Node10, Node12, Node15, Node08, Node24]
        self.probValUT =  [0.22  , pVar  , 0.0029, 0.002 , dVar]

class Node12(BasicNode):

    def __init__(self, OV):
        super(Node12, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB Long Term Rx"
        self.destStates = [Node10, Node12, Node13, Node15 , Node08, Node24]
        self.probValUT =  [0.27  , pVar  , 0.01  , 0.00295, 0.002 , dVar]

class Node13(BasicNode):

    def __init__(self, OV):
        super(Node13, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB Long Term with Rx with Resistance"
        self.destStates = [Node10, Node13, Node16, Node08, Node24]
        self.probValUT =  [0.05  , pVar  , 0.0295, 0.004 , dVar]

class Node14(BasicNode):

    def __init__(self, OV):
        super(Node14, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Initial Rx"
        self.destStates = [Node10, Node15, Node08, Node24]
        self.probValUT =  [0.22  , pVar  , 0.009 , dVar]

class Node15(BasicNode):

    def __init__(self, OV):
        super(Node15, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Long Term Rx"
        self.destStates = [Node10, Node15, Node16, Node07, Node08, Node23, Node24]
        self.probValUT =  [0.27  , pVar  , 0.01  , 0.0071, 0.0167, 0.0239, dVar]

class Node16(BasicNode):

    def __init__(self, OV):
        super(Node16, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Long Term Rx with resistance"
        self.destStates = [Node10, Node16, Node07, Node08, Node23, Node24]
        self.probValUT =  [0.05  , pVar  , 0.079 , 0.018 , 0.0478, dVar]

class Node17(BasicNode):

    def __init__(self, OV):
        super(Node17, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- initial Rx"
        self.destStates = [Node10, Node18, Node20, Node08, Node24]
        self.probValUT =  [0.11  ,   pVar,  0.006, 0.002,   dVar]

class Node18(BasicNode):

    def __init__(self, OV):
        super(Node18, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- longterm Rx"
        self.destStates = [Node10, Node18, Node19,  Node21, Node08, Node24]
        self.probValUT =  [0.11  ,   pVar,   0.01, 0.00295, 0.006,   dVar]

class Node19(BasicNode):

    def __init__(self, OV):
        super(Node19, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- longterm Rx resistance"
        self.destStates = [Node10, Node19, Node21, Node08, Node24]
        self.probValUT =  [0.005 ,   pVar,  0.062, 0.002,   dVar]

class Node20(BasicNode):

    def __init__(self, OV):
        super(Node20, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- initial Rx"
        self.destStates = [Node10, Node21, Node08, Node24]
        self.probValUT =  [0.11  ,   pVar, 0.015,   dVar]

class Node21(BasicNode):

    def __init__(self, OV):
        super(Node21, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- longterm Rx"
        self.destStates = [Node10, Node21, Node22, Node07, Node08, Node23, Node24]
        self.probValUT =  [0.11  ,   pVar,   0.01, 0.0071, 0.0167, 0.0239,   dVar]

class Node22(BasicNode):

    def __init__(self, OV):
        super(Node22, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- longterm Rx with resistance"
        self.destStates = [Node10, Node22, Node07, Node08, Node23, Node24]
        self.probValUT =  [0.005 ,   pVar,  0.079,  0.029, 0.0478,   dVar]

class Node23(BasicNode):

    def __init__(self, OV):
        super(Node23, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death HBV"
        self.destStates = [Node23]
        self.probValUT = [1]

class Node24(BasicNode):

    def __init__(self, OV):
        super(Node24, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death (Other)"
        self.destStates = [Node24]
        self.probValUT =  [1]
        self.probValAT =  [1]

class Node25(BasicNode):

    def __init__(self, OV):
        super(Node25, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg SeroclearanceNH"
        self.destStates = [Node25, Node32, Node35]
        self.probValUT =  [pVar  , 0.0   , dVar]
        self.probValAFF = [pVar  , 0.01  , dVar]

class Node26(BasicNode):

    def __init__(self, OV):
        super(Node26, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg + NH"
        self.destStates = [Node25, Node28, Node30 , Node32  , Node35, Node26]
        self.probValUT =  [0.0077, 0.0087, 0.00038, 0.001677, dVar  ,   pVar]
        self.probValAT =  [0.0107, 0.0143, 0.00049, 0.001677, dVar  ,   pVar]
        self.probValAFR = [0.0165, 0.0278, 0.00068, 0.001677, dVar  ,   pVar]
        self.probValAFF = [0.0183, 0.0202, 0.00150, 0.001677, dVar  ,   pVar]

class Node27(BasicNode):

    def __init__(self, OV):
        super(Node27, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBeAg SeroconversionNH"
        self.destStates = [Node27, Node25, Node29, Node30, Node32, Node35]
        self.probValUT =  [pVar  , 0.008 , 0.029 , 0.002 , 0     , dVar]
        self.probValAT =  [pVar  , 0.007 , 0.038 , 0.01  , 0     , dVar]
        self.probValAFR = [pVar  , 0.003 , 0.086 , 0.042 , 0     , dVar]
        self.probValAFF = [pVar  , 0.003 , 0.086 , 0.042 , 0.01  , dVar]

class Node28(BasicNode):

    def __init__(self, OV):
        super(Node28 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe+NH"
        self.destStates = [Node28, Node27, Node29, Node30, Node32, Node34, Node35]
        self.probValLET = [pVar  , 0.09  , 0.019 , 0.001 , 0.001 , 0.0064, dVar]
        self.probValAT =  [pVar  , 0.07  , 0.019 , 0.0235, 0.008 , 0.0064, dVar]

class Node29(BasicNode):

    def __init__(self, OV):
        super(Node29 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB e- diseaseNH"
        self.destStates = [Node29, Node26, Node30, Node32, Node34, Node35]
        self.probValUT  = [pVar  , 0.016 , 0.0235, 0.0080, 0.0064, dVar]

class Node30(BasicNode):

    def __init__(self, OV):
        super(Node30 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis NH"
        self.destStates = [Node30, Node31, Node32, Node34, Node35]
        self.probValUT =  [pVar  , 0.039 , 0.05  , 0.0555, dVar]

class Node31(BasicNode):

    def __init__(self, OV):
        super(Node31 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "DecompCirr NH"
        self.destStates = [Node31, Node32, Node33, Node34, Node35]
        self.probValUT =  [pVar  , 0.0710, 0.12  , 0.1495, dVar]

class Node32(BasicNode):

    def __init__(self, OV):
        super(Node32 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HCC NH"
        self.destStates = [Node32, Node33, Node34, Node35]
        self.probValUT =  [pVar  , 0.047 , 0.545 , dVar]

class Node33(BasicNode):

    def __init__(self, OV):
        super(Node33 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Liver Transplantation NH"
        self.destStates = [Node33, Node34, Node35]
        self.probValUT  = [pVar  , 0.066 , dVar]

class Node34(BasicNode):

    def __init__(self, OV):
        super(Node34, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death HBV NH"
        self.destStates = [Node34]
        self.probValUT =  [1]

class Node35(BasicNode):

    def __init__(self, OV):
        super(Node35, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death Other NH"
        self.destStates = [Node35]
        self.probValUT =  [1]

class Node36(BasicNode):

    def __init__(self, OV):
        super(Node36, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg + Monitor"
        self.destStates = [Node01, Node04,   Node06,   Node08, Node24, Node36]
        self.probValUT =  [0.0077, 0.0087 , 0.00038, 0.00167 , dVar  ,  pVar ]
        self.probValAT =  [0.0107, 0.0143 , 0.00049, 0.00167 , dVar  ,  pVar ]
        self.probValAFR = [0.0165, 0.0278 , 0.00068, 0.00167 , dVar  ,  pVar ]
        self.probValAFF = [0.0183, 0.0202 , 0.00150, 0.00167 , dVar  ,  pVar ]


