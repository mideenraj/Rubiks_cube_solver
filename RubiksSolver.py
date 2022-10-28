from time import sleep
import kociemba
import copy
import random

# Description: This script manages the RubiksSolver class, which holds the virtual representation of the Rubiks cube and
#              also methods for accessing solution to any cube orientation using the kociemba algorithm.

class RubiksSolver:
    """xxx"""

    def __init__(self, gui) -> None:
        """Constructor method for class."""

        # Store RubiksGUI class instance
        self.gui = gui      # This is only to be used when this class is initialized and called by the RubiksGUI class, othewise initialize with a placeholder (Ex. 1)

        # Tracker variables for tracking the current move being made
        self.current_side_being_moved = None
        self.current_direction_of_rotation = None

        # Store move specifications and metrics for assist with moves: Used for updating neighboring square when making a move from ANY side. When staring 
        #   at the side being moved, the first list aligns with the row that lies on top, the second with the column that lies to the right, the third with 
        #   the row that lies directly at below and the fourth with the column that lies to the left. So you always start at the neighboring side that is 
        #   directly above the moving side and work around in a clockwise fashion until all 4 neighboring sides are covered
        self.move_directory = {
            "FACE_cw": {"side_shift_values": [2, 4, 6, -2, 0, 2, -6, -4, -2], "neighbors": ['TOP', 'RIGHT', 'BOTTOM', 'LEFT'], 
                'neighbor_shift_values': [[-6, -4, -2], [2, -2, -6], [6, 4, 2], [-2, 2, 6]], 'base_indices': [[6, 7, 8], [0, 3, 6], [2, 1, 0], [8, 5, 2]]},

            "FACE_ccw": {"side_shift_values": [6, 2, -2, 4, 0, -4, 2, -2, -6], "neighbors": ['TOP', 'LEFT', 'BOTTOM', 'RIGHT'], 
                'neighbor_shift_values': [[-6, -2, 2], [-2, -4, -6], [6, 2, -2], [2, 4, 6]], 'base_indices': [[8, 7, 6], [2, 5, 8], [0, 1, 2], [6, 3, 0]]},

            "BACK_cw": {"side_shift_values": [2, 4, 6, -2, 0, 2, -6, -4, -2], "neighbors": ['TOP', 'LEFT', 'BOTTOM', 'RIGHT'], 
                'neighbor_shift_values': [[-2, 2, 6], [6, 4, 2], [2, -2, -6], [-6, -4, -2]], 'base_indices': [[2, 1, 0], [0, 3, 6], [6, 7, 8], [8, 5, 2]]},

            "BACK_ccw": {"side_shift_values": [6, 2, -2, 4, 0, -4, 2, -2, -6], "neighbors": ['TOP', 'RIGHT', 'BOTTOM', 'LEFT'], 
                'neighbor_shift_values': [[2, 4, 6], [6, 2, -2], [-2, -4, -6], [-6, -2, 2]], 'base_indices': [[0, 1, 2], [2, 5, 8], [8, 7, 6], [6, 3, 0]]},

            "LEFT_cw": {"side_shift_values": [2, 4, 6, -2, 0, 2, -6, -4, -2], "neighbors": ['TOP', 'FACE', 'BOTTOM', 'BACK'], 
                'neighbor_shift_values': [[0, 0, 0], [0, 0, 0], [8, 2, -4], [-8, -2, 4]], 'base_indices': [[0, 3, 6], [0, 3, 6], [0, 3, 6], [8, 5, 2]]},

            "LEFT_ccw": {"side_shift_values": [6, 2, -2, 4, 0, -4, 2, -2, -6], "neighbors": ['TOP', 'BACK', 'BOTTOM', 'FACE'], 
                'neighbor_shift_values': [[-4, 2, 8], [4, -2, -8], [0, 0, 0], [0, 0, 0]], 'base_indices': [[6, 3, 0], [2, 5, 8], [6, 3, 0], [6, 3, 0]]},

            "RIGHT_cw": {"side_shift_values": [2, 4, 6, -2, 0, 2, -6, -4, -2], "neighbors": ['TOP', 'BACK', 'BOTTOM', 'FACE'], 
                'neighbor_shift_values': [[-8, -2, 4], [8, 2, -4], [0, 0, 0], [0, 0, 0]], 'base_indices': [[8, 5, 2], [0, 3, 6], [8, 5, 2], [8, 5, 2]]},

            "RIGHT_ccw": {"side_shift_values": [6, 2, -2, 4, 0, -4, 2, -2, -6], "neighbors": ['TOP', 'FACE', 'BOTTOM', 'BACK'], 
                'neighbor_shift_values': [[0, 0, 0], [0, 0, 0], [4, -2, -8], [-4, 2, 8]], 'base_indices': [[2, 5, 8], [2, 5, 8], [2, 5, 8], [6, 3, 0]]},

            "TOP_cw": {"side_shift_values": [2, 4, 6, -2, 0, 2, -6, -4, -2], "neighbors": ['BACK', 'RIGHT', 'FACE', 'LEFT'], 
                'neighbor_shift_values': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 'base_indices': [[2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0]]},

            "TOP_ccw": {"side_shift_values": [6, 2, -2, 4, 0, -4, 2, -2, -6], "neighbors": ['BACK', 'LEFT', 'FACE', 'RIGHT'], 
                'neighbor_shift_values': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 'base_indices': [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]]},

            "BOTTOM_cw": {"side_shift_values": [2, 4, 6, -2, 0, 2, -6, -4, -2], "neighbors": ['FACE', 'RIGHT', 'BACK', 'LEFT'], 
                'neighbor_shift_values': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 'base_indices': [[6, 7, 8], [6, 7, 8], [6, 7, 8], [6, 7, 8]]},

            "BOTTOM_ccw": {"side_shift_values": [6, 2, -2, 4, 0, -4, 2, -2, -6], "neighbors": ['FACE', 'LEFT', 'BACK', 'RIGHT'], 
                'neighbor_shift_values': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 'base_indices': [[8, 7, 6], [8, 7, 6], [8, 7, 6], [8, 7, 6]]},
        }


        # How the state of the cube will be represented: A dictionary with each side as a property with its values being an array of 9 elements (colors)

        self.cube_state = {         # Original uninitialized state:
            "FACE": ["Green" for _ in range(9)],
            "BACK": ["Blue" for _ in range(9)],
            "LEFT": ["Orange" for _ in range(9)],
            "RIGHT": ["Red" for _ in range(9)],
            "TOP": ["White" for _ in range(9)],
            "BOTTOM": ["Yellow" for _ in range(9)]
        }



        # States used for testing
        self.test_cube_states = [
            # Scenario 1: YT Video example (Solution 16: F B' U' R' U2 D B U D F2 B2 U' D' R2 L2 F2) - PASSED
            { "FACE": ["White", "Red", "Red", "Orange", "Green", "Orange", "Green", "Blue", "Orange"],
                "BACK": ["White", "White", "Orange", "Red", "Blue", "Orange", "Red", "Blue", "Yellow"],
                "LEFT": ["White", "Green", "Green", "White", "Orange", "Blue", "Orange", "Green", "Yellow"],
                "RIGHT": ["White", "Green", "Blue", "Yellow", "Red", "Yellow", "Yellow", "White", "Yellow"],
                "TOP": ["Blue", "Red", "Red", "Orange", "White", "Yellow", "Orange", "Green", "Green"],
                "BOTTOM": ["Red", "Red", "Blue", "White", "Yellow", "Blue", "Green", "Yellow", "Blue"]
            },

            # Scenario 2: Custom (Solution 17 R F B U' D' R L' U2 B2 L2 B2 D L2 D' R2 B2 R2) - PASSED
            { "FACE": ["Orange", "Yellow", "White", "Red", "Green", "White", "Red", "White", "Yellow"],
                "BACK": ["White", "White", "Orange", "Yellow", "Blue", "Orange", "White", "Yellow", "Green"],
                "LEFT": ["Blue", "Blue", "Green", "Blue", "Orange", "Green", "Red", "Orange", "Blue"],
                "RIGHT": ["Blue", "Green", "Red", "Green", "Red", "Green", "Red", "Blue", "Orange"],
                "TOP": ["Yellow", "Blue", "Green", "Yellow", "White", "Orange", "Yellow", "Orange", "Orange"],
                "BOTTOM": ["White", "Red", "Blue", "White", "Yellow", "Red", "Yellow", "Red", "Green"]
            },
            # Scenario 3: Custom (Solution ) - CUSTOM INPUT TESTING
           { "FACE": ["Blue", "Green", "White", "Blue", "Green", "Green", "Yellow", "Green", "Yellow"],
                "BACK": ["Orange", "White", "Blue", "Yellow", "Blue", "White", "Orange", "Blue", "Green"],
                "LEFT": ["Orange", "Orange", "Red", "Red", "Orange", "Yellow", "Yellow", "Orange", "Red"],
                "RIGHT": ["Green", "Red", "Yellow", "Red", "Red", "Red", "Red", "Yellow", "Green"],
                "TOP": ["White", "Green", "Blue", "White", "White", "Blue", "White", "Orange", "Red"],
                "BOTTOM": ["Green", "Yellow", "Blue", "Blue", "Yellow", "Orange", "Orange", "White", "White"]
            }
        ]

        self.cube_state = self.cube_state

       

    def start(self):
        """Main function. 

        *This function is to be called only by this class when 
        running this script individually,without the GUI."""


        self.randomize()    # Scramble cube

        kociemba_input = self.encode_before_kociemba()          # Prepare input for kociemba using current cube state

        kociemba_output = kociemba.solve(kociemba_input)        # Access the solution string
        print(kociemba_output)

        decoded_solution = self.decode_after_kociemba(kociemba_output)  # Decode the solution into a list of moves
        for s, d in decoded_solution:
            print(s, d)

        self.execute_solution(decoded_solution)     # Execute the moves

        print("Solved: ", self.is_solved())
        self.print_cube_state()

    def encode_before_kociemba(self):
        """xxx"""

        color_to_code_conversion = {
            'Green'  : 'F',
            'White'  : 'U',
            'Blue'   : 'B',
            'Red'    : 'R',
            'Orange' : 'L',
            'Yellow' : 'D'
        }

        # Kociemba takes a 54 length string represents the color codes of each sides in the following order: UP, RIGHT, FACE, BOTTOM, LEFT, BACK
        state_str = ''
        sides = ["TOP", "RIGHT", "FACE", "BOTTOM", "LEFT", "BACK"]  # Original
        # sides = ["RIGHT", "FACE", "BOTTOM", "LEFT", "BACK", "TOP"]      # Testing
        for i in range(6):
            for square in self.cube_state[sides[i]]:
                state_str += color_to_code_conversion[square]

        return state_str

    def decode_after_kociemba(self, kociemba_solution):
        """xxx"""

        code_to_side_conversion = {
            'F'  : 'FACE',
            'L'  : 'LEFT',
            'R'  : 'RIGHT',
            'U'  : 'TOP',
            'D' : 'BOTTOM',
            'B' : 'BACK'
        }

        # Break string into list of steps
        k_solution = kociemba_solution.split(" ")

        # Decode solution into a nested list. Ex: [[side, direction], [...], ...]
        moves = []
        for i in k_solution:
            if len(i) == 1:     # Ex: R
                move = [code_to_side_conversion[i], "cw"]
                moves.append(move) 
            elif len(i) == 2 and "'" in i:  # Ex: R'
                move = [code_to_side_conversion[i[0]], "ccw"]
                moves.append(move)
            elif len(i) == 2 and "2" in i:  # Ex: R2
                move = [code_to_side_conversion[i[0]], "cw"]
                moves.append(move)
                moves.append(move)
            elif len(i) == 3 and "2'" in i:  # Ex: R2'
                move = [code_to_side_conversion[i[0]], "ccw"]
                moves.append(move)
                moves.append(move)
        
        # Return decoded solution
        return moves
  
    def execute_solution(self, solution):
        """Executes the passed list of solutions, one by one.

        *This function is to be called only by this class when 
        running this script individually,without the GUI."""

        count = 1
        for move in solution:
            self.current_side_being_moved = move[0]
            self.current_direction_of_rotation = move[1]
            self.make_move()

            count+=1

    def make_move(self) -> None:
        """Executes the requested move by updating self.cube_state."""

        # Update class cube (aka the ones stored as a dictionary)
        self.update_cube_state()

    def update_cube_state(self):
        """xxx"""

        # 1. Make copy of existing state of the side being rotated (This will not be altered and will be for reference while actual list is being modified)
        #prev_state = self.cube_state[self.current_side_being_moved].copy()
        prev_state = copy.deepcopy(self.cube_state[self.current_side_being_moved])  # Deepcopy

        # 2. Update side of cube that is being turned.
        this_sides_move_directory = self.move_directory[self.current_side_being_moved + "_" + self.current_direction_of_rotation]
        for i in range(9):
            color = prev_state[i]
            new_index = i + this_sides_move_directory['side_shift_values'][i]
            self.cube_state[self.current_side_being_moved][new_index] = color
        
        # 3. Update the 3 of the 4 neigboring sides
        # prev_neighbor_state = self.cube_state[this_sides_move_directory['neighbors'][3]].copy()     # Store state of neighbor that is directly above the side being moved
        prev_neighbor_state = copy.deepcopy(self.cube_state[this_sides_move_directory['neighbors'][3]])   # Deepcopy

        for i in range(4):

            # 1. Initialize variables
            neighbors = this_sides_move_directory['neighbors']
            this_neighbors_label = neighbors[i]   # Get name of this neighor
            base_indices = this_sides_move_directory['base_indices'][i-1]
            neighbor_shift_values = this_sides_move_directory['neighbor_shift_values'][i-1]

            # 2. Access and store neccessary data from prev_neighbor_state variable
            colors = [prev_neighbor_state[base_indices[i]] for i in range(3)]  # Get colors of prev neighbor

            # 3. Update prev_neighbor_state to represent current neighbor state
            prev_neighbor_state = copy.deepcopy(self.cube_state[this_neighbors_label])  # Deepcopy

            # 4. Calculate new indices to write onto and then update color values at that index
            for e in range(3):
                new_idx = base_indices[e] + neighbor_shift_values[e]
                self.cube_state[this_neighbors_label][new_idx] = colors[e]  
        
    def randomize(self, count=5):
        """xxx"""
        faces = ['FACE', 'BACK', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM']
        rotations = ['cw', 'ccw']

        # Make the specified # of moves
        for i in range(count):
            # Choose random side and direction
            self.current_side_being_moved = random.choice(faces)
            self.current_direction_of_rotation = random.choice(rotations)

            # Make move
            self.make_move()
        
    def is_solved(self):
        """Checks if the rubik's cube has been solved or not. Return True is solved, else False."""

        for side in self.cube_state:
            curr_side = self.cube_state[side]
            if curr_side.count(curr_side[0]) != len(curr_side):
                return False
        return True

    def print_cube_state(self):
        """xxx"""

        state_cpy = copy.deepcopy(self.cube_state)
        for side in state_cpy:
            for i in range(9):
                if len(state_cpy[side][i]) < 6:
                    temp = state_cpy[side][i]
                    for _ in range(6-len(state_cpy[side][i])):
                        temp += " "
                    state_cpy[side][i] = temp
        
        for side in state_cpy:   
            print(f"{side}{' '*(6-len(side))}: {state_cpy[side]}")



if __name__ =='__main__':
    solver = RubiksSolver(None)
    solver.cube_state = solver.test_cube_states[2]
    solver.start()
