from ..repository.find_TILTs import *
from ..repository.sharing_networks import *
from ..logic.gds_graph import *
from multiprocessing import Pool
from os import cpu_count
from tld import get_fld
from bson.json_util import dumps
import random
import string
import json
import os

class Controller:

    def update():
        find = FindTILTs()
        
        cursor = find.allTILTs()

        pool = Pool(cpu_count())
        changes = pool.map(Controller.multiUpdate, cursor)
        pool.close()
        pool.join()

        for c in changes:
            if c:
                Controller.calculateMeasures()
                break

        Controller.calculateRisks()

    def multiUpdate(doc):
        find = FindTILTs()
        sharing = SharingNetworks()
        changes = False
        
        doc["meta"]["url"] = get_fld(doc["meta"]["url"])
        nodeData = find.nodeData(doc)
        if not sharing.existsNode(doc["meta"]["url"]):
            changes = True
            sharing.createNode(nodeData[0])
        for recipient in nodeData[1]:
            if not sharing.existsNode(recipient[0]):
                changes = True
                sharing.createNode(recipient)
            if not sharing.existsRelationship([doc["meta"]["url"], recipient[0]]):
                changes = True
                sharing.createRelationship([doc["meta"]["url"], recipient[0]])

        return changes

    def updateDomain(domain):
        find = FindTILTs()
        sharing = SharingNetworks()
        changes = False
    
        doc = find.getTILT(domain)
        if doc is None:
            return True
        
        doc["meta"]["url"] = get_fld(doc["meta"]["url"])
        nodeData = find.nodeData(doc)
        if not sharing.existsNode(doc["meta"]["url"]):
            changes = True
            sharing.createNode(nodeData[0])
        for recipient in nodeData[1]:
            if not sharing.existsNode(recipient[0]):
                changes = True
                sharing.createNode(recipient)
            if not sharing.existsRelationship([doc["meta"]["url"], recipient[0]]):
                changes = True
                sharing.createRelationship([doc["meta"]["url"], recipient[0]])
                
        if changes:
            Controller.calculateMeasures()
        
        Controller.calculateRiskDomain(domain)
        
        return False

    def calculateMeasures():
        Graph().writeLouvain()
        cluster = Graph().distinctLouvainCluster()
        for c in cluster:
            print(c)
            Graph().writeArticleRankCluster(c["cluster"])
            Graph().writeBetweennessCluster(c["cluster"])
            Graph().writeDegreeCluster(c["cluster"])
            Graph().writeHarmonicClosenessCluster(c["cluster"])

    def calculateRiskDomain(domain):
        client = pymongo.MongoClient(
            host=MONGO['DOCKER'],
            port=MONGO['PORT'],
            username=MONGO['USERNAME'],
            password=MONGO['PASSWORD']
        )
        riskScoreCollection = client["RiskAnalysis"]["riskScore"]
        
        if riskScoreCollection.find_one( { "domain": domain } ) is None:
            riskScoreCollection.insert_one(Graph().similarityProbability(domain))

    def calculateRisks():
        client = pymongo.MongoClient(
            host=MONGO['DOCKER'],
            port=MONGO['PORT'],
            username=MONGO['USERNAME'],
            password=MONGO['PASSWORD']
        )
        riskScoreCollection = client["RiskAnalysis"]["riskScore"]

        domains = Graph().getDomains()
        
        for domain in domains:
            if riskScoreCollection.find_one( { "domain": domain["domain"] } ) is None:
                riskScoreCollection.insert_one(Graph().similarityProbability(domain["domain"]))

    def getRiskScore(domain):
        client = pymongo.MongoClient(
            host=MONGO['DOCKER'],
            port=MONGO['PORT'],
            username=MONGO['USERNAME'],
            password=MONGO['PASSWORD']
        )
        tiltCollection = client["RiskAnalysis"]["riskScore"]
        
        try:
            return json.loads(dumps(tiltCollection.find_one( { "domain": domain } )))
        except Exception as e:
            print(e)
            return { "ERROR": "Risk not found!" }

    def deleteGraph():
        Graph().dropDatabase()

    def deleteCollection(collection):
        client = pymongo.MongoClient(
            host=MONGO['DOCKER'],
            port=MONGO['PORT'],
            username=MONGO['USERNAME'],
            password=MONGO['PASSWORD']
        )
        tiltCollection = client["RiskAnalysis"][collection]

        tiltCollection.delete_many({})
    
    def removeProperties():
        properties = ["articleRank", "betweenness", "degree", "harmonicCloseness", "louvain"]

        for property in properties:
            Graph().removeProperty(property)

    def generate(i):
        domains = []
        for r in range(i):
            res = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 7))
            domains.append(res + ".com")
        print("Here")
        with open('./src/tilt/do-not-use.json') as f:  #./riskanalysis/src/tilt/do-not-use.json
            print("Here")
            file_data = json.load(f)
            for count in range(i):
                usedDomains = [count]
                file_data["meta"]["url"] = "https://" + domains[count]
                
                for recipient in file_data["dataDisclosed"][0]["recipients"]:
                    while True:
                        rand = random.randint(0, i-1)
                        if rand in usedDomains:
                            continue

                        usedDomains.append(rand)
                        recipient["domain"] = domains[rand]
                        break
                
                FindTILTs().postTILT(file_data.copy())

    def path():
        return { "path": os.path.abspath(__file__) }