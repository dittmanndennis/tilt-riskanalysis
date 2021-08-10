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
    def __writePageRank(self):
        Graph().__createGraph("pageRankGraph")
        graph.run("CALL gds.pageRank.write('pageRankGraph', {writeProperty: 'pageRank'})")
        Graph().__deleteGraph("pageRankGraph")

    def writeArticleRank(self):
        Graph().__createGraph("articleRankGraph")
        graph.run("CALL gds.alpha.articleRank.write('articleRankGraph', {writeProperty: 'articleRank'})")
        Graph().__deleteGraph("articleRankGraph")

    def writeEigenvector(self):
        Graph().__createGraph("eigenvectorGraph")
        graph.run("CALL gds.eigenvector.write('eigenvectorGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvectorGraph")

    # may not work
    def writeCloseness(self):
        Graph().__createGraph("closenessGraph")
        graph.run("CALL gds.alpha.closeness.write('closenessGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("closenessGraph")

    def writeLouvain(self):
        Graph().__createGraph("louvainGraph")
        graph.run("CALL gds.louvain.write('louvainGraph', {writeProperty: 'louvain'})")
        Graph().__deleteGraph("louvainGraph")

    def writeLabelPropagation(self):
        Graph().__createGraph("labelPropagationGraph")
        graph.run("CALL gds.labelPropagation.write('labelPropagationGraph', {writeProperty: 'labelPropagation'})")
        Graph().__deleteGraph("labelPropagationGraph")

    def writeWeaklyConnectedComponents(self):
        Graph().__createGraph("weaklyConnectedComponentsGraph")
        graph.run("CALL gds.wcc.write('weaklyConnectedComponentsGraph', {writeProperty: 'wcc'})")
        Graph().__deleteGraph("weaklyConnectedComponentsGraph")

    def writeTriangleCount(self):
        Graph().__createGraph("triangleCountGraph")
        graph.run("CALL gds.triangleCount.write('triangleCountGraph', {writeProperty: 'triangleCount'})")
        Graph().__deleteGraph("triangleCountGraph")

    def writeLocalClusteringCoefficient(self):
        Graph().__createGraph("localClusteringCoefficientGraph")
        graph.run("CALL gds.localClusteringCoefficient.write('localClusteringCoefficientGraph', {writeProperty: 'localClusteringCoefficient'})")
        Graph().__deleteGraph("localClusteringCoefficientGraph")

    def writeNodeSimilarity(self):
        Graph().__createGraph("nodeSimilarityGraph")
        graph.run("CALL gds.nodeSimilarity.write('nodeSimilarityGraph', {writeRelationshipType: 'SIMILAR', writeProperty: 'similarity'})")
        Graph().__deleteGraph("nodeSimilarityGraph")