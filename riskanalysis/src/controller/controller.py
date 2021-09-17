from ..repository.find_TILTs import *
from ..repository.sharing_networks import *
from ..logic.gds_graph import *

class Controller(object):

    def update(self):
        find = FindTILTs()
        sharing = SharingNetworks()

        properties = find.findProperties(domain)
        childNodes = sharing.getChildNodes(domain)

        if properties is not None and (len(properties)-1 is not len(childNodes) or len(childNodes) == 0):
            connections = find.findConnections(domain)
            #print(properties)
            sharing.createSharingNetwork(properties, connections)

        Graph().writeLouvain()
        cluster = Graph().distinctLouvainCluster()
        for c in cluster:
            Graph().writeArticleRankCluster(c)
            Graph().writeBetweennessCluster(c)
            Graph().writeDegreeCluster(c)
            Graph().writeHarmonicClosenessCluster(c)

    def getRiskScore(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        properties = find.findProperties(domain)
        childNodes = sharing.getChildNodes(domain)

        if properties is not None and (len(properties)-1 is not len(childNodes) or len(childNodes) == 0):
            connections = find.findConnections(domain)
            #print(properties)
            sharing.createSharingNetwork(properties, connections)

        return Graph().similarityProbability(domain)