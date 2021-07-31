from ..repository.find_TILTs import *
from ..repository.sharing_networks import *

class Controller(object):

    def getRiskScore(self, domain):
        find = FindTILTs()
        domains = find.findDomains(domain)
        
        if domains is not None:
            sharing = SharingNetworks()
            
            connections = find.findConnections(domain)
            sharing.createSharingNetwork(domains, connections)

            # get subgraph
            childNodes = sharing.getChildNodes(domain)
            numberChildNodes = sharing.getNumberChildRelationships(domain)

            return { "RiskScore": len(domains) }
        
        return { "RiskScore": domains }