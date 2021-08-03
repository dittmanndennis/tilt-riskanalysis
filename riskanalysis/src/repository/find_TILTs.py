import pymongo as pymongo
import re

from ..common.constants import *

# pymongo connecting to mongoDB
client = pymongo.MongoClient(
    host=MONGO['HOST'],
    port=MONGO['PORT'],
    username=MONGO['USERNAME'],
    password=MONGO['PASSWORD']
)
tiltCollection = client["RiskAnalysis"]["tilt"]

class FindTILTs(object):

    # returns all tilt documents that are part of the given domains subgraph
    def findTILTs(self, domain):
        this = FindTILTs()
        if this.nextTILT(domain) == None:
            return None
        tilts = []
        prevTILTs = [ domain ]
        nextTILTs = []
        visitedTILTs = [ domain ]

        while len(prevTILTs) > 0:

            for domain in prevTILTs:
                nextTILT = this.nextTILT(domain)
                if nextTILT != None:
                    tilts.append(nextTILT)
                    for dataDisclosed in nextTILT["dataDisclosed"]:
                        for recipient in dataDisclosed["recipients"]:
                            if "domain" not in recipient:
                                continue
                            if recipient["domain"] not in visitedTILTs:
                                nextTILTs.append(recipient["domain"])
                                visitedTILTs.append(recipient["domain"])
            
            prevTILTs.clear()
            prevTILTs = nextTILTs.copy()
            nextTILTs.clear()

        return tilts

    # returns all domains that are part of the given domains subgraph
    def findDomains(self, domain):
        this = FindTILTs()
        if this.nextTILT(domain) == None:
            return None
        prevTILTs = [ domain ]
        nextTILTs = []
        visitedTILTs = [ domain ]

        while len(prevTILTs) > 0:

            for domain in prevTILTs:
                nextTILT = this.nextTILT(domain)
                if nextTILT != None:
                    for dataDisclosed in nextTILT["dataDisclosed"]:
                        for recipient in dataDisclosed["recipients"]:
                            if "domain" not in recipient:
                                continue
                            if recipient["domain"] not in visitedTILTs:
                                nextTILTs.append(recipient["domain"])
                                visitedTILTs.append(recipient["domain"])
            
            prevTILTs.clear()
            prevTILTs = nextTILTs.copy()
            nextTILTs.clear()

        return visitedTILTs

    # returns all graph properties that are part of the given domains subgraph
    def findProperties(self, domain):
        this = FindTILTs()
        if this.nextTILT(domain) == None:
            return None
        prevTILTs = [ domain ]
        nextTILTs = []
        visitedTILTs = [ domain ]
        # {0: domain}, {1: country}, {2: numberOfBreaches}, {3: severityOfBreaches}, {4: dataTypeShared[]}, {5: marketCapitalization}, {6: industrialSector}
        properties = []

        while len(prevTILTs) > 0:

            for domain in prevTILTs:
                
                nextTILT = this.nextTILT(domain)
                if nextTILT != None:
                    
                    dataTypes = []
                    country = nextTILT["controller"]["country"]
                    
                    for dataDisclosed in nextTILT["dataDisclosed"]:
                        dataTypes.append(dataDisclosed["category"])
                        for recipient in dataDisclosed["recipients"]:
                            if "domain" not in recipient:
                                continue
                            if recipient["domain"] not in visitedTILTs:
                                nextTILTs.append(recipient["domain"])
                                visitedTILTs.append(recipient["domain"])
                    
                    properties.append([domain, country, 0, 0, dataTypes, 0, None])
            
            prevTILTs.clear()
            prevTILTs = nextTILTs.copy()
            nextTILTs.clear()

        return properties

    # returns all connections that are part of the given domains subgraph
    def findConnections(self, domain):
        this = FindTILTs()
        if this.nextTILT(domain) == None:
            return None
        currentDomain = domain
        connections = []
        prevTILTs = [ domain ]
        nextTILTs = []
        visitedTILTs = [ domain ]
        currentVisitedTILTs = []

        while len(prevTILTs) > 0:

            for domain in prevTILTs:
                nextTILT = this.nextTILT(domain)
                if nextTILT != None:
                    currentDomain = domain
                    for dataDisclosed in nextTILT["dataDisclosed"]:
                        for recipient in dataDisclosed["recipients"]:
                            if "domain" not in recipient:
                                continue
                            if recipient["domain"] not in visitedTILTs:
                                nextTILTs.append(recipient["domain"])
                                visitedTILTs.append(recipient["domain"])
                            if recipient["domain"] not in currentVisitedTILTs:
                                currentVisitedTILTs.append(recipient["domain"])
                                connections.append([currentDomain, recipient["domain"]])
            
            currentVisitedTILTs.clear()
            prevTILTs.clear()
            prevTILTs = nextTILTs.copy()
            nextTILTs.clear()

        return connections

    # returns the tilt document of the given domain
    def nextTILT(self, domain):
        try:
            return tiltCollection.find_one( { "meta.url": re.compile("^" + domain + "$|^" + domain + "/|/" +
            domain + "$|\." + domain + "$|/" + domain + "/|\." + domain + "/") } )
        except Exception as e:
            print(e)
            return None