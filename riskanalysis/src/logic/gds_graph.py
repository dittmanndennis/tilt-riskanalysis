from py2neo import Graph, Node, Relationship

from ..common.constants import *

# connects to the Neo4j instance
graph = Graph(NEO4J['URI'])

class Graph(object):

    def countNodesCluster(self, cluster):
        return graph.run("MATCH (n {louvain: " + str(cluster) + "}) RETURN count(n) AS count").data()[0]["count"]

    def setPropertyFirst(self, property, value):
        graph.run("MATCH (n) WHERE NOT EXISTS (n." + property + ") SET n." + property + " = '" + str(value) + "'")

    def setProperty(self, property, value):
        graph.run("MATCH (n) SET n." + property + " = '" + str(value) + "'")

    def setPropertyCluster(self, cluster, property, value):
        graph.run("MATCH (n {louvain: " + str(cluster) + "}) SET n." + property + " = '" + str(value) + "'")

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
        try:
            graph.run("CALL gds.alpha.articleRank.write('articleRankGraph', {writeProperty: 'articleRank'})")
        except Exception as e:
            Graph().setProperty("articleRank", 0)
            #print(e)
        Graph().__deleteGraph("articleRankGraph")

    def writeArticleRankCluster(self, cluster):
        Graph().__createLouvainGraph("articleRankGraph", cluster)
        try:
            graph.run("CALL gds.alpha.articleRank.write('articleRankGraph', {writeProperty: 'articleRank'})")
        except Exception as e:
            Graph().setPropertyCluster(cluster, "articleRank", 0)
            #print(e)
        Graph().__deleteGraph("articleRankGraph")

    def __writeEigenvector(self):
        Graph().__createGraph("eigenvectorGraph", "REVERSE")
        graph.run("CALL gds.alpha.eigenvector.write('eigenvectorGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvectorGraph")

    def __writeEigenvectorCluster(self, cluster):
        Graph().__createLouvainGraph("eigenvectorGraph", cluster)
        graph.run("CALL gds.alpha.eigenvector.write('eigenvectorGraph', {writeProperty: 'eigenvector'})")
        Graph().__deleteGraph("eigenvectorGraph")

    def writeBetweenness(self):
        Graph().__createGraph("betweennessGraph", "REVERSE")
        try:
            graph.run("CALL gds.betweenness.write('betweennessGraph', { writeProperty: 'betweenness' })")
        except Exception as e:
            Graph().setProperty("betweenness", 0)
            #print(e)
        Graph().__deleteGraph("betweennessGraph")

    def writeBetweennessCluster(self, cluster):
        Graph().__createLouvainGraph("betweennessGraph", cluster)
        try:
            graph.run("CALL gds.betweenness.write('betweennessGraph', { writeProperty: 'betweenness' })")
        except Exception as e:
            Graph().setPropertyCluster(cluster, "betweenness", 0)
            #print(e)
        Graph().__deleteGraph("betweennessGraph")

    def writeDegree(self):
        Graph().__createGraph("degreeGraph", "REVERSE")
        try:
            graph.run("CALL gds.alpha.degree.write('degreeGraph', { writeProperty: 'degree' })")
        except Exception as e:
            Graph().setProperty("degree", 0)
            #print(e)
        Graph().__deleteGraph("degreeGraph")

    def writeDegreeCluster(self, cluster):
        Graph().__createLouvainGraph("degreeGraph", cluster)
        try:
            graph.run("CALL gds.alpha.degree.write('degreeGraph', { writeProperty: 'degree' })")
        except Exception as e:
            Graph().setPropertyCluster(cluster, "degree", 0)
            #print(e)
        Graph().__deleteGraph("degreeGraph")

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
        try:
            graph.run("CALL gds.alpha.closeness.harmonic.write('harmonicClosenessGraph', {writeProperty: 'harmonicCloseness'})")
        except Exception as e:
            Graph().setProperty("harmonicCloseness", 0)
            #print(e)
        Graph().__deleteGraph("harmonicClosenessGraph")

    def writeHarmonicClosenessCluster(self, cluster):
        Graph().__createLouvainGraph("harmonicClosenessGraph", cluster)
        try:
            graph.run("CALL gds.alpha.closeness.harmonic.write('harmonicClosenessGraph', {writeProperty: 'harmonicCloseness'})")
        except Exception as e:
            Graph().setPropertyCluster(cluster, "harmonicCloseness", 0)
            #print(e)
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
        graph.run("MATCH (n) WITH {item: id(n), weights: [n.articleRank, n.betweenness, n.degree, n.harmonicCloseness]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.pearson.write({data: data, topK: 0, similarityCutoff: 0.1}) YIELD nodes, similarityPairs, writeRelationshipType, writeProperty, min, max, mean, stdDev, p25, p50, p75, p90, p95, p99, p999, p100 RETURN nodes, similarityPairs, writeRelationshipType, writeProperty, min, max, mean, p95")

    def euclideanSimilarityCluster(self, cluster):
        try:
            articleRankSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.articleRank]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg") #YIELD item1, item2, similarity RETURN gds.util.asNode(item1).domain AS from, gds.util.asNode(item2).domain AS to, similarity ORDER BY similarity DESC")
            print(articleRankSimilarity.data())
        except Exception as e:
            print(e)
        
        try:
            betweennessSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.betweenness]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg")
            print(betweennessSimilarity.data())
        except Exception as e:
            print(e)
        
        try:
            degreeSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.degree]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg")
            print(degreeSimilarity.data())
        except Exception as e:
            print(e)
        
        try:
            harmonicClosenessSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.harmonicCloseness]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg")
            print(harmonicClosenessSimilarity.data())
        except Exception as e:
            print(e)

    def writePearsonSimilarityBreached(self):
        graph.run("MATCH (n) WHERE n.numberOfBreaches>0 WITH {item: id(n), weights: [n.articleRank, n.betweenness, n.degree, n.harmonicCloseness]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.pearson.write({data: data, topK: 0, similarityCutoff: 0.1}) YIELD nodes, similarityPairs, writeRelationshipType, writeProperty, min, max, mean, stdDev, p25, p50, p75, p90, p95, p99, p999, p100 RETURN nodes, similarityPairs, writeRelationshipType, writeProperty, min, max, mean, p95")

    def trainNodeClassification(self):
        graph.run()

    def writeNodeClassification(self):
        graph.run()