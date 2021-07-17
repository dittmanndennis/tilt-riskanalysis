
from riskanalysis.src.logic.sharing_networks import SharingNetworks
from ..logic.find_TILTs import *

class Logic(object):

    def getRiskScore(self, domain):
        find = FindTILTs()
        sharing = SharingNetworks()

        #existingNetworks = sharing.getSharingNetworks(domain)
        #if len(existingNetworks<1):
        tilts = find.findTILTs(domain)
        domains = find.findDomains(domain)
        connections = find.findConnections(domain)
        sharing.createSharingNetwork(domains, connections)
        
        return { "RiskScore": len(tilts) }