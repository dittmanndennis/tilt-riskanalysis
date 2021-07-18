from neo4j import GraphDatabase
from py2neo import Graph

from ..common.constants import *

driver = GraphDatabase.driver(NEO4J['URI'])
#graph = Graph(NEO4J['URI'])

class SharingNetworks(object):

    def getSharingNetworks(self, domain):
        this = SharingNetworks()
        result = None# = this.createSharingNetwork(domains)

        return result

    def getDomain(self, domain):
        session = driver.session()

        tx = session.begin_transaction()

        result = tx.run("CREATE ($domain:Domain {data_type: $domain, industrial_sector: $domain, organization_size: $domain}) RETURN id($domain) AS node_id", domain=domain)
        record = result.single()    #.value()

        tx.commit()
        tx.close()

        session.close()
        return record

    def createSharingNetwork(self, domains, connections):
        this = SharingNetworks()
        ids = []

        for domain in domains:
            ids.append(this.createNode(domain))

        for connection in connections:
            ids.append(this.createEdge(connection))

        print(ids)

        return len(ids)>0

    def createNode(self, domain):
        session = driver.session()

        tx = session.begin_transaction()

        result = tx.run("CREATE ($domain:Domain {data_type: $domain, industrial_sector: $domain, organization_size: $domain}) RETURN id($domain) AS node_id", domain=domain)
        record = result.single()    #.value()

        tx.commit()
        tx.close()

        session.close()
        return record

    def createEdge(self, connection):
        session = driver.session()

        tx = session.begin_transaction()

        result = tx.run("MATCH ($domain1:Domain), ($domain2:Domain) CREATE ($domain1)-[r:SENDS_DATA_TO]->($domain2) RETURN type(r)", domain1=connection[0], domain2=connection[1])
        record = result.single()    #.value()

        tx.commit()
        tx.close()

        session.close()
        return record