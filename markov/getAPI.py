import urllib2
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

def stuff():
    response = urllib2.urlopen("https://api.typeform.com/v0/form/TOsSUX?key=6289137c9f94850a29203f5fd601c826a202d259&completed=true&offset=0&limit=1?order_by[]=completed&order_by[]=date_land,desc")
    data = json.loads(response.read())
    # pp.pprint(data)

    questionDict = {}
    for question in data.get("questions"):
        questionDict[str(question.get('id'))] = question.get('question')

    print questionDict

    # for answer in
    print data['responses'][0].get("answers")
