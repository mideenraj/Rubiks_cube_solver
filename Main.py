from RubiksBot import RubiksBot
from RubiksSolver import RubiksSolver
import kociemba
from time import sleep

def for_nontesting_runs(solver):
    """Call for non testing runs."""
    state = {}
    letter_to_color_conv = {'g': 'Green', 'b': 'Blue', 'o': 'Orange', 'r': 'Red', 'w': 'White', 'y': 'Yellow'}
    for side in ['FACE', 'BACK', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM']:
        side_input = input(f"Please enter state for {side}: ")    # Input will be a string of length 9, each letter representing first letter of color
        side_input = [i for i in side_input]  # Convert string to a list

        # Replace each letter in list with its respective color
        for i in range(len(side_input)):
            side_input[i] = letter_to_color_conv[side_input[i]]
        
        # Store side input to dict
        state[side] = side_input
    
    solver.cube_state = state   # Set state
    
    
    
    
    
    
    
    

def main():
    """Main driver function for Rubiks cube program."""

    bot = RubiksBot()
    solver = RubiksSolver(None)

    # 1. ----------------- Set start cube state
    testing = False
    if testing:
        solver.cube_state = solver.test_cube_states[0]

    else:
        for_nontesting_runs(solver)


    # 2. ----------------- Get cube solution
    kociemba_input = solver.encode_before_kociemba()          # Prepare input for kociemba using current cube state
    kociemba_output = kociemba.solve(kociemba_input)        # Access the solution string
    decoded_solution = solver.decode_after_kociemba(kociemba_output)  # Decode the solution into a list of moves. Ex: [[side, direction], [...], ...]
    
    # For Testing
    debug1 = False
    if debug1:
        print("Moves count: ", len(decoded_solution))
        for side, direction in decoded_solution:
            print(side, direction)


    # 3. ----------------- Execute moves through bot
    startprints = False
    if startprints:
        print("Bot State: ", bot.bot_state)
        print("Starting cube state: ")
        solver.print_cube_state()
    
    debug2 = False
    for side, direction in decoded_solution:
        
        if debug2:  # Setup for debugging
            print("Move stats : ", side, direction)
            input("Continue...")
            
        bot.load_side(side)   # Load side to rotate
        
        # Update cube state in script
        solver.current_side_being_moved = side
        solver.current_direction_of_rotation = direction
        solver.make_move() # Make virtual move (Also updates cube state)

        
        # Testing...
        new_angle = bot.curr_angle + bot.cw_angle if direction=='cw' else bot.curr_angle + bot.ccw_angle
        if new_angle > 270:
            new_angle = 0
        elif new_angle < 0:
            new_angle = 270
        #input(f"Direction of rotation: {direction}. Moving: {bot.curr_angle} -> {new_angle}")
        # Testing end...
            
        bot.turn_cube(direction)    # Rotate cube
        
        if debug2:  # Setup for debugging
            print("Post Bot State: ", bot.bot_state)
            print("Post Cube State: ")
            print(solver.print_cube_state())
            input("Press to continue\n")
        
        

    print("Cube solved: ", solver.is_solved())



main()


