from py2neo import Graph, Node, Relationship
from collections import Counter

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class SharingNetworks(object):

    # returns the first matching node to the given domain
    def getDomain(self, domain):
        return graph.nodes.match("Domain", domain=domain).first()

    def existsDomain(self, domain):
        if(SharingNetworks().getDomain(domain) is None):
            return False
        return True

    # returns the first matching relationship to the given connection
    def getConnection(self, connection):
        this = SharingNetworks()
        a = this.getDomain(connection[0])
        b = this.getDomain(connection[1])
        return graph.relationships.match((a, b)).first()    #graph.relationships.match((a, b), "SEND_DATA_TO").first()

    def existsConnection(self, connection):
        if(SharingNetworks().getConnection(connection) is None):
            return False
        return True

    # https://stackoverflow.com/questions/44025445/how-to-get-all-childs-of-a-particular-node-in-neo4j
    # https://stackoverflow.com/questions/44237316/get-all-childs-of-a-particular-node-till-a-particular-depth
    # https://stackoverflow.com/questions/60701818/how-to-get-all-child-nodes-of-a-node
    def getChildNodes(self, parentDomain):
        query = 'MATCH (p:Domain)-[:SENDS_DATA_TO *]->(d:Domain) WHERE p.domain="' + parentDomain + '" WITH COLLECT (d) + p AS all UNWIND all as p MATCH (p)-[:SENDS_DATA_TO]->(d) RETURN p.domain'
        nodes = graph.run(query).data()

        childNodes = []
        visitedNodes = []
        for node in nodes:
            if node["p.domain"] not in visitedNodes:
                childNodes.append(node["p.domain"])
                visitedNodes.append(node["p.domain"])
        return childNodes

    def getNumberChildRelationships(self, parentDomain):
        query = 'MATCH (p:Domain)-[:SENDS_DATA_TO *]->(d:Domain) WHERE p.domain="' + parentDomain + '" WITH COLLECT (d) + p AS all UNWIND all as p MATCH (p)-[:SENDS_DATA_TO]->(d) RETURN p.domain'
        nodes = graph.run(query).data()
        if nodes is None:
            return 0
        return len(nodes)

    # https://towardsdatascience.com/hdbscan-clustering-with-neo4j-57e0cec57560?source=list-c74c18b6c78a----57e0cec57560----0-------8a45989e0731---------------------
    # https://medium.com/neo4j/k-means-clustering-with-neo4j-b0ec54bf0103
    # https://stackoverflow.com/questions/53629951/find-cluster-in-neo4j
    # https://stackoverflow.com/questions/49134739/how-to-return-top-n-biggest-cluster-in-neo4j
    # https://wiki.htw-berlin.de/confluence/display/~iclassen/graph
    def getCluster(self, parentDomain):
        query = 'MATCH (p:Domain)-[:SENDS_DATA_TO *]->(d:Domain) WHERE p.domain="' + parentDomain + '" WITH COLLECT (d) + p AS all UNWIND all as p MATCH (p)-[:SENDS_DATA_TO]->(d) RETURN p.domain'
        data = graph.run(query).data()

        nodes = []
        for node in data:
            nodes.append(node["p.domain"])
        
        count = Counter(nodes)
        print(count)

    # creates a sharing network with createNode() and createRelationship()
    def createSharingNetwork(self, domains, connections, properties):
        this = SharingNetworks()

        if(domains is not None and connections is not None):
            for property in properties:
                if(not this.existsDomain(property[0])):
                    this.createNode(property)

            for connection in connections:
                if(not this.existsConnection(connection)):
                    this.createRelationship(connection)

    # creates a node in the default database of the Neo4j instance
    # {0: domain}, {1: country}, {2: numberOfBreaches}, {3: severityOfBreaches}, {4: dataTypeShared[]}, {5: marketCapitalization}, {6: industrialSector}
    def createNode(self, properties):
        tx = graph.begin()
        
        a = Node("Domain", domain=properties[0], country=properties[1], numberOfBreaches=properties[2], severityOfBreaches=properties[3], dataTypes=properties[4], marketCapitalization=properties[5], industrialSector=properties[6])
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