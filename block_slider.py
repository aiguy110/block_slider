import numpy as np
import itertools

BLOCKS = 11
init_grid = np.array([[2, 1, 1, 3],
                      [2, 1, 1, 3],
                      [4, 5, 5, 6],
                      [4, 7, 8, 11],
                      [9, 0, 0, 10]], dtype=np.int32)
equivalencies = [(2, 3, 4), (9, 6, 7, 8, 10, 11)]
win = lambda g: g[4, 1]==1 and g[4, 2]==1


# BLOCKS = 10
# init_grid = np.array([[2, 1, 1, 3],
#                       [2, 1, 1, 3],
#                       [4, 5, 5, 6],
#                       [4, 7, 8, 6],
#                       [9, 0, 0, 10]], dtype=np.int32)
# equivalencies = [(2, 3, 4, 6), (9, 7, 8, 10)]
# win = lambda g: g[4, 1]==1 and g[4, 2]==1

# BLOCKS = 3
# init_grid = np.array([[1, 2],
#                       [1, 0],
#                       [3, 0]], dtype=np.int32)
# equivalencies = [(2, 3)]
# win = lambda g: g[2, 1]==1

# BLOCKS = 2
# init_grid = np.array([[1, 0],
#                       [0, 2]], dtype=np.int32)
# equivalencies = []
# win = lambda g: g[1, 1]==1

ROWS= len(init_grid)
COLS= len(init_grid[0])

RIGHT=0
DOWN=1
LEFT=2
UP=3

def move(grid, block, direction):
    global ROWS, COLS
    
    # Can we move this block that way?
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i, j] != block:
                continue
            
            di, dj = [(0, 1), (1, 0), (0, -1), (-1, 0)][direction]
            if i+di >= ROWS or j+dj >= COLS or i+di < 0 or j+dj < 0:
                return None
            if grid[i+di, j+dj] != block and grid[i+di, j+dj] != 0:
                return None
    
    # If we're here we can. Do it
    new_grid = np.zeros((ROWS, COLS), dtype=np.int32)
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i, j] == block:
                di, dj = [(0, 1), (1, 0), (0, -1), (-1, 0)][direction]
                new_grid[i+di, j+dj] = block
            elif grid[i, j] != 0: # Don't let zero overwrite things
                new_grid[i, j] = grid[i, j]
    return new_grid

def equiv_grids(grid):
    global equivalencies, ROWS, COLS, BLOCKS
    grids = []
    for equivilance in itertools.product(*[list(itertools.permutations(eq)) for eq in equivalencies]):
        block_map = {0: 0}
        for block in range(1, BLOCKS+1):
            for e, eq in enumerate(equivalencies):
                if block in eq:
                    block_map[block] = equivalencies[e][equivilance[e].index(block)]
                    break
            else:
                block_map[block] = block
        
        new_grid = np.zeros((ROWS, COLS), dtype=np.int32)
        for i in range(ROWS):
            for j in range(COLS):
                new_grid[i, j] = block_map[ grid[i, j] ]
        grids.append(new_grid)
    
    if len(grids) == 0:
        return [grid]
    else:
        return grids

def solve(init_grid):
    global BLOCKS
    checked_grid_hashes = {}
    current_depth = 0
    
    edge_solutions = [([], init_grid)] # A solution matches (move_hist, resulting_grid)

    while True:
        best_partial_solution_ind = 0
        best_partial_solution_cost = None
        for i in range(len(edge_solutions)):
            partial_solution = edge_solutions[best_partial_solution_ind]
            if best_partial_solution_cost == None or len(partial_solution[0]) < best_partial_solution_cost:
                best_partial_solution_ind = i
                best_partial_solution_cost = len(partial_solution[0])
        if best_partial_solution_cost > current_depth:
            current_depth = best_partial_solution_cost
            print('Current depth:', current_depth, ', Edge nodes:', len(edge_solutions), ', Hash table length:', len(checked_grid_hashes))

        move_hist, grid = edge_solutions[best_partial_solution_ind]
        next_partial_solutions = []
        for block in range(1, BLOCKS+1):
            for direction in range(4):
                new_grid = move(grid, block, direction)
                
                if new_grid is None: # Can't move that way
                    continue
                if hash(str(new_grid)) in checked_grid_hashes: # Already checked
                    continue
                
                # Is this a win?
                if win(new_grid):
                    return move_hist + [(block, direction)]
                
                # Add next moves to list of moves to consider
                for equiv_grid in equiv_grids(new_grid):
                    checked_grid_hashes[ hash(str(equiv_grid)) ] = True
                next_partial_solutions.append( (move_hist + [(block, direction)], new_grid) )
            
        # We apparently didn't find a win. Update edge_solutions
        del edge_solutions[best_partial_solution_ind]
        edge_solutions.extend( next_partial_solutions )




        

    # We can't win from here :(
    return None


# print('equiv_grids')
# for grid in equiv_grids(init_grid):
#     print(grid) 

result = solve(init_grid)
print()
print('MOVES:', len(result))
print(init_grid)
for move in result:
    dir_str = ['RIGHT', 'DOWN', 'LEFT', 'UP'][move[1]]
    print(f'Move block {move[0]} {dir_str}')