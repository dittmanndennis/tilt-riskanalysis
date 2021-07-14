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
        nextTILTs = []
        nextTILT = this.nextTILT(domain)
        doc = JSONEncoder().encode(nextTILT)
        for dataDisclosed in nextTILT["dataDisclosed"]:
            for recipient in dataDisclosed["recipients"]:
                nextTILTs.append(recipient["domain"])

        return domain

    def nextTILT(self, domain):
        try:
            return tiltCollection.find_one( { "meta.url": re.compile(domain + "/|" + domain + "$") } )
        except Exception as e:
            return e