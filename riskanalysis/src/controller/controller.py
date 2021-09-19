from ..repository.find_TILTs import *
from ..repository.sharing_networks import *
from ..logic.gds_graph import *
from tld import get_fld

class Controller(object):

    def update(self):
        find = FindTILTs()
        sharing = SharingNetworks()
        
        changes = False
        cursor = find.allTILTs()

        for doc in cursor:
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
            Graph().writeLouvain()
            cluster = Graph().distinctLouvainCluster()
            for c in cluster:
                Graph().writeArticleRankCluster(c)
                Graph().writeBetweennessCluster(c)
                Graph().writeDegreeCluster(c)
                Graph().writeHarmonicClosenessCluster(c)

    def updateDomain(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        changes = False
        doc = find.getTILT(domain)

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
            Graph().writeLouvain()
            cluster = Graph().distinctLouvainCluster()
            for c in cluster:
                Graph().writeArticleRankCluster(c)
                Graph().writeBetweennessCluster(c)
                Graph().writeDegreeCluster(c)
                Graph().writeHarmonicClosenessCluster(c)

    def calculateMeasures(self):
        Graph().writeLouvain()
        cluster = Graph().distinctLouvainCluster()
        for c in cluster:
            Graph().writeArticleRankCluster(c["cluster"])
            Graph().writeBetweennessCluster(c["cluster"])
            Graph().writeDegreeCluster(c["cluster"])
            Graph().writeHarmonicClosenessCluster(c["cluster"])

    def getRiskScore(self, domain):
        return Graph().similarityProbability(domain)