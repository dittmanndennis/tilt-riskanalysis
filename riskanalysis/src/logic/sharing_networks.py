from py2neo import Graph, Node, Relationship

from ..common.constants import *

graph = Graph(NEO4J['URI'])

class SharingNetworks(object):

    def getSharingNetworks(self, domain):
        this = SharingNetworks()
        result = None# = this.createSharingNetwork(domains)

        return result

    def getDomain(self, domain):
        return graph.nodes.match("Domain", domain=domain).first()

    def existsDomain(self, domain):
        return len(SharingNetworks().getDomain(domain))>0

    def getConnection(self, connection):
        this = SharingNetworks()
        a = this.getDomain(connection[0])
        b = this.getDomain(connection[1])
        return graph.relationships.match((a, b)).first()    #graph.relationships.match((a, b), "SEND_DATA_TO").first()

    def existsConnection(self, connection):
        return len(SharingNetworks().getConnection(connection))>0

    def createSharingNetwork(self, domains, connections):
        this = SharingNetworks()
        ids = []

        for domain in domains:
            if(not this.existsDomain(domain)):
                ids.append(this.createNode(domain))

        for connection in connections:
            if(not this.existsConnection(connection)):
                ids.append(this.createEdge(connection))

        print(ids)

        return len(ids)>0

    def createNode(self, domain):
        tx = graph.begin()

        a = Node("Domain", domain=domain)
        tx.create(a)

        tx.commit()

    def createEdge(self, connection):
        tx = graph.begin()

        a = graph.nodes.match("Domain", domain=connection[0]).first()
        b = graph.nodes.match("Domain", domain=connection[1]).first()

        ab = Relationship(a, "SENDS_DATA_TO", b)
        tx.create(ab)

        tx.commit()