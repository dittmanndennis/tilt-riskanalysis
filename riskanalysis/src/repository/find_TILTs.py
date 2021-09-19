import pymongo as pymongo
import re
import requests as req
from tld import get_fld

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

    def getBreaches(self, domain):
        data = req.get("https://haveibeenpwned.com/api/v3/breaches?domain=" + domain).json()
        
        breachCount = 0
        averageSeverity = 0
        for breach in data:
            breachCount += 1
            averageSeverity += breach["PwnCount"]
        if breachCount != 0:
            averageSeverity = averageSeverity/breachCount

        return [breachCount, averageSeverity]

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
                    breaches = this.getBreaches(domain)
                    numberOfBreaches = breaches[0]
                    severityOfBreaches = breaches[1]
                    marketCapitalization = 0
                    industrialSector = ""
                    if "riskAnalysis" in nextTILT:
                        #if "numberOfBreaches" in nextTILT["riskAnalysis"]:
                            #numberOfBreaches = nextTILT["riskAnalysis"]["numberOfBreaches"]
                        #if "severityOfBreaches" in nextTILT["riskAnalysis"]:
                            #severityOfBreaches = nextTILT["riskAnalysis"]["severityOfBreaches"]
                        if "marketCapitalization" in nextTILT["riskAnalysis"]:
                            marketCapitalization = nextTILT["riskAnalysis"]["marketCapitalization"]
                        if "industrialSector" in nextTILT["riskAnalysis"]:
                            industrialSector = nextTILT["riskAnalysis"]["industrialSector"]
                    
                    maximumDataTypes = 8163
                    lowerCaseTypes = []
                    for dataDisclosed in nextTILT["dataDisclosed"]:
                        if dataDisclosed["category"].lower() not in lowerCaseTypes:
                            maximumDataTypes -= (2 + len(dataDisclosed["category"].encode('utf-8')))
                            if maximumDataTypes >= 0:
                                lowerCaseTypes.append(dataDisclosed["category"].lower())
                                dataTypes.append(dataDisclosed["category"])
                        for recipient in dataDisclosed["recipients"]:
                            if "domain" not in recipient:
                                continue
                            if recipient["domain"] not in visitedTILTs:
                                nextTILTs.append(recipient["domain"])
                                visitedTILTs.append(recipient["domain"])
                    
                    properties.append([domain, country, numberOfBreaches, severityOfBreaches, dataTypes, marketCapitalization, industrialSector])
                
                else:
                    dataTypes = []
                    country = nextTILT["controller"]["country"]
                    breaches = this.getBreaches(domain)
                    numberOfBreaches = breaches[0]
                    severityOfBreaches = breaches[1]
                    marketCapitalization = 0
                    industrialSector = ""
                    
                    properties.append([domain, country, numberOfBreaches, severityOfBreaches, dataTypes, marketCapitalization, industrialSector])
            
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

    def getTILT(self, domain):
        try:
            return tiltCollection.find_one( { "meta.url": re.compile("^" + domain + "$|^" + domain + "/|/" +
            domain + "$|\." + domain + "$|/" + domain + "/|\." + domain + "/") },
            { "_id": 0, "meta.url": 1, "controller.country": 1, "dataDisclosed.category": 1, "riskanalysis.marketCapitalization": 1, "riskanalysis.industrialSector": 1, "dataDisclosed.recipients.domain": 1 } )
        except Exception as e:
            print(e)
            return None

    def allTILTs(self):
        try:
            return tiltCollection.find( {}, { "_id": 0, "meta.url": 1, "controller.country": 1, "dataDisclosed.category": 1, "riskanalysis.marketCapitalization": 1, "riskanalysis.industrialSector": 1, "dataDisclosed.recipients.domain": 1 } )
        except Exception as e:
            print(e)
            return None

    def nodeData(self, doc):
        breaches = FindTILTs().getBreaches(doc["meta"]["url"])
        
        categories = []
        recipients = []
        for category in doc["dataDisclosed"]:
            if "category" in category and len(category["category"]) > 0 and category["category"].lower() not in categories:
                categories.append(category["category"].lower())
                for recipient in category["recipients"]:
                    if "domain" in recipient and len(recipient["domain"]) > 0 and recipient["domain"].lower() not in recipients:
                        recipientBreaches = FindTILTs().getBreaches(recipient["domain"])
                        recipients.append([recipient["domain"].lower(), "", recipientBreaches[0], recipientBreaches[1], [], 0, ""])
        
        marketCapitalization = 0
        industrialSector = ""
        if "riskAnalysis" in doc:
                        if "marketCapitalization" in doc["riskAnalysis"]:
                            marketCapitalization = doc["riskAnalysis"]["marketCapitalization"]
                        if "industrialSector" in doc["riskAnalysis"]:
                            industrialSector = doc["riskAnalysis"]["industrialSector"]

        return [[doc["meta"]["url"], doc["controller"]["country"], breaches[0], breaches[1], categories, marketCapitalization, industrialSector], recipients]