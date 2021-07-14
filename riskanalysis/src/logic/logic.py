import json
import pymongo as pymongo
import re

from ..common.constants import *
from .json_encoder import *

# pymongo connecting to mongoDB
client = pymongo.MongoClient(
    host=MONGO['HOST'],
    port=MONGO['PORT'],
    username=MONGO['USERNAME'],
    password=MONGO['PASSWORD']
)
tiltCollection = client["RiskAnalysis"]["tilt"]

class FindTILTs(object):

    def findTILTs(self, domain):
        this = FindTILTs()
        tilts = []
        prevTILTs = []
        nextTILTs = []
        visitedTILTs = [ domain ]

        tilt = this.nextTILT(domain)
        tilts.append(JSONEncoder().encode(tilt))

        for dataDisclosed in prevTILTs[0]["dataDisclosed"]:
                    for recipient in dataDisclosed["recipients"]:
                        nextTILTs.append(recipient["domain"])
        
        prevTILTs.clear()
        prevTILTs = nextTILTs.copy()
        nextTILTs.clear()

        while prevTILTs.count() > 0:

            for nextTILT in prevTILTs:
                nextTILT = this.nextTILT(nextTILT)
                tilts.append(nextTILT)
                for dataDisclosed in nextTILT["dataDisclosed"]:
                    for recipient in dataDisclosed["recipients"]:
                        nextTILTs.append(recipient["domain"])
            
            prevTILTs.clear()
            prevTILTs = nextTILTs.copy()
            nextTILTs.clear()

        return tilts

    def nextTILT(self, domain):
        try:
            return tiltCollection.find_one( { "meta.url": re.compile(domain + "/|" + domain + "$") } )
        except Exception as e:
            return e