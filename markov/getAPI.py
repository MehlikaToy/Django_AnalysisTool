import urllib2
import json
import pprint

# pp = pprint.PrettyPrinter(indent=4)

def stuff():
    request = urllib2.urlopen("https://api.typeform.com/v0/form/TOsSUX?key=6289137c9f94850a29203f5fd601c826a202d259&completed=true")
    print json.dumps(request)