from ..repository.find_TILTs import *
from ..repository.sharing_networks import *

class Controller(object):

    def getRiskScore(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        properties = find.findProperties(domain)
        childNodes = sharing.getChildNodes(domain)
        
        if properties is not None and len(properties)-1 is not len(childNodes):
            connections = find.findConnections(domain)
            sharing.createSharingNetwork(properties, connections)

            # get subgraph
            numberChildNodes = sharing.getNumberChildRelationships(domain)

            return { "RiskScore": len(properties) }
        
        return { "RiskScore": properties }