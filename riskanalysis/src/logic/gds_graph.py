from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class Graph(object):

    def distinctLouvainCluster(self):
        return graph.run("MATCH (n:Domain) RETURN DISTINCT n.louvain")

    def breachedDomains(self):
        return graph.run("MATCH (n) WHERE n.numberOfBreaches>0 RETURN id(n)")
    
    #Graph Data Science Stuff

    def __deleteGraph(self, graph_name):
        graph.run("CALL gds.graph.drop('" + graph_name + "')")

    def __createGraph(self, graph_name, orientation):
        graph.run("CALL gds.graph.create('" + graph_name + "', 'Domain', {SENDS_DATA_TO: {orientation: '" + orientation + "'}})")

    def __createLouvainGraph(self, graph_name, cluster):
        graph.run("CALL gds.graph.create.cypher('" + graph_name + "', 'MATCH (n:Domain {louvain: " + str(cluster) + "}) RETURN id(n) as id', 'MATCH (n {louvain: " + str(cluster) + "})-[rel:SENDS_DATA_TO]->(m) RETURN id(n) AS source, id(m) AS target')")

    # depreciated by writeArticleRank
    def __writePageRank(self):
        Graph().__createGraph("pageRankGraph", "REVERSE")
        graph.run("CALL gds.pageRank.write('pageRankGraph', {writeProperty: 'pageRank'})")
        Graph().__deleteGraph("pageRankGraph")

    def writeArticleRank(self):
        Graph().__createGraph("articleRankGraph", "REVERSE")
        graph.run("CALL gds.alpha.articleRank.write('articleRankGraph', {writeProperty: 'articleRank'})")
        Graph().__deleteGraph("articleRankGraph")

    def writeArticleRankCluster(self, cluster):
        Graph().__createLouvainGraph("articleRankGraph", cluster)
        graph.run("CALL gds.alpha.articleRank.write('articleRankGraph', {writeProperty: 'articleRank'})")
        Graph().__deleteGraph("articleRankGraph")

    def writeEigenvector(self):
        Graph().__createGraph("eigenvectorGraph", "REVERSE")
        graph.run("CALL gds.alpha.eigenvector.write('eigenvectorGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvectorGraph")

    def writeEigenvectorCluster(self, cluster):
        Graph().__createLouvainGraph("eigenvectorGraph", cluster)
        graph.run("CALL gds.alpha.eigenvector.write('eigenvectorGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvectorGraph")

    def writeBetweenness(self):
        Graph().__createGraph("betweennessGraph", "REVERSE")
        graph.run("CALL gds.betweenness.write('betweennessGraph', { writeProperty: 'betweenness' })")
        Graph().__deleteGraph("betweennessGraph")

    def writeBetweennessCluster(self, cluster):
        Graph().__createLouvainGraph("betweennessGraph", cluster)
        graph.run("CALL gds.betweenness.write('betweennessGraph', { writeProperty: 'betweenness' })")
        Graph().__deleteGraph("betweennessGraph")

    def writeDegree(self):
        Graph().__createGraph("degreeGraph", "REVERSE")
        graph.run("CALL gds.degree.write('degreeGraph', { writeProperty: 'degree' })")
        Graph().__deleteGraph("degreeGraph")

    def writeDegreeCluster(self, cluster):
        print("Here")
        Graph().__createLouvainGraph("degreeGraph", cluster)
        print("Here")
        graph.run("CALL gds.degree.write('degreeGraph', { writeProperty: 'degree' })")
        print("Here")
        Graph().__deleteGraph("degreeGraph")
        print("Here")

    # depreciated through writeHarmonicCloseness
    def __writeCloseness(self):
        Graph().__createGraph("closenessGraph", "REVERSE")
        graph.run("CALL gds.alpha.closeness.write('closenessGraph', {writeProperty: 'closeness'})")
        Graph().__deleteGraph("closenessGraph")

    # depreciated through writeHarmonicClosenessCluster
    def __writeClosenessCluster(self, cluster):
        Graph().__createLouvainGraph("closenessGraph", cluster)
        graph.run("CALL gds.alpha.closeness.write('closenessGraph', {writeProperty: 'closeness'})")
        Graph().__deleteGraph("closenessGraph")

    def writeHarmonicCloseness(self):
        Graph().__createGraph("harmonicClosenessGraph", "REVERSE")
        graph.run("CALL gds.alpha.closeness.harmonic.write('harmonicClosenessGraph', {writeProperty: 'harmonicCloseness'})")
        Graph().__deleteGraph("harmonicClosenessGraph")

    def writeHarmonicClosenessCluster(self, cluster):
        Graph().__createLouvainGraph("harmonicClosenessGraph", cluster)
        graph.run("CALL gds.alpha.closeness.harmonic.write('harmonicClosenessGraph', {writeProperty: 'harmonicCloseness'})")
        Graph().__deleteGraph("harmonicClosenessGraph")

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

    def writePearsonSimilarity(self):
        graph.run("MATCH (n) WITH {item:id(n), weights: [n.articleRank, n.eigenvector, n.betweenness, n.degree, n.closeness]} AS userData WITH collect(userData) as data CALL gds.alpha.similarity.pearson.write({data: data, topK: 1, similarityCutoff: 0.1}) YIELD nodes, similarityPairs, writeRelationshipType, writeProperty, min, max, mean, stdDev, p25, p50, p75, p90, p95, p99, p999, p100 RETURN nodes, similarityPairs, writeRelationshipType, writeProperty, min, max, mean, p95")

    def trainNodeClassification(self):
        graph.run()

    def writeNodeClassification(self):
        graph.run()