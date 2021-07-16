from neo4j import GraphDatabase

from ..common.constants import *

driver = GraphDatabase.driver(NEO4J['URI'])

class SharingNetworks(object):

    def getSharingNetworks(tilts):
        this = SharingNetworks()
        result = this.createSharingNetwork(tilts)

        return result

    def createSharingNetwork(domain):
        session = driver.session()

        tx = session.begin_transaction()

        result = tx.run("CREATE (tilt:Domain {name: $name}) RETURN id(tilt) AS node_id", name=domain)
        record = result.single()

        tx.commit()
        tx.close()

        session.close()
        return record