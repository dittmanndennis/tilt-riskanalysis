from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class Graph(object):

    def deleteGraph(self, graph_name):
        graph.run("CALL gds.graph.drop('" + graph_name + "')")

    def createGraph(self, graph_name):
        graph.run("CALL gds.graph.create('" + graph_name + "', 'Domain', {SENDS_DATA_TO: {orientation: 'REVERSE'}})")

    def writePageRank(self, graph_name):
        graph.run("CALL gds.pageRank.write('" + graph_name + "', {writeProperty: 'pageRank'})")

    def writeArticleRank(self, graph_name):
        graph.run("CALL gds.articleRank.write('" + graph_name + "', {writeProperty: 'articleRank'})")

    def writeEigenvector(self, graph_name):
        graph.run("CALL gds.eigenvector.write('" + graph_name + "', {writeProperty: 'eigenvector'})")