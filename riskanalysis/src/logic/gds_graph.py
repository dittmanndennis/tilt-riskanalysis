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

    def pearsonSimilarityMeasures(self, cluster, measures):
        # Article, Betweenness, Degree, Closeness
        #measures = [True, True, True, True]

        item = graph.run("MATCH (n {louvain: " + str(cluster) + "}) RETURN id(n) AS item LIMIT 1").data()[0]
        try:
            articleBetweenness = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH [{item: " + str(item["item"]) + ", weights: collect(n.articleRank)}, {item: " + str(item["item"]) + ", weights: collect(n.betweenness)}] as data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]["similarity"]
        except Exception as e:
            #print(e)
            articleBetweenness = 1.0
        try:
            articleDegree = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH [{item: " + str(item["item"]) + ", weights: collect(n.articleRank)}, {item: " + str(item["item"]) + ", weights: collect(n.degree)}] as data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]["similarity"]
        except Exception as e:
            #print(e)
            articleDegree = 1.0
        try:
            articleCloseness = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH [{item: " + str(item["item"]) + ", weights: collect(n.articleRank)}, {item: " + str(item["item"]) + ", weights: collect(n.harmonicCloseness)}] as data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]["similarity"]
        except Exception as e:
            #print(e)
            articleCloseness = 1.0
        try:
            betweennessDegree = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH [{item: " + str(item["item"]) + ", weights: collect(n.betweenness)}, {item: " + str(item["item"]) + ", weights: collect(n.degree)}] as data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]["similarity"]
        except Exception as e:
            #print(e)
            betweennessDegree = 1.0
        try:
            betweennessCloseness = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH [{item: " + str(item["item"]) + ", weights: collect(n.betweenness)}, {item: " + str(item["item"]) + ", weights: collect(n.harmonicCloseness)}] as data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]["similarity"]
        except Exception as e:
            #print(e)
            betweennessCloseness = 1.0
        try:
            degreeCloseness = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH [{item: " + str(item["item"]) + ", weights: collect(n.degree)}, {item: " + str(item["item"]) + ", weights: collect(n.harmonicCloseness)}] as data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]["similarity"]
        except Exception as e:
            #print(e)
            degreeCloseness = 1.0

        #Degree can always be calculated
        if articleBetweenness == 1.0 and articleDegree == 1.0 and articleCloseness == 1.0 and betweennessDegree == 1.0 and betweennessCloseness == 1.0 and degreeCloseness == 1.0:
            return [False, False, True, False]
        
        if measures[0] and measures[1] and articleBetweenness >= 0.8:
            if (articleDegree + 1.0) + (articleCloseness + 1.0) < (betweennessDegree + 1.0) + (betweennessCloseness + 1.0):
                measures[1] = False
            else:
                measures[0] = False
        if measures[0] and measures[2] and articleDegree >= 0.8:
            if (articleBetweenness + 1.0) + (articleCloseness + 1.0) < (betweennessDegree + 1.0) + (degreeCloseness + 1.0):
                measures[2] = False
            else:
                measures[0] = False
        if measures[0] and measures[3] and articleCloseness >= 0.8:
            if (articleBetweenness + 1.0) + (articleDegree + 1.0) < (betweennessCloseness + 1.0) + (degreeCloseness + 1.0):
                measures[3] = False
            else:
                measures[0] = False
        if measures[1] and measures[2] and betweennessDegree >= 0.8:
            if (articleBetweenness + 1.0) + (betweennessCloseness + 1.0) < (articleDegree + 1.0) + (degreeCloseness + 1.0):
                measures[2] = False
            else:
                measures[1] = False
        if measures[1] and measures[3] and betweennessCloseness >= 0.8:
            if (articleBetweenness + 1.0) + (betweennessDegree + 1.0) < (articleCloseness + 1.0) + (degreeCloseness + 1.0):
                measures[2] = False
            else:
                measures[1] = False
        if measures[2] and measures[3] and degreeCloseness >= 0.8:
            if (articleDegree + 1.0) + (betweennessDegree + 1.0) < (articleCloseness + 1.0) + (betweennessCloseness + 1.0):
                measures[3] = False
            else:
                measures[2] = False
        if measures[3] and articleCloseness == 1.0 and betweennessCloseness == 1.0 and degreeCloseness == 1.0:
            measures[3] = False
            
        return measures

    def pearsonSimilarityNodes(self, node, breachedNode, comparedSimilarity):
            if comparedSimilarity[0] and comparedSimilarity[1] and comparedSimilarity[2] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.betweenness, n.degree, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]

            elif comparedSimilarity[0] and comparedSimilarity[1] and comparedSimilarity[2]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.betweenness, n.degree]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[0] and comparedSimilarity[1] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.betweenness, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[0] and comparedSimilarity[2] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.degree, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[1] and comparedSimilarity[2] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.betweenness, n.degree, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[0] and comparedSimilarity[1]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.betweenness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[0] and comparedSimilarity[2]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.degree]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[0] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[1] and comparedSimilarity[2]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.betweenness, n.degree]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[1] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.betweenness, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[2] and comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.degree, n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[0]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.articleRank]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[1]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.betweenness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[2]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.degree]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
                
            elif comparedSimilarity[3]:
                return graph.run("MATCH (n) WHERE n.domain = '" + str(node) + "' OR n.domain = '" + str(breachedNode) + "' WITH {item: id(n), weights: [n.harmonicCloseness]} AS dataMeasures WITH collect(dataMeasures) AS data CALL gds.alpha.similarity.pearson.stream({data: data, topK: 0}) YIELD similarity RETURN similarity ORDER BY similarity DESC").data()[0]
            
            return None

    def euclideanSimilarityCluster(self, cluster):
        try:
            articleRankSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.articleRank]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg").data()[0]["similarityAvg"] #YIELD item1, item2, similarity RETURN gds.util.asNode(item1).domain AS from, gds.util.asNode(item2).domain AS to, similarity ORDER BY similarity DESC")
        except Exception as e:
            #print(e)
            articleRankSimilarity = 0.0
        
        try:
            betweennessSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.betweenness]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg").data()[0]["similarityAvg"]
        except Exception as e:
            #print(e)
            betweennessSimilarity = 0.0
        
        try:
            degreeSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.degree]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg").data()[0]["similarityAvg"]
            if degreeSimilarity is None:
                degreeSimilarity = 0.0
        except Exception as e:
            #print(e)
            degreeSimilarity = 0.0
        
        try:
            harmonicClosenessSimilarity = graph.run("MATCH (n {louvain: " + str(cluster) + "}) WITH {item: id(n), weights: [n.harmonicCloseness]} AS userData WITH collect(userData) AS data CALL gds.alpha.similarity.euclidean.stream({data: data, topK: 0}) YIELD similarity RETURN avg(similarity) AS similarityAvg").data()[0]["similarityAvg"]
        except Exception as e:
            #print(e)
            harmonicClosenessSimilarity = 0.0

        # Article, Betweenness, Degree, Closeness
        measures = [True, True, True, True]

        if articleRankSimilarity < 0.1:
            measures[0] = False
        if betweennessSimilarity < 0.1:
            measures[1] = False
        if degreeSimilarity < 0.1:
            measures[2] = False
        if harmonicClosenessSimilarity < 0.1:
            measures[3] = False
            
        return measures

    def similarityProbability(self, domain):
        similarity = []

        domainCluster = graph.run("MATCH (n) WHERE n.domain = '" + str(domain) + "' RETURN n.louvain AS cluster").data()[0]["cluster"]

        validDomainMeasures = Graph().euclideanSimilarityCluster(domainCluster)
        similarityDomain = Graph().pearsonSimilarityMeasures(domainCluster, validDomainMeasures)
        #print(similarityDomain)

        cluster = graph.run("MATCH (n) RETURN DISTINCT n.louvain AS cluster").data()
        for c in cluster:
            validMeasures = Graph().euclideanSimilarityCluster(c["cluster"])
            similarityCluster = Graph().pearsonSimilarityMeasures(c["cluster"], validMeasures)

            comparedSimilarity = [similarityDomain[0] and similarityCluster[0]]
            comparedSimilarity.append(similarityDomain[1] and similarityCluster[1])
            comparedSimilarity.append(similarityDomain[2] and similarityCluster[2])
            comparedSimilarity.append(similarityDomain[3] and similarityCluster[3])
            #print(comparedSimilarity)

            bestEntry = 0.9
            if c["cluster"] == domainCluster:
                bestEntry = 1.0
            bestNodes = []
            clusterNodes = graph.run("MATCH (n {louvain: " + str(c["cluster"]) + "}) RETURN n.domain AS domain, n.numberOfBreaches AS breaches, n.louvain AS cluster").data()
            for n in clusterNodes:
                if n["domain"] is not None and domain not in n["domain"]:
                    sim = Graph().pearsonSimilarityNodes(domain, n["domain"], comparedSimilarity)
                    if sim["similarity"] == 1.0:
                        bestEntry = 1.0
                        bestNodes.clear()
                        similarity.append(n)
                    elif sim["similarity"] > bestEntry:
                        bestEntry = sim
                        bestNodes.clear()
                        bestNodes.append(n)
                    elif sim["similarity"] == bestEntry:
                        bestNodes.append(n)
            
            if bestEntry < 1.0:
                similarity.extend(bestNodes)
        
        if len(similarity) == 0:
            return graph.run("MATCH (n) WHERE n.numberOfBreaches > 0  MATCH (m) RETURN toFloat(count(DISTINCT n)) / toFloat(count(DISTINCT m)) AS riskScore").data()[0]["riskScore"]

        breachedNodes = []
        for n in similarity:
            if n["breaches"] > 0:
                breachedNodes.append(n)

        print(similarity)
        
        return len(breachedNodes) / (len(similarity))

    def trainNodeClassification(self):
        graph.run()

    def writeNodeClassification(self):
        graph.run()