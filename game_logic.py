from map_loader import MapLoader
import copy # For deep copying game state or parts of the map

# Cell type identifiers (can be expanded or made into an Enum)
CELL_EMPTY = 0
CELL_BLACK_HOLE = 1
CELL_GIANT_STAR = 2
CELL_WORMHOLE_ENTRANCE = 3
# CELL_WORMHOLE_EXIT (not strictly needed as a separate type on map, logic handles it)
CELL_RECHARGE_ZONE = 4
CELL_MIN_CHARGE_REQUIRED = 5
# Origin and Destination are properties of the map, not cell types themselves

class GameLogic:
    def __init__(self, map_loader_instance):
        self.map_loader = map_loader_instance
        if not self.map_loader or not self.map_loader.data:
            raise ValueError("Valid MapLoader instance with loaded data is required.")

        self.rows, self.cols = self.map_loader.get_dimensions()
        self.start_pos = self.map_loader.get_start_location()
        self.end_pos = self.map_loader.get_end_location()
        self.initial_energy = self.map_loader.get_initial_charge()
        self.energy_costs = self.map_loader.get_energy_costs()

        # Convert special cell locations to sets for efficient lookup
        self.black_holes = set(self.map_loader.get_black_holes())
        self.giant_stars = set(self.map_loader.get_giant_stars())
        
        self.wormholes_map = {
        tuple(wh['entrada']): (tuple(wh['salida']), wh['costo'])
        for wh in self.map_loader.get_wormholes()
    }
        
        self.recharge_zones = {tuple(rz[:2]): rz[2] for rz in self.map_loader.get_recharge_zones()}
        
        self.min_charge_cells = {tuple(cell['coordenada']): cell['cargaMinima'] for cell in self.map_loader.get_required_charge_cells()}

        self.solution_path = []
        self.solution_energy_levels = []

    def _is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def _get_cell_energy_cost(self, r, c):
        if self._is_valid(r,c):
            return self.energy_costs[r][c]
        return float('inf') # Should not happen if _is_valid is checked first

    def solve(self):
        """
        Iterative Depth-First Search (DFS) to find a path from start to end.
        Manages its own stack to avoid Python's recursion limits.
        """
        self.solution_path = []
        self.solution_energy_levels = []

        initial_r, initial_c = self.start_pos
        
        # Stack stores states: (r, c, energy_at_arrival_at_rc, path_list, visited_set, 
        #                       consumed_wormholes_set, temp_removed_bh_set, energy_log_list)
        stack = [(
            initial_r, initial_c, 
            self.initial_energy,
            [],                   
            set(),                
            set(),                
            set(),                
            []                    
        )]

        while stack:
            (r, c, energy_at_arrival, current_path_list, visited_on_this_path,
             consumed_wormholes_on_this_path, temp_removed_bh_on_this_path, 
             current_energy_log_list) = stack.pop()

            current_pos = (r, c)

            # --- 1. Initial validation and cost deduction for entering current_pos ---
            if not self._is_valid(r, c):
                continue

            # Check minimum charge requirement (uses energy_at_arrival)
            if current_pos in self.min_charge_cells and energy_at_arrival < self.min_charge_cells[current_pos]:
                continue

            # Cycle detection for this specific path exploration
            if current_pos in visited_on_this_path:
                continue
            
            # --- MODIFIED BLACK HOLE CHECK TO PRIORITIZE UNCONSUMED WORMHOLES ---
            # Check if current_pos is an entry to an unconsumed wormhole for this path
            is_unconsumed_wormhole_entry = current_pos in self.wormholes_map and \
                                           current_pos not in consumed_wormholes_on_this_path

            if not is_unconsumed_wormhole_entry:
                # Not an unconsumed wormhole, so standard Black Hole check applies.
                # `temp_removed_bh_on_this_path` are BHs removed by stars *before* current_pos.
                if current_pos in self.black_holes and current_pos not in temp_removed_bh_on_this_path:
                    # print(f"DEBUG Iter: Hit active BH {current_pos} (not a wormhole or wormhole consumed). Temp removed: {temp_removed_bh_on_this_path}")
                    continue # It's an active black hole
            # If it IS an unconsumed_wormhole_entry, we bypass the BH check here.
            # The wormhole logic in Stage 3 will then take over.
            # else:
            #     print(f"DEBUG Iter: Cell {current_pos} is an unconsumed wormhole. Skipping BH check here.")
            # --- END OF MODIFIED BLACK HOLE CHECK ---

            cost_to_enter_current_cell = self._get_cell_energy_cost(r, c)
            energy_after_standard_entry_cost = energy_at_arrival - cost_to_enter_current_cell
            
            if current_pos not in self.recharge_zones and energy_after_standard_entry_cost < 0:
                continue

            # --- 2. Current cell is valid. Update path state for this branch. ---
            new_path = list(current_path_list)
            new_path.append(current_pos)
            
            new_visited = set(visited_on_this_path)
            new_visited.add(current_pos)
            
            new_energy_log = list(current_energy_log_list)

            energy_for_next_moves = energy_after_standard_entry_cost
            if current_pos in self.recharge_zones:
                energy_for_next_moves = energy_at_arrival * self.recharge_zones[current_pos]
            
            new_energy_log.append(energy_for_next_moves)

            # --- 3. Handle Wormholes (mandatory if landed upon and not consumed in this path) ---
            # Make copies of mutable sets for this specific path branch if modified by wormhole/star
            # These are the states *after* processing current_pos's entry but *before* its special features like wormholes or stars.
            branch_consumed_wormholes = set(consumed_wormholes_on_this_path)
            branch_temp_removed_bh = set(temp_removed_bh_on_this_path)

            if current_pos in self.wormholes_map and current_pos not in branch_consumed_wormholes: # Re-check using branch_consumed_wormholes
                exit_pos_tuple, costo_gusano = self.wormholes_map[current_pos]
                energy_after_wormhole_cost = energy_for_next_moves - costo_gusano

                if energy_after_wormhole_cost < 0:
                    continue 

                branch_consumed_wormholes.add(current_pos) 
                
                stack.append((
                    exit_pos_tuple[0], exit_pos_tuple[1],
                    energy_after_wormhole_cost, 
                    new_path,                   
                    new_visited,                
                    branch_consumed_wormholes, 
                    branch_temp_removed_bh,    
                    new_energy_log              
                ))
                continue 

            # --- 4. Destination Check ---
            if current_pos == self.end_pos:
                self.solution_path = new_path
                self.solution_energy_levels = new_energy_log
                # print(f"Iterative Solution Found: {self.solution_path}") # Optional debug
                # print(f"Iterative Energy Levels: {self.solution_energy_levels}") # Optional debug
                return self.solution_path, self.solution_energy_levels

            # --- 5. Explore Moves (Giant Star or Standard) ---
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # R, L, D, U

            # Handle Giant Star: If current_pos is a giant star, try removing one adjacent BH at a time
            # The state for the next iteration of the main loop (stack.pop()) needs to reflect the *current* state
            # of consumed wormholes and temp_removed_bh *before* considering the effect of a giant star at current_pos.
            # So, we use branch_consumed_wormholes and branch_temp_removed_bh for the standard moves.
            # If a giant star is processed, it creates new states for the stack with its specific BH removal.

            if current_pos in self.giant_stars:
                # print(f"DEBUG Iter: Giant star at {current_pos}. Temp removed before this star: {branch_temp_removed_bh}")
                adjacent_potential_bh = []
                for dr_adj, dc_adj in moves: # Check all 4 adjacent cells
                    adj_r, adj_c = r + dr_adj, c + dc_adj
                    adj_pos = (adj_r, adj_c)
                    # Check if it's a valid cell, a known black hole, AND not already in the set of BHs
                    # temporarily removed by *previous* stars on this path.
                    if self._is_valid(adj_r, adj_c) and \
                       adj_pos in self.black_holes and \
                       adj_pos not in branch_temp_removed_bh: 
                        adjacent_potential_bh.append(adj_pos)
                
                # If there are adjacent, active black holes to remove
                if adjacent_potential_bh:
                    for bh_to_remove_by_this_star in adjacent_potential_bh:
                        # Create a new set of temp_removed_bh for this specific branch of star effect
                        # This includes BHs removed by *previous* stars PLUS the one removed by *this* star
                        path_specific_temp_removed_bh_due_to_star = set(branch_temp_removed_bh)
                        path_specific_temp_removed_bh_due_to_star.add(bh_to_remove_by_this_star)
                        # print(f"DEBUG Iter: Star at {current_pos} attempting to remove {bh_to_remove_by_this_star}. Total removed for this branch: {path_specific_temp_removed_bh_due_to_star}")

                        # Add all 4 moves to the stack with this specific BH removed
                        for dr_move, dc_move in reversed(moves): # Add in reversed order for DFS pop behavior
                            next_r, next_c = r + dr_move, c + dc_move
                            stack.append((
                                next_r, next_c, 
                                energy_for_next_moves, 
                                new_path,              
                                new_visited,           
                                branch_consumed_wormholes, # Wormholes consumed are not affected by this star directly
                                path_specific_temp_removed_bh_due_to_star, # Use the set with the BH removed by *this* star
                                new_energy_log         
                            ))
                    continue # After trying all Giant Star effects, skip standard moves from this cell for this iteration.
                             # The moves from the star cell (with BHs removed) have been added to stack.
                # else:
                    # print(f"DEBUG Iter: Star at {current_pos} has no active adjacent BHs to remove. Proceeding with standard moves.")
            
            # Standard Moves (also applies if Giant Star had no BHs to remove, or if not a star cell)
            # Add moves in reversed order so that (0,1) is tried first due to LIFO stack.pop()
            for dr, dc in reversed(moves): 
                next_r, next_c = r + dr, c + dc
                stack.append((
                    next_r, next_c, 
                    energy_for_next_moves,    # Energy *before* entering (next_r, next_c)
                    new_path,                 # Path taken to reach (r,c)
                    new_visited,              # Visited set to reach (r,c)
                    branch_consumed_wormholes,# Wormholes consumed to reach (r,c)
                    branch_temp_removed_bh,   # BHs removed by stars *before* (r,c)
                    new_energy_log            # Energy log up to (r,c)
                ))
        
        # print("Iterative: No solution found after stack empty.") # Optional debug
        return None, None

