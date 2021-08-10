from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class Graph(object):

    def __deleteGraph(self, graph_name):
        graph.run("CALL gds.graph.drop('" + graph_name + "')")

    def __createGraph(self, graph_name):
        graph.run("CALL gds.graph.create('" + graph_name + "', 'Domain', {SENDS_DATA_TO: {orientation: 'REVERSE'}})")

    # depreciated by writeArticleRank
    def __writePageRank(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.pageRank.write('" + graph_name + "', {writeProperty: 'pageRank'})")
        Graph().__deleteGraph(graph_name)

    def writeArticleRank(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.articleRank.write('" + graph_name + "', {writeProperty: 'articleRank'})")
        Graph().__deleteGraph(graph_name)

    def writeEigenvector(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.eigenvector.write('" + graph_name + "', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph(graph_name)

    # may not work
    def writeCloseness(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.alpha.closeness.write('" + graph_name + "', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph(graph_name)

    def writeLouvain(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.louvain.write('" + graph_name + "', {writeProperty: 'louvain'})")
        Graph().__deleteGraph(graph_name)

    def writeLabelPropagation(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.labelPropagation.write('" + graph_name + "', {writeProperty: 'labelPropagation'})")
        Graph().__deleteGraph(graph_name)

    def writeWeaklyConnectedComponents(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.wcc.write('" + graph_name + "', {writeProperty: 'wcc'})")
        Graph().__deleteGraph(graph_name)

    def writeTriangleCount(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.triangleCount.write('" + graph_name + "', {writeProperty: 'triangleCount'})")
        Graph().__deleteGraph(graph_name)

    def writeLocalClusteringCoefficient(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.localClusteringCoefficient.write('" + graph_name + "', {writeProperty: 'localClusteringCoefficient'})")
        Graph().__deleteGraph(graph_name)

    def writeNodeSimilarity(self, graph_name):
        Graph().__createGraph(graph_name)
        graph.run("CALL gds.nodeSimilarity.write('" + graph_name + "', {writeRelationshipType: 'SIMILAR', writeProperty: 'similarity'})")
        Graph().__deleteGraph(graph_name)