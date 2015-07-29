import urllib2
import json
import pprint
import collections
import flowchart as fc

pp = pprint.PrettyPrinter(indent=4)

def stuff():
    response = urllib2.urlopen("https://api.typeform.com/v0/form/TOsSUX?key=6289137c9f94850a29203f5fd601c826a202d259&completed=true&offset=0&limit=1?order_by[]=completed&order_by[]=date_land,desc")
    data = json.loads(response.read())
    pp.pprint(data)

    questionDict = {}
    for question in data.get("questions"):
        questionDict[str(question.get('id'))] = question.get('question')

    answerDict = data['responses'][0].get("answers")

    finalDict = {}
    for key in questionDict.keys():
        # print questionDict[key]
        # print answerDict[key]
        # print "*****"
        finalDict[questionDict[key]] = answerDict[key]

    finalDict =  convert(finalDict)
    for q, ans in finalDict.iteritems():
        if ("Does" in q):
            fc.firstQ(ans)
        
    return finalDict
    # {'Does your HBsAg patient have Cirrhosis': '1', 'Patient Age?': '4', 'ALT Levels?': '', 'HBV DNA Levels': '', 'Patient Stage?': '6'}


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data