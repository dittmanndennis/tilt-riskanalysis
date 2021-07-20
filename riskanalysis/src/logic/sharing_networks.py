from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class SharingNetworks(object):

    # returns the first matching node to the given domain
    def getDomain(self, domain):
        return graph.nodes.match("Domain", domain=domain).first()

    def existsDomain(self, domain):
        return len(SharingNetworks().getDomain(domain))>0

    # returns the first matching relationship to the given connection
    def getConnection(self, connection):
        this = SharingNetworks()
        a = this.getDomain(connection[0])
        b = this.getDomain(connection[1])
        return graph.relationships.match((a, b)).first()    #graph.relationships.match((a, b), "SEND_DATA_TO").first()

    def existsConnection(self, connection):
        return len(SharingNetworks().getConnection(connection))>0

    def getChildNodes(self, parentDomain):
        query = 'MATCH (p:Domain)-[:SENDS_DATA_TO *]->(d:Domain) WHERE p.domain="' + parentDomain + '" WITH COLLECT (d) + p AS all UNWIND all as p MATCH (p)-[:SENDS_DATA_TO]->(d) RETURN p,d'
        return graph.run(query).data()

    # creates a sharing network with createNode() and createRelationship()
    def createSharingNetwork(self, domains, connections):
        this = SharingNetworks()

        for domain in domains:
            if(not this.existsDomain(domain)):
                this.createNode(domain)

        for connection in connections:
            if(not this.existsConnection(connection)):
                this.createRelationship(connection)

    # creates a node in the default database of the Neo4j instance
    def createNode(self, domain):
        tx = graph.begin()

        a = Node("Domain", domain=domain)
        tx.create(a)

        tx.commit()

    # creates a relationship in the default database of the Neo4j instance
    def createRelationship(self, connection):
        tx = graph.begin()

        a = graph.nodes.match("Domain", domain=connection[0]).first()
        b = graph.nodes.match("Domain", domain=connection[1]).first()

        ab = Relationship(a, "SENDS_DATA_TO", b)
        tx.create(ab)

        tx.commit()