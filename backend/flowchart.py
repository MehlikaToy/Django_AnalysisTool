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
  "type": "service_account",
  "project_id": "testapi1-245008",
  "private_key_id": "370f2dcffd0adb48d6c25ee74ecb973a36557be1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCyQJ45zo8AFGRI\nN+qwi6NnU7YwodBUQ6M3tmQ5b0nXdUr1v/JOwq2IWGsILr641Kov7ICkgsY1SsiA\nTDN6VHK9BNk2bpxjD/LGSv89mEZZnIEFrNH4rFmg8ArVCSZyqjsIsDRgYomFT8//\nopHu1MIEmnd8orsMeZPSCAPkfknGGv//1AZ8INzbxZPIh3ec/aOTvUY198DkAuNC\nPZ3bzlhyc9Oq8xzPMkkpjJm6CZzVXUysepDngLuoHDJSGAMtS0pm+6R5fnZm4i49\ngolx6DywbqRmWRWyL0qRXGJCL4DRc6rC1k/1FhQ4JziW1z5M04Zr3X+gmSDMG6cr\ngqZopwhBAgMBAAECggEAIDOGsfQ0BqRoalh5o/uR4R5xDQ+KWlKet3eSWwLVAOCO\nUl9i12IZZcZtTXzeVPcMKJytr6p1QpbYKj851HlRgf6Qe+IXC9lLdxGA0yCBYvpg\nH4WVJ/qAtY9vsYUV5kSE5iCo0ZmzdLsSnQCCIvZZ92ltOP2P02TaNKjghSRgUPJt\nQCC/etwE4s4HtOs/XK2dOfwNE/bXs0oJht+D7FtQX4BA9RBGauA/SKbehcwQ+9n+\nHS8yHNtYuwRD09Bxk0cQEZTtCIBdHp8T/Vf+fCSRVAp1tvRcyR2pX0+HlHmkLaej\nAUNWAdag3kowk+/orU5WZHsu682kt2VJI0YGNnozfQKBgQD2fdcJtzKijwZmDgJ1\n6dWAtLS7uhVzjIkP4oEGPfwaQRUMitrC45M0TiRmWgOrtdLQRtR8LUWrz4eEbPXS\nDTLnlUK9y8AvU/YZRr8cbUgzL8AjqrAoTr6yLjTsI4PMwEMQxbpIMHWWTjb5N2ow\nH/Uy6IaTHyDW4XTa+5itD+8ZdQKBgQC5IOaqKsfBT+k1Q+se3CuzXsEebZfJJY3X\ne/m0BsYtgP/i4IS8pdA85k09Ctkruou/B6b+V1P5oD3+/uskY9pzRW1QwHiUJj5T\n9BD21atwP1NJQXYWIcyJVpwJ6bCJyEq8H226GvbvpEdbz0VtxA+/JpuS1IAyaVy7\nlFVBvCHOHQKBgQCe4lauSIw3BIJXXkhvwR6CK/kj2LrjFH904cfRQjsyoSj0QLzq\nSs8kNAp6fyNGl5kf78gfkv8J1GfCEIoTr7ZUWH4A4UksOK61dEjUBg04EVuEog2S\nrc92AxrR68KVRIj2Ur3UsofZLul4kyO7iZ4ABqpYQwRj/kfYr7ymMVMp0QKBgC9c\nSWZzN1MvHFwyGe51KQDkVsdwBgrBfr4Hy2PQ79YoUE48Xfjc+p750/yvz8suGB4w\n2PnsYWFVK0cW9BUFLpeaxVKJSs+r0PotUEG1e/xlVutAwfL7hpYEADtQ+4bkJKpn\n5+xahZ3dCxxjtEFWjSi7ucUgdANxjPW4Bu+gL43JAoGAE/O1MhsSdy9cyT4uYopQ\nUVC0fZVkYGQQCmxdLDCi35vgp3j1gYFFdTqCYirlFn9EEJsMNl6yQOExC8U8/uVW\n/j8vx3B2/3rFLvaQvR+7pxSzW7SD8zUwYpJj1ejMhcnSmk6ke4/7ykFUpBC0T+D6\nPIaI/Eq0MhVHSz926zpGZWQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "webtooltest@testapi1-245008.iam.gserviceaccount.com",
  "client_id": "103643131633598775640",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/webtooltest%40testapi1-245008.iam.gserviceaccount.com"
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
    
    endem = endem_labels[arr[1]]
    age = int(arr[2])
    cirr = arr[4]			#cirrhosis
    ALT = arr[5]
    HBV_DNA = arr[6]
    gender = arr[3]

    return (endem, age, cirr, ALT, HBV_DNA, gender)



def getWhoRec(cirr, age, ALT, HBV_DNA):
	if answer == 'Yes' or (age >= 30 and ALT == "Persistently Abnormal" and HBV_DNA == ">20,000 IU/ml"):
		return 'Monitoring and Treatment'
	else:
		return 'Monitoring'
