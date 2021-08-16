from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class Graph(object):

    def distrinctLouvainCluster(self):
        return graph.run("MATCH (n:Domain) RETURN DISTINCT n.louvain")

    
    #Graph Data Science Stuff

    def __deleteGraph(self, graph_name):
        graph.run("CALL gds.graph.drop('" + graph_name + "')")

    def __createGraph(self, graph_name, orientation):
        graph.run("CALL gds.graph.create('" + graph_name + "', 'Domain', {SENDS_DATA_TO: {orientation: '" + orientation + "'}})")

    def __createLouvainGraph(self, graph_name, cluster):
        graph.run("CALL gds.graph.create.cypher('" + graph_name + "', 'MATCH (n:Domain {louvain: " + cluster + "}) RETURN id(n) as id', 'MATCH (n)-->(m) RETURN id(n) AS source, id(m) AS target')")

    # depreciated by writeArticleRank
    def __writePageRank(self):
        Graph().__createGraph("pageRankGraph", "REVERSE")
        graph.run("CALL gds.pageRank.write('pageRankGraph', {writeProperty: 'pageRank'})")
        Graph().__deleteGraph("pageRankGraph")

    def writeArticleRank(self):
        Graph().__createGraph("articleRankGraph", "REVERSE")
        graph.run("CALL gds.alpha.articleRank.write('articleRankGraph', {writeProperty: 'articleRank'})")
        Graph().__deleteGraph("articleRankGraph")

    def writeEigenvector(self):
        Graph().__createGraph("eigenvectorGraph", "REVERSE")
        graph.run("CALL gds.alpha.eigenvector.write('eigenvectorGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvectorGraph")

    # may not work
    def writeCloseness(self):
        Graph().__createGraph("closenessGraph", "REVERSE")
        graph.run("CALL gds.alpha.closeness.write('closenessGraph', {writeProperty: 'closeness'})")
        Graph().__deleteGraph("closenessGraph")

    def writeLouvain(self):
        Graph().__createGraph("louvainGraph", "REVERSE")
        graph.run("CALL gds.louvain.write('louvainGraph', {writeProperty: 'louvain'})")
        Graph().__deleteGraph("louvainGraph")

    def writeLabelPropagation(self):
        Graph().__createGraph("labelPropagationGraph", "REVERSE")
        graph.run("CALL gds.labelPropagation.write('labelPropagationGraph', {writeProperty: 'labelPropagation'})")
        Graph().__deleteGraph("labelPropagationGraph")

    def writeWeaklyConnectedComponents(self):
        Graph().__createGraph("weaklyConnectedComponentsGraph", "REVERSE")
        graph.run("CALL gds.wcc.write('weaklyConnectedComponentsGraph', {writeProperty: 'wcc'})")
        Graph().__deleteGraph("weaklyConnectedComponentsGraph")

    def writeTriangleCount(self):
        Graph().__createGraph("triangleCountGraph", "UNDIRECTED")
        graph.run("CALL gds.triangleCount.write('triangleCountGraph', {writeProperty: 'triangleCount'})")
        Graph().__deleteGraph("triangleCountGraph")

    def writeLocalClusteringCoefficient(self):
        Graph().__createGraph("localClusteringCoefficientGraph", "UNDIRECTED")
        graph.run("CALL gds.localClusteringCoefficient.write('localClusteringCoefficientGraph', {writeProperty: 'localClusteringCoefficient'})")
        Graph().__deleteGraph("localClusteringCoefficientGraph")

    def writeNodeSimilarity(self):
        Graph().__createGraph("nodeSimilarityGraph", "REVERSE")
        graph.run("CALL gds.nodeSimilarity.write('nodeSimilarityGraph', {writeRelationshipType: 'SIMILAR', writeProperty: 'similarity'})")
        Graph().__deleteGraph("nodeSimilarityGraph")