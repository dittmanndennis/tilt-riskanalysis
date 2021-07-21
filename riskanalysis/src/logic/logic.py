
from riskanalysis.src.logic.sharing_networks import SharingNetworks
from ..logic.find_TILTs import *

class Logic(object):

    def getRiskScore(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        tilts = find.findTILTs(domain)
        domains = find.findDomains(domain)
        connections = find.findConnections(domain)
        sharing.createSharingNetwork(domains, connections)

        # get subgraph
        childNodes = sharing.getChildNodes(domain)
        print(childNodes)
        numberChildNodes = sharing.getNumberChildRelationships(domain)
        print(numberChildNodes)
        sharing.getCluster(domain)
        
        return { "RiskScore": len(tilts) }