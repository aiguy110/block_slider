import numpy as np

BLOCKS = 10
init_grid = np.array([[2, 1, 1, 3],
                      [2, 1, 1, 3],
                      [4, 5, 5, 6],
                      [4, 7, 8, 6],
                      [9, 0, 0, 10]], dtype=np.int32)

ROWS= len(init_grid)
COLS= len(init_grid[0])
win = lambda g: g[4, 1]==1 and g[4, 2]==1 

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

def solve(grid, past_grid_hashes={}):
    global BLOCKS
    past_grid_hashes[ hash(str(grid)) ] = True
    
    # Can we win from any of the possible moves?
    for block in range(1, BLOCKS+1):
        for direction in range(4):
            new_grid = move(grid, block, direction)
            
            # If we can't move that way or we've been there before, don't try it
            if new_grid is None:
                continue
            if hash(str(new_grid)) in past_grid_hashes:
                continue
            
            # Did we win?
            if win(new_grid):
                # Tell the selves who remember where we've been of our glorious victory!
                return [new_grid]
            
            # This move hasn't made us win, but it still could. Past it up the chain
            solution = solve(new_grid, past_grid_hashes)
            if solution is not None: 
                # Someone up the chain figured it out :D
                # Add our contribution before passing it down
                return [new_grid] + solution
     
    # We can't win from here :(
    return None

result = solve(init_grid)
print('MOVES:', len(result))
for grid in result:
    print(grid)
    print('    |')
    print('    V')