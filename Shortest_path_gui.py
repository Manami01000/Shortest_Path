import tkinter as tk
from PIL import Image, ImageTk
from time import sleep
from Game import Game
from random import randint, uniform, sample

# Your default board here, replace it with your desired board.
default_board = [
    [3, 1, 1, 1, 1,1,1,1,1],
    [1, 0, 0, 1, 0,0,0,1,1],
    [1, 1, 1, 1, 1,0,2,0,0],
    [0, 1, 0, 1, 0,0,1,0,1],
    [0, 0, 0, 1, 1,1,1,0,1],
    [0, 0, 0, 1, 1,1,1,0,1],
    [0, 0, 0, 1, 1,1,1,0,1],
    [0, 0, 0, 1, 1,1,1,0,1],
    [0, 0, 0, 1, 1,1,1,0,1],

]

class ShortestPathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Path")

        self.board = default_board
        self.board_generator()

        self.heading_label = tk.Label(root, text="Shortest Path", font=("Helvetica", 20, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=5, pady=10)

        size_grid = 500
        self.size_of_cell = int(size_grid /self.len_board)
        self.canvas = tk.Canvas(root, width=size_grid, height=size_grid)
        self.canvas.grid(row=1, column=0, columnspan=5, pady=10)

        self.images = {
            0: ImageTk.PhotoImage(Image.open("starwars theme/block.png").resize((self.size_of_cell, self.size_of_cell))),
            1: None,  # Blank cell
            2: ImageTk.PhotoImage(Image.open("starwars theme/target.png").resize((self.size_of_cell, self.size_of_cell))),
            3: ImageTk.PhotoImage(Image.open("starwars theme/source.png").resize((self.size_of_cell, self.size_of_cell))),
        }

        self.draw_grid()

        self.solve_button = tk.Button(root, text="Solve", command=self.animate_path)
        self.solve_button.grid(row=2, column=0, columnspan=5, pady=10)


    def draw_grid(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                x1, y1 = j * self.size_of_cell, i * self.size_of_cell
                x2, y2 = x1 + self.size_of_cell, y1 + self.size_of_cell
                cell_value = self.board[i][j]

                source_index = 0

                # Draw cells with white borders on all sides
                if cell_value == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")  # Add white border
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.images[cell_value])
                elif cell_value == 1:
                      self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")
                elif cell_value == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")  # Add white border
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.images[cell_value])
                elif cell_value == 3:
                    for x in range(len(self.paths)):
                        if self.paths[x][0] == (i,j):
                            source_index = x
                            break
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")  # Add white border
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.images[cell_value], tags=f"moving_image{source_index}")
                    source_index += 1


    def animate_path(self, index=1):
        for i in range(len(self.paths)):
            source_i, source_j = self.paths[i][index - 1]

            if index == 1:
                self.canvas.delete(f"moving_image{i}")
                source_x, source_y = source_j * self.size_of_cell, source_i * self.size_of_cell
                self.canvas.create_image(source_x, source_y, anchor=tk.NW, image=self.images[3], tags=f"moving_image{i}")

            if index < len(self.paths[i]):
                target_i, target_j = self.paths[i][index]

                # Remove the previous image (if any) from the source cell
                self.canvas.delete(f"moving_image{i}")

                # Draw the image in the target cell
                target_x, target_y = target_j * self.size_of_cell, target_i * self.size_of_cell
                self.canvas.create_image(target_x, target_y, anchor=tk.NW, image=self.images[3], tags=f"moving_image{i}")

        # Update the whole GUI to show the changes
        self.root.update()

        if index < len(self.paths[0]):
            # Schedule the next step after a delay (e.g., 500 milliseconds)
            self.root.after(500, self.animate_path, index + 1)





        # source_i, source_j = self.paths[index - 1]
        # if index == 1:
        #     self.canvas.delete("moving_image")

        #     source_x, source_y = source_j * self.size_of_cell, source_i * self.size_of_cell
        #     self.canvas.create_image(source_x, source_y, anchor=tk.NW, image=self.images[3], tags="moving_image")

        #     # Update the whole GUI to show the changes
        #     self.root.update()

        #     sleep(0.5)

        # if index < len(self.paths):
        #     target_i, target_j = self.paths[index]

        #     # Remove the previous image (if any) from the source cell
        #     self.canvas.delete("moving_image")

        #     # Draw the image in the target cell
        #     target_x, target_y = target_j * self.size_of_cell, target_i * self.size_of_cell
        #     self.canvas.create_image(target_x, target_y, anchor=tk.NW, image=self.images[3], tags="moving_image")

        #     # Update the whole GUI to show the changes
        #     self.root.update()

        #     # Schedule the next step after a delay (e.g., 500 milliseconds)
        #     self.root.after(500, self.animate_path, index + 1)

    def board_generator(self):
        self.paths = []
        solvable = False
        print("Generating Board...")
        while not solvable:
            self.len_board = randint(10,50)
            # sum_of_targets_sources = (self.len_board // 4) * 3 makes it run slow
            sum_of_targets_sources = randint(1,7)
            amount_cells = self.len_board**2
            amount_blocks = int(uniform(0.2,0.6) * amount_cells)
            places_in_board = [(i//self.len_board,i%self.len_board) for i in range(amount_cells)] # converts single number to coordinates
            object_location = sample(places_in_board, amount_blocks + sum_of_targets_sources * 2)
            self.board = [[1 for j in range(self.len_board)] for i in range(self.len_board)]
            i = 0
            for x, y in object_location:
                i+=1
                if i <= sum_of_targets_sources:
                    self.board[x][y] = 3
                elif i > sum_of_targets_sources and i<=sum_of_targets_sources*2:
                    self.board[x][y] = 2
                else:
                    self.board[x][y] = 0
            self.game = Game(self.board)
            self.paths = self.game.solve()

            solvable = True
            print('Tried')

            for path in self.paths:
                if len(path) == 1:
                    solvable = False
                    # continue
            
        longest_path = max(self.paths, key = lambda p: len(p))
        for path in self.paths:
            for i in range(len(longest_path) - len(path)):
                path += [path[-1]]
        print("Success!")

            
            



if __name__ == "__main__":
    root = tk.Tk()
    shortest_path_gui = ShortestPathGUI(root)
    root.mainloop()