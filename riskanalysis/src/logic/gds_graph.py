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

    def writeLouvain(self, graph_name):
        graph.run("CALL gds.louvain.write('" + graph_name + "', {writeProperty: 'louvain'})")

    def writeLabelPropagation(self, graph_name):
        graph.run("CALL gds.labelPropagation.write('" + graph_name + "', {writeProperty: 'labelPropagation'})")

    def writeWeaklyConnectedComponents(self, graph_name):
        graph.run("CALL gds.wcc.write('" + graph_name + "', {writeProperty: 'wcc'})")

    def writeTriangleCount(self, graph_name):
        graph.run("CALL gds.triangleCount.write('" + graph_name + "', {writeProperty: 'triangleCount'})")

    def writeLocalClusteringCoefficient(self, graph_name):
        graph.run("CALL gds.localClusteringCoefficient.write('" + graph_name + "', {writeProperty: 'localClusteringCoefficient'})")

    def writeNodeSimilarity(self, graph_name):
        graph.run("CALL gds.nodeSimilarity.write('" + graph_name + "', {writeRelationshipType: 'SIMILAR', writeProperty: 'similarity'})")