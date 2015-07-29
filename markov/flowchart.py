import sys


# The second path of the algorithm
def initThM(age):
	
	pass

# age (int), ALT (char)
def deferThM(age, ALT):
	pass		# depends on what combinations we will be given from Dr. Toy


def ALT(age):
	while(1):
		input_ALT = raw_input("Choose your ALT: 1-Persistently Abnormal, 2-Intermittently Abnormal, 3-Persistently Abnormal. ")
		if(input_ALT == '1'):
			initThM(age)
			break
		elif(input_ALT == '2' or input_ALT == '3'):
			deferThM(age, input_ALT)
			break
		else:
			print "Please enter either 1, 2, or 3."


# The first path of the algorithm
def yesCirr():	
	pass 		# Get user input (age, stage, health state) and pass into MM

def noCirr():
	while(1):
		input_age = input("Please input your age: ")
		print "You entered", input_age

		if(input_age > 30):
			ALT(input_age)
			break
		elif(input_age <= 30 and input_age >= 5):
			# ALT is persisitently normal, HBV DNA < 2000
			deferThM(input_age, '3')
			break
		else:
			print "Please enter a valid age."



def firstQ(answer):
	# Ask if HBsAg positive (Cirrhosis)
	if (answer == 1):
		yesCirr()
		break
	else:
		noCirr()
		break