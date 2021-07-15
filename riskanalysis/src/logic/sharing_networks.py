from neo4j import GraphDatabase

from ..common.constants import *

driver = GraphDatabase.driver(NEO4J['URI'])

class SharingNetworks(object):

    def getSharingNetworks(tilts):
        this = SharingNetworks()
        result = this.createSharingNetwork(tilts)

        return result

    def createSharingNetwork(tilts):
        session = driver.session()

        tx = session.begin_transaction()

        result = tx.run()   # Example: "CREATE (a:Person { name: $name }) RETURN id(a) AS node_id", name="Some String"
        record = result.single()

        tx.commit()
        tx.close()

        session.close()
        return record