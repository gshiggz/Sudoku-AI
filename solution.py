assignments = []

#Setting up the board
def cross(a, b):
    return [s+t for s in a for t in b]
rows = 'ABCDEFGHI'
cols = '123456789'
cols_back = cols[::-1]
boxes = cross(rows, cols)

#Setting up the row, column, box and diagonal units
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
box_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(len(rows))]]
diag2_units = [[rows[i]+cols_back[i] for i in range(len(rows))]]

unitlist = row_units + col_units + box_units + diag_units + diag2_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    #assigning possible naked twins to each box value
    possible_twins = [box for box in values.keys() if len(values[box]) == 2]
    naked_twins = [[box1,box2] for box1 in possible_twins for box2 in peers[box1] if set(values[box1])==set(values[box2])]

    for i, x in enumerate(naked_twins):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_intersect = peers1.intersection(peers2)

        #check for naked twins and eliminate
        for peer_value in peers_intersect:
            if len(values[peer_value]) >= 2:
                for remaining_value in values[box1]:
                   values = assign_value(values, peer_value, values[peer_value].replace(remaining_value,''))
    return values
    

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

#def cross(A, B):
#    "Cross product of elements in A and elements in B."
#    pass

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    #converting grid into dictionary
    alpha = []
    digits = '123456789'
    for a in grid:
        if a in digits:
            alpha.append(a)
        if a =='.':
            alpha.append(digits)
    assert len(alpha) == 81
    return dict(zip(boxes, alpha))
                

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    #generating the grid for pygame
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    #eliminate the duplicates of given values in relative units
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    #eliminate the box values that can only be a single value given their units
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    #cycle through eliminate and only_choice again until stalled
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_after == solved_values_before
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

    
def search(values):
    #eliminate values from previous functions and pick unfinished boxes with lowest possible matches
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #Solve function given previous function
    
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