if __name__ == '__main__':
    import os
    # Test the game logic
    # Assuming this script is in the project root and 'maps/map.json' exists
    project_root = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(project_root, 'maps', 'map.json')

    if not os.path.exists(map_file):
        print(f"Map file for testing not found: {map_file}")
    else:
        print(f"Loading map from: {map_file}")
        loader = MapLoader(map_file)
        if loader.data:
            game = GameLogic(loader)
            print(f"Starting solver... Origin: {game.start_pos}, Destination: {game.end_pos}, Initial Energy: {game.initial_energy}")
            
            # Adjust map for a simpler test initially if needed
            # Example: Clear some black holes for a known path
            # game.black_holes.clear() # or remove specific ones
            # game.black_holes.discard((3,5))

            solution = game.solve()
            if solution:
                print("Solution found!")
                print("Path:", solution)
                print("Path length (steps):", len(solution))
            else:
                print("No solution found.")
        else:
            print("Failed to load map data for game logic testing.")

    # Example of a more complex map setup for testing specific features:
    # You might want to create a dedicated test_map.json
    # For instance, to test giant stars:
    # Place a giant star next to a black hole that blocks the only path.
    # To test wormholes: Place a wormhole that bypasses a costly or blocked section.
    # To test recharge zones: Place one before a high-cost area or min_charge_cell.
