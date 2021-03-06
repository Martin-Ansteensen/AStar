#!/usr/bin/env python3
import time
import copy
start_time = time.time()

horizontal = 10
vertical = 20
work_grid = [["0" for i in range(horizontal)] for j in range(vertical)] 


solution_grid = copy.deepcopy(work_grid)

start = [0, 0] #xy
end = [9, 19 ]  #xy


class Node:
    best_node = None
    lowest_cost = None

    def __init__(self, x, y, parent):
        # In comes coordinates
        self.x = x
        self.y = y
        self.parent = parent
        self.has_been_parent = False

        self.x_from_start = abs(start[0] - self.x)
        self.y_from_start = abs(start[1] - self.y)
        self.x_from_end = abs(end[0] - self.x)
        self.y_from_end = abs(end[1] - self.y)
        
        self.cost = self.x_from_end +self.y_from_end + self.x_from_start + self.y_from_start # Important to keep **2
    
    def is_valid(self):
        try:
            valid_conditions = [
                work_grid[self.y][self.x] != "-", # The cell is not an obstacle
                self.x in range(horizontal), # The cells x is within the workspace
                self.y in range(vertical), # The cells y is within the workspace
                not self.already_exists() # Returns True if it already exists, therefor not
            ]
            
            if all(valid_conditions) or self.x == end[0] and self.y == end[1]: # The cell is valid of all conditions were met or if it has reached the end
                return True
            else:
                return False
        except(TypeError, IndexError) as e: # The coordinates of the cell does not exist
            print(e)
            return False

    def already_exists(self): 
        status = False
        for node in all_nodes: # Checks all of the nodes that exist
            if node.x == self.x and node.y == self.y and node != self: # Checks if the cell has the same coordinate as an existing cell
                return True
        return status
        
    def draw(self): # GUI
        work_grid[self.y][self.x] = "i"


parent_nodes = []
all_nodes = []
current_node_xy = start
all_nodes.append(Node(start[0], start[1], None)) # Add the starting node to the list
nodes_pattern = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] # Right, left, up, down, upper right, upper left, down right, down left

counter = 0
while current_node_xy != end: # Run until the current node is the end node
    new_nodes_created = False
    # Finds the node closest to the end node
    Node.lowest_cost = all_nodes[-1].cost 
    for node in all_nodes:
        if node.cost <= Node.lowest_cost and node.has_been_parent == False:
            Node.lowest_cost = node.cost
            Node.best_node = node
            current_node_xy[0], current_node_xy[1] = node.x, node.y
            parent_nodes.append(node)
            node.has_been_parent = True
    
    # Create surrounding nodes
    for i in range(len(nodes_pattern)):
        all_nodes.append(Node(current_node_xy[0]+nodes_pattern[i][0], current_node_xy[1]+nodes_pattern[i][1], Node.best_node))
        if all_nodes[-1].is_valid() == True:
            all_nodes[-1].draw()
            new_nodes_created = True
        else:
            del all_nodes[-1]
    

    if not new_nodes_created:
        if len(all_nodes) == len(parent_nodes):
            print("No solutions available")
            break

    # # Print the grid
    for i in range(vertical):
        print(work_grid[i])
    print("\n")

    #input("Press N to continue...")


solution = []     
solution.append(Node.best_node)
# solution.append(parent_nodes[-1]) # The end node

# Backtracks
while True:
    solution.append(solution[-1].parent) # Adds the 
    if solution[-1].x_from_start == 0 and solution[-1].y_from_start == 0:
        break

for node in solution:
    solution_grid[node.y][node.x] = "i"

for x in range(vertical):
    print(work_grid[x])

print("\n")
for x in range(vertical):
    print(solution_grid[x])

print("--- %s seconds ---" % (time.time() - start_time))
