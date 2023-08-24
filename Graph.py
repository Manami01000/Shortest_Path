import numpy as np
import sys


class Vertex:
    def __init__(self, value):
        self.value = value
        self.distance = sys.maxsize
        self.previous = None



class Graph:
    def __init__(self, matrix, weight=1):
        self.matrix = matrix
        self.vertices = {i: Vertex(i) for i in range(len(self.matrix))}
        self.weight = weight

    def dijkstra(self, source_vertex, destination_vertex):
        for i in self.vertices:
            self.vertices[i].distance = sys.maxsize
            self.vertices[i].previous = None

        spt_set = np.array([False for i in range(len(self.matrix))])  # vertices visiteds
        self.vertices[source_vertex].distance = 0

        while not spt_set[destination_vertex]:
            not_in_spt_set = np.array([self.vertices[i] for i in range(len(spt_set)) if not spt_set[i]])
            min_v = min(not_in_spt_set, key=lambda v: v.distance)  # gets the minimum distance value in not_in_spt_set
            spt_set[min_v.value] = True  # put min_v in spt_set
            adjacent_min_v = np.array([self.vertices[i] for i in range(len(self.matrix))
                                       if self.matrix[i][min_v.value] == 1])  # finds adjacent vertices for min_v
            for v in adjacent_min_v:  # updates adjacent distance
                if min_v.distance + self.weight < v.distance:
                    v.distance = min_v.distance + self.weight
                    v.previous = min_v
            

    def shortest_path(self, source_vertex, destination_vertex):
        self.dijkstra(source_vertex, destination_vertex)
        v = self.vertices[destination_vertex]
        path = []
        while v is not None:
            path = [v.value] + path
            v = v.previous
        return path






