from ..repository.find_TILTs import *
from ..repository.sharing_networks import *

class Controller(object):

    def getRiskScore(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        domains = find.findDomains(domain)
        childNodes = sharing.getChildNodes(domain)
        
        if domains is not None and len(domains) is not len(childNodes):
            connections = find.findConnections(domain)
            properties = find.findProperties(domain)
            sharing.createSharingNetwork(domains, connections, properties)

            # get subgraph
            numberChildNodes = sharing.getNumberChildRelationships(domain)

            return { "RiskScore": len(domains) }
        
        return { "RiskScore": domains }