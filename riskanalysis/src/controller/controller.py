from ..repository.find_TILTs import *
from ..repository.sharing_networks import *

class Controller(object):

    def getRiskScore(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        tilts = find.findTILTs(domain)
        domains = find.findDomains(domain)
        connections = find.findConnections(domain)
        sharing.createSharingNetwork(domains, connections)

        # get subgraph
        childNodes = sharing.getChildNodes(domain)
        numberChildNodes = sharing.getNumberChildRelationships(domain)
        
        return { "RiskScore": len(tilts) }