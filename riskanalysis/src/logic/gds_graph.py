from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class Graph(object):

    def __deleteGraph(self, graph_name):
        graph.run("CALL gds.graph.drop('" + graph_name + "')")

    def __createGraph(self, graph_name):
        graph.run("CALL gds.graph.create('" + graph_name + "', 'Domain', {SENDS_DATA_TO: {orientation: 'REVERSE'}})")

    def writePageRank(self, graph_name):
        Graph().__createGraph("pageRank")
        graph.run("CALL gds.pageRank.write('" + graph_name + "', {writeProperty: 'pageRank'})")
        Graph().__deleteGraph("pageRank")

    def writeArticleRank(self, graph_name):
        Graph().__createGraph("articleRank")
        graph.run("CALL gds.articleRank.write('" + graph_name + "', {writeProperty: 'articleRank'})")
        Graph().__deleteGraph("articleRank")

    def writeEigenvector(self, graph_name):
        Graph().__createGraph("eigenvector")
        graph.run("CALL gds.eigenvector.write('" + graph_name + "', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvector")

    def writeLouvain(self, graph_name):
        Graph().__createGraph("louvain")
        graph.run("CALL gds.louvain.write('" + graph_name + "', {writeProperty: 'louvain'})")
        Graph().__deleteGraph("louvain")

    def writeLabelPropagation(self, graph_name):
        Graph().__createGraph("labelPropagation")
        graph.run("CALL gds.labelPropagation.write('" + graph_name + "', {writeProperty: 'labelPropagation'})")
        Graph().__deleteGraph("labelPropagation")

    def writeWeaklyConnectedComponents(self, graph_name):
        Graph().__createGraph("connectedComponents")
        graph.run("CALL gds.wcc.write('" + graph_name + "', {writeProperty: 'wcc'})")
        Graph().__deleteGraph("connectedComponents")

    def writeTriangleCount(self, graph_name):
        Graph().__createGraph("triangleCount")
        graph.run("CALL gds.triangleCount.write('" + graph_name + "', {writeProperty: 'triangleCount'})")
        Graph().__deleteGraph("triangleCount")

    def writeLocalClusteringCoefficient(self, graph_name):
        Graph().__createGraph("clusteringCoefficient")
        graph.run("CALL gds.localClusteringCoefficient.write('" + graph_name + "', {writeProperty: 'localClusteringCoefficient'})")
        Graph().__deleteGraph("clusteringCoefficient")

    def writeNodeSimilarity(self, graph_name):
        Graph().__createGraph("nodeSimilarity")
        graph.run("CALL gds.nodeSimilarity.write('" + graph_name + "', {writeRelationshipType: 'SIMILAR', writeProperty: 'similarity'})")
        Graph().__deleteGraph("nodeSimilarity")