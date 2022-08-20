import numpy
class levenshteinDistance():
    @staticmethod
    def levenshteinDistanceDP(word1: str, word2: str) -> int:
        distances = numpy.zeros((len(word1) + 1, len(word2) + 1))
    
        for t1 in range(len(word1) + 1):
            distances[t1][0] = t1
    
        for t2 in range(len(word2) + 1):
            distances[0][t2] = t2
            
        a = 0
        b = 0
        c = 0
        
        for t1 in range(1, len(word1) + 1):
            for t2 in range(1, len(word2) + 1):
                if (word1[t1-1] == word2[t2-1]):
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]
                    
                    distances[t1][t2] = min(a, b, c) + 1
    
        #levenshteinDistance.printDistances(distances, len(word1), len(word2))
        return distances[len(word1)][len(word2)]
    
    @staticmethod
    def printDistances(distances, token1Length, token2Length):
        for t1 in range(token1Length + 1):
            for t2 in range(token2Length + 1):
                print(int(distances[t1][t2]), end=" ")
            print()