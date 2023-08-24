from Graph import Graph
import networkx as nx
from itertools import product



class Game:
    # Rules of game 0 = blocked, 1 = open, 2 = target, 3 = soldier starting point
    def __init__(self, board):
        self.board = board

    def parser(self):
        matrix = [[0 for i in range(len(self.board) ** 2)]for i in range(len(self.board) ** 2)] # adjacent matrix
        n = len(self.board)
        for i in range(len(matrix)):
            if i%n != 0 and self.board[(i-1) // n][(i-1) % n] != 0: #checks if there is adjacent cell left
                matrix[i][i-1] = 1 
            if i%n != n -1 and self.board[(i+1) // n][(i+1) % n] != 0: #checks if there is adjacent cell right
                matrix[i][i+1] = 1
            if i - n >= 0 and self.board[(i-n) // n][(i-n) % n] != 0: #checks if there is adjacent cell up
                matrix[i][i-n] = 1
            if i + n < len(matrix) and self.board[(i+n) // n][(i+n) % n] != 0: #checks if there is adjacent cell down
                matrix[i][i+n] = 1
        
        return matrix
    
    def solve(self):
        graph = Graph(self.parser())
        destination_vertices = []
        source_vertices = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 2:
                    destination_vertices.append(i * len(self.board) + j)
                if self.board[i][j] == 3:
                    source_vertices.append(i * len(self.board) + j)

        if len(source_vertices) > len(destination_vertices):
            num_of_outs = len(source_vertices) - len(destination_vertices)
            out_vertices = [len(self.board) ** len(self.board) for i in num_of_outs]
            destination_vertices += out_vertices
        


        # Create a weighted bipartite graph
        G = nx.Graph()

        # Add nodes from the left partition(sources)
        G.add_nodes_from(source_vertices, bipartite=0)

        # Add nodes from the right partition(destinations)
        G.add_nodes_from(destination_vertices, bipartite=1)

        all_paths = {(i, j): graph.shortest_path(i, j) for i in source_vertices for j in destination_vertices}
        for key in all_paths:
            path = all_paths[key]
            tuple_path = [(x//len(self.board), x% len(self.board))for x in path]
            all_paths[key] = tuple_path

        # Add weighted edges
        edges = [(i, j, len(all_paths[(i,j)])) for i, j in product(source_vertices, destination_vertices)]
        G.add_weighted_edges_from(edges)

        # Find a minimum weight perfect matching
        matching = nx.bipartite.minimum_weight_full_matching(G)

        paths = [all_paths[(i,j)] for i, j in matching.items() if i in source_vertices]
        
        # longest_path = max(paths, key = lambda p: len(p))
        # for path in paths:
        #     for i in range(len(longest_path) - len(path)):
        #         path += [path[-1]]


        return paths


if __name__ == "__main__":
    board = [
        [1, 3, 3],
        [1, 1, 1],
        [2, 1, 2]
    ]

    game = Game(board)
    print(game.solve())