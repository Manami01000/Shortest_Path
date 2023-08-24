from Graph import Graph


if __name__ == "__main__":
    matrix = [[0, 0, 1, 0, 1, 0],
              [0, 0, 1, 1, 0, 0],
              [1, 1, 0, 0, 1, 0],
              [0, 1, 0, 0, 1, 1],
              [1, 0, 1, 1, 0, 0],
              [0, 0, 0, 1, 0, 0]]
    graph = Graph(matrix)
    print(graph.shortest_path(0,5))
