import sys
import json
import tangelo
import os
import time
from sets import Set
sys.path.append(".")
from decorators import allow_all_origins



@tangelo.restful
@allow_all_origins
def get(filePath='./', fileAppOut='', maxOut = "500"):
    maxOut = int(maxOut)
    ssName  = filePath + "previewTrainingFiles/" + fileAppOut

    retList = []
    with open(ssName,'r') as f:
        for line in f:
            try:
                (lat,lon,user,date,text) = line.strip().split('\t')
            except:
                tangelo.log("Parser error for file: "+ssName+" line: "+line)
                continue
            dItem = {
                'lat':lat,
                'lon':lon,
                'posts': [{'cap':text,
                           'usr':user,
                           'date':date
                          }]

            }
            retList.append(dItem)
            if maxOut > 0 and len(retList) >= maxOut:
                break
    retDict = {}
    retDict['sco'] = retList
    retDict['total'] = len(retList)
    return json.dumps(retDict)
