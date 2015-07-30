"""
	Author: Jasmine Kim
	Developed July 2015
	Flowchart algorithm
"""

import sys
from nodes_monitor import * 



g1 = []
g2 = []
g3 = []
answer = age = stage = 0
ALT = HBV_DNA = ""


# First method to call.
# Parse through dictionary of questions and answers
def parse(finalDict):
	global g1, g2, g3, answer, age, ALT, stage, HBV_DNA
	g1 = []
	g2 = []
	g3 = []
	for q, ans in finalDict.iteritems():
		if ("Does your HBsAg patient have Cirrhosis" in q):
			answer = ans
		elif ("How old is your patient" in q):
			age = int(ans)
		elif ("What is your patient's ALT level" in q):
			ALT = ans
			print ALT
		elif ("How many years do you wish to see yourself in" in q):
			stage = int(ans)
		elif ("What is your patient's HBV DNA level" in q):
			HBV_DNA = ans
			print HBV_DNA

	if (answer == '1'):
		yesCirr()
	else:
		noCirr()


# Append to g1 and g2 arrays.
def yesCirr():																	# 1
	g1.append(Node04(1))
	g2.append(Node30(1))


def noCirr():
	global g1, g2, g3
	if(age <= 30):
		print ALT, HBV_DNA
		if(ALT == "Persistently Abnormal" and HBV_DNA == ">20,000 IU/ml"):		# 6
			g1.append(Node36(1))
			g2.append(Node26(1))
			g3.append(Node04(0.5))
			g3.append(Node05(0.5))
		else:																	# 7, 8
			g1.append(Node36(1))
			g2.append(Node26(1))
	elif(age >30):
		if(HBV_DNA == "<2000 IU/ml" or HBV_DNA == "2000-20,000 IU/ml"):		# 3, 5
			g1.append(Node36(1))
			g2.append(Node26(1))
		elif(ALT == "Persistently Abnormal"):									# 2
			g1.append(Node04(0.5))
			g1.append(Node05(0.5))
			g2.append(Node28(0.5))
			g2.append(Node29(0.5))
		else:																	# 4
			g1.append(Node36(1))
			g2.append(Node26(1))
			g3.append(Node04(0.5))
			g3.append(Node05(0.5))


def ageStage():
	return age, stage

def getInitNodes():
	return g1, g2 ,g3










