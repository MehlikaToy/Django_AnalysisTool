"""
	Jasmine
	Developed July 2015
	Flowchart algorithm
"""

import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import sys
# from nodes_monitor_e3 import *
import ssl


"""
Below is code to read google form
"""
jsonfile = {
  "private_key_id": "d579623aed14e4c8fe99c9c17ae682141516fc91",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMpmoo7px2ln0q\n3sTlLkwTge7JY3y+gpix7Ny2yURGzedqcM7W1DnJ9qMFUXycmp0exJnRU9kyGTFi\n7ic3Eujpwh/buJLmlJxkkxBmU10BbjeuDo0jGGey4fkBA66qrmzFUT4SLK4G0Ins\ny4UHl6q/goZHoucVHwW7/oQQUAxrH3k5QsHpAkkIxHyvBKdWTk6RYXRYG1kPO9V8\nnJ2J0+ER+H2R1V2B69SMiignxwCxUks4+LxK7xhVetbGnr7AmzRPx0kni/06yXeY\nRHSatREpmhUtWB34jje8RQvAg4TXaBWrfayvQ3DEmjaoLJyMtArFr6HBbJ3fKN4f\nmzjjJCu5AgMBAAECggEBAJKzHFh5K3mqyNDpXdU3idtWAdklUu+x6ElrFJCG2EW1\nJhVcBjljaoWHIjcWwa/0+XprziOK6qAKBSf4te25xXKD8JhtyAg4MZ+6+D+RtJLo\n8kr4LV4iCXvmlruOay/41wnfAhK/KoTCCozPG25k30ZnB2DkuqeeVFr9yKd06mIC\npS/yqrN7D8kCBeGsOIAhFXh2opkTFTNpWdJWYYUjw0ptyXBN1Sd2JAaSfF1BQ3NJ\nV+Wuqett/iELlrhfK/3MlDfsD277Li6ItCQXKcbHmOfRdet0E7ZQr4jrJL59gBxD\nbdgMRuNXruTe8gTEsDBvkoDNOtHH5FVT/ax9qngOaW0CgYEA+xnWCalh+btr2XnE\ndjcZkHSgObw9vP+OeJIeyOM56hFJTckLF2Se3rqlv1c0nFQkUkvzW+SUhKes4jVQ\nD8n92/lE2aXML98S8spRDwtYlBFqoNHunqi1Trk3js6jGflZOHGR7jj944FbcBuY\nDWeQqwK9KU9vVi5EJYYGEe6eH1MCgYEA0KSSgbYylRWzGdyKvfYM1wolIpGAwMUl\nF6svwpg4JgoccHMz7UCF3pX8ZFNyxvLdsArGuSxFU8UeL5J9jOfdqZKQaTOrS7jp\neJENxviSv5xyiT/8b2zbXl51xaaPsc0vLBGZ7IgviRt6Pmgkj6PpIgUBG/Xtkx+o\nj7pdCTyMA0MCgYEAisFpJGekS3MFEuUV6lliWBAKZj0eRK1XlkrwlgPygeTRhBlf\ndqrUm7G6W7SdzvE0LQHpVdNHOtLJVysstbzh+keRg0/6OE3l06J3DoAvj4rcSEgZ\nuzTxE7KH//Mx7+15HxarFGAL9EcMNzQYXvfm2okl7IkHtjDU2YNpIUmhuR8CgYBr\ntqrUQGW4xe0iytLt4xsZ4WjugcPAwYa2w2/yvHcwXEP2YeNK9ual1TTp7pLw1u1Q\nNyAE9TANYVSGJtCecA3lv37CcSRcAWi3D9vW/vlz5qbS6K/ALqjJ/WY71hOVLWLP\nE38tt9kipYbktQs7BNoU8BR0hPBT5iI1oXbqj9GQ1QKBgA+dY45vAykuhi09c1Be\n+emiJA/eu1Fu1U2FW8teNVgFC5CmrdvkWlmgUzeowf0nRwFeXyfS8+hWd50VyRbg\nsD4AcKBhJAcoFJnr0XnBk3W7kmJyGQ3v3vlRcmCJMb1RoztCsNGlKlgTKD75OzVd\nKg46gjU5ZZ81VFHvztAWcmI2\n-----END PRIVATE KEY-----\n",
  "client_email": "476245914215-lnglqcrvcc1oh2nsl8ktjcfg370bodkm@developer.gserviceaccount.com",
  "client_id": "476245914215-lnglqcrvcc1oh2nsl8ktjcfg370bodkm.apps.googleusercontent.com",
  "type": "service_account"
}

"""the algorithm"""


g1 = []
g2 = []
g3 = []
answer = age = endem = 0
ALT = HBV_DNA = ""


# First method to call.
# Parse through dictionary of questions and answers
def parse():
	# json_key = json.load(jsonfile)

    if (hasattr(ssl, '_create_unverified_context')):
        ssl._create_default_https_context = ssl._create_unverified_context

    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(jsonfile['client_email'], jsonfile['private_key'], scope)
    
    gc = gspread.authorize(credentials)
    
    wks = gc.open("Markov Questions (Responses)").sheet1
    
    lowestRow = wks.row_count - 1000 # this is magic don't touch

    arr = []
    for col in range(1,8):
        arr.append(wks.cell(lowestRow, col).value)

    endem_labels = {'Low':1, 'Intermediate':2, 'High':3}
    
    endem = endem_labels[arr[4]]
    age = int(arr[5])
    cirr = arr[1]			#cirrhosis
    ALT = arr[2]
    HBV_DNA = arr[3]
    gender = arr[6]

    return (endem, age, cirr, ALT, HBV_DNA, gender)



def getWhoRec(cirr, age, ALT, HBV_DNA):
	if answer == 'Yes' or (age >= 30 and ALT == "Persistently Abnormal" and HBV_DNA == ">20,000 IU/ml"):
		return 'Monitoring and Treatment'
	else:
		return 'Monitoring'
