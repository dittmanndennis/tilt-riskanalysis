from ..repository.find_TILTs import *
from ..repository.sharing_networks import *
from ..logic.gds_graph import *
from multiprocessing import Pool
from os import cpu_count
from tld import get_fld

class Controller:

    def update():
        find = FindTILTs()
        sharing = SharingNetworks()
        
        cursor = find.allTILTs()

        pool = Pool(cpu_count())
        changes = pool.map(Controller.multiUpdate, cursor)
        pool.close()
        pool.join()

        for c in changes:
            if c:
                Controller.calculateMeasures()
                break

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
            Controller().calculateMeasures()
        return False

    def calculateMeasures():
        print("here")
        Graph().writeLouvain()
        print("here")
        cluster = Graph().distinctLouvainCluster()
        print("here")
        for c in cluster:
            Graph().writeArticleRankCluster(c["cluster"])
            Graph().writeBetweennessCluster(c["cluster"])
            Graph().writeDegreeCluster(c["cluster"])
            Graph().writeHarmonicClosenessCluster(c["cluster"])
        print("here")

    def getRiskScore(domain):
        return Graph().similarityProbability(domain)