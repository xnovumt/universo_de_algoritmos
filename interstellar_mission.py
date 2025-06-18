import pygame
import json
import random
import sys
from typing import List, Tuple, Dict, Optional, Set, FrozenSet
import collections # For deque

# sys.setrecursionlimit(4000) # No longer needed for iterative approach

class InterstellarMission:
    def __init__(self, config_filepath: str = "map_config.json"):
        self.config_filepath = config_filepath
        self.font = None
        self.cell_size = 20 # Adjust based on map size and screen
        
        # Game state variables
        self.solutions: List[List[Dict]] = [] # Stores paths, each step is a dict with info
        self.current_solution_idx: int = 0
        self.show_solution_path: bool = False
        self.show_step_by_step: bool = False
        self.current_step: int = 0
        self.search_in_progress: bool = False
        self.max_solutions: int = 1 # Find at least one solution as per prompt

        # Memoization: State: (r, c, current_energy, black_holes_state, used_wormholes_state)
        # Using a tuple as key for memoization.
        # Maps state_key -> max_energy_achieved_at_this_state
        self._visited_states: Dict[Tuple, int] = {} 

        self.load_map_from_json() # Load map on initialization

        # Define colors and icons (basic example)
        self.colors = {
            'empty': (50, 50, 50), 'grid': (100, 100, 100),
            'origin': (0, 255, 0), 'destination': (255, 255, 0),
            'black_hole': (10, 10, 10), 'giant_star': (255, 165, 0),
            'wormhole_entry': (138, 43, 226), 'wormhole_exit': (75, 0, 130),
            'recharge_zone': (0, 191, 255), 'required_charge_cell': (255, 105, 180),
            'path': (0, 0, 255), 'player': (255, 0, 0), 'visited_search': (70,70,90)
        }
        self.icons = {} # Placeholder for actual icon surfaces

    def load_map_from_json(self):
        with open(self.config_filepath, 'r') as f:
            data = json.load(f)

        self.rows: int = data['matriz']['filas']
        self.cols: int = data['matriz']['columnas']
        
        self.origin: Tuple[int, int] = tuple(data['origen'])
        self.destination: Tuple[int, int] = tuple(data['destino'])
        self.initial_ship_energy: int = data['cargaInicial']
        
        self.base_black_holes: FrozenSet[Tuple[int, int]] = frozenset(map(tuple, data['agujerosNegros']))
        self.giant_stars: Set[Tuple[int, int]] = set(map(tuple, data['estrellasGigantes']))
        
        self.wormholes: Dict[Tuple[int, int], Dict] = {}
        for i, wh in enumerate(data['agujerosGusano']):
            entry = tuple(wh['entrada'])
            wh_id = wh.get("id", f"wh_{i}_{entry[0]}-{entry[1]}") 
            self.wormholes[entry] = {
                "id": wh_id, 
                "salida": tuple(wh['salida']),
                "entrada": entry
            }

        self.recharge_zones: Dict[Tuple[int, int], int] = {tuple(rz[:2]): rz[2] for rz in data['zonasRecarga']}
        self.required_charge_cells: Dict[Tuple[int, int], int] = {tuple(rc['coordenada']): rc['cargaGastada'] for rc in data['celdasCargaRequerida']}
        
        self.initial_energy_matrix: List[List[int]] = data['matrizInicial']

        self.solutions = []
        self.current_solution_idx = 0
        self.show_solution_path = False
        self.show_step_by_step = False
        self.current_step = 0
        self.search_in_progress = False


    def _get_adjacent_cells(self, r: int, c: int) -> List[Tuple[int, int]]:
        adj = []
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                adj.append((nr, nc))
        return adj

    def solve(self):
        self.search_in_progress = True
        self.solutions = []
        self._visited_states = {} # Clear memoization cache for new search
        
        # Initial path for the starting state
        initial_path_step = {
            "coords": self.origin,
            "energy_before_move": self.initial_ship_energy,
            "action": "Departed from Origin",
            "black_holes_state": self.base_black_holes, 
            "used_wormholes_state": frozenset(),
            "energy_after_action": self.initial_ship_energy # Initial energy at origin before any moves
        }
        
        # Call the iterative solver
        self._solve_iterative()

        self.search_in_progress = False
        if self.solutions:
            print(f"Found {len(self.solutions)} solution(s). First one shown.")
        else:
            print("No solution found.")


    def _solve_iterative(self):
        # Stack for DFS: (r, c, current_energy_upon_arrival, path_taken, current_black_holes, used_wormholes)
        # We push states that need to be processed.
        
        # The path_taken stores the sequence of steps to reach the current (r,c)
        # We need to make a copy of path_taken when pushing to the stack to ensure
        # each path branch has its own history.
        
        # Initialize stack with the origin state.
        # Path for origin: Only the origin step itself.
        initial_path = [{
            "coords": self.origin,
            "energy_before_move": self.initial_ship_energy, 
            "action": "Departed from Origin",
            "black_holes_state": self.base_black_holes, 
            "used_wormholes_state": frozenset()
            # energy_after_action will be set when processing this 'arrival' state.
        }]

        # State on stack: (r, c, energy_upon_arrival, path_to_this_cell, black_holes_state, used_wormholes_state)
        # We process the 'arrival' effects of (r,c) when we *pop* it from the stack.
        stack = collections.deque() # Using deque as a stack (append and pop from right)
        
        # Initial push: The state *before* applying effects at the origin cell itself.
        # The first step in path_taken represents the origin, and its effects will be applied when processing it.
        stack.append((self.origin[0], self.origin[1], self.initial_ship_energy,
                      initial_path, self.base_black_holes, frozenset()))

        while stack and len(self.solutions) < self.max_solutions:
            # Pop the current state to process
            r, c, current_energy_upon_arrival, path_taken, current_black_holes, used_wormholes = stack.pop()

            # --- Apply effects of the current cell (r,c) AFTER arriving there ---
            energy_for_next_moves = current_energy_upon_arrival
            black_holes_for_this_state = set(current_black_holes) # Mutable copy
            wormholes_for_this_state = set(used_wormholes) # Mutable copy
            action_at_current_cell = ""

            # Recharge Zone effect
            if (r, c) in self.recharge_zones:
                multiplier = self.recharge_zones[(r,c)]
                energy_for_next_moves = current_energy_upon_arrival * multiplier
                action_at_current_cell += f"Recharged at ({r},{c}) by x{multiplier}. New E: {energy_for_next_moves}. "
            
            # Giant Star effect
            if (r, c) in self.giant_stars:
                destroyed_one = False
                adj_cells = self._get_adjacent_cells(r, c)
                random.shuffle(adj_cells) 
                for adj_r, adj_c in adj_cells:
                    if (adj_r, adj_c) in black_holes_for_this_state:
                        black_holes_for_this_state.remove((adj_r, adj_c))
                        action_at_current_cell += f"Giant Star at ({r},{c}) destroyed BH at ({adj_r},{adj_c}). "
                        destroyed_one = True
                        break
                if not destroyed_one:
                    action_at_current_cell += f"Giant Star at ({r},{c}), no adjacent BH to destroy. "
            
            # Convert back to frozenset for hashing
            black_holes_for_this_state_frozen = frozenset(black_holes_for_this_state)
            wormholes_for_this_state_frozen = frozenset(wormholes_for_this_state)

            # Update the last step's info in path_taken with the effects at the current cell.
            # This is crucial for correctly tracking energy and black holes on each step.
            if path_taken: # Only if path_taken is not empty (i.e., not the very first push of origin before any path)
                last_step_info = path_taken[-1]
                # If it's the very first entry (origin), its action might be empty, so add to it.
                if (r,c) == self.origin and last_step_info["action"] == "Departed from Origin":
                     last_step_info["action"] += " " + action_at_current_cell.strip()
                elif action_at_current_cell: # For subsequent cells, just append
                    last_step_info["action"] += " " + action_at_current_cell.strip()

                last_step_info["energy_after_action"] = energy_for_next_moves
                last_step_info["black_holes_state"] = black_holes_for_this_state_frozen
                last_step_info["used_wormholes_state"] = wormholes_for_this_state_frozen

            # --- Memoization Check AFTER applying effects at current cell ---
            state_key = (r, c, energy_for_next_moves, black_holes_for_this_state_frozen, wormholes_for_this_state_frozen)
            if state_key in self._visited_states and self._visited_states[state_key] >= energy_for_next_moves:
                continue # Already visited this state with equal or more energy, so prune this path.
            self._visited_states[state_key] = energy_for_next_moves

            # --- Base Case: Destination Reached ---
            if (r, c) == self.destination:
                self.solutions.append(list(path_taken)) # Append a copy of the path
                if len(self.solutions) >= self.max_solutions:
                    return # Stop searching if enough solutions found
            
            # --- Explore Next Moves (Standard moves and Wormholes) ---

            # 3.1 Wormhole Travel
            if (r, c) in self.wormholes:
                wh_data = self.wormholes[(r,c)]
                wh_id = wh_data["id"]
                if wh_id not in wormholes_for_this_state_frozen: # Only if this wormhole hasn't been used in *this path*
                    exit_r, exit_c = wh_data["salida"]
                    new_used_wormholes = wormholes_for_this_state_frozen | {wh_id} 
                    
                    # Prepare the next step info for the wormhole jump
                    next_step_info = {
                        "coords": (exit_r, exit_c),
                        "energy_before_move": energy_for_next_moves, # Energy before taking wormhole
                        "action": f"Took wormhole {wh_id} from ({r},{c}) to ({exit_r},{exit_c}).",
                        "energy_after_action": -1, # Placeholder, will be updated when this state is popped
                        "black_holes_state": black_holes_for_this_state_frozen,
                        "used_wormholes_state": new_used_wormholes
                    }
                    new_path = path_taken + [next_step_info]
                    stack.append((exit_r, exit_c, energy_for_next_moves, new_path,
                                  black_holes_for_this_state_frozen, new_used_wormholes))


            # 3.2 Standard Moves
            moves = [(0, 1, "Right"), (0, -1, "Left"), (1, 0, "Down"), (-1, 0, "Up")]
            # No need to randomize for iterative DFS unless you want to find different solutions.
            # For finding *any* solution, order doesn't strictly matter for correctness, just for which one is found first.
            # Reversing for DFS-like behavior (exploring deepest first)
            # stack.extend() would push in reverse order, so we iterate normally.
            # If using BFS (deque.popleft()), you'd want to extend with moves in preferred order.
            
            for dr, dc, move_name in moves:
                nr, nc = r + dr, c + dc

                if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                    continue
                
                if (nr, nc) in black_holes_for_this_state_frozen:
                    continue

                if (nr, nc) in self.required_charge_cells:
                    min_required = self.required_charge_cells[(nr, nc)]
                    if energy_for_next_moves < min_required:
                        continue

                cost_from_matrix = self.initial_energy_matrix[nr][nc]
                if (nr, nc) in self.recharge_zones:
                    cost_from_matrix = 0 
                
                energy_after_moving_to_nr_nc = energy_for_next_moves - cost_from_matrix

                if energy_after_moving_to_nr_nc < 0:
                    continue

                # Prepare the next step info for standard move
                next_step_info = {
                    "coords": (nr, nc),
                    "energy_before_move": energy_for_next_moves, # Energy before consuming cost
                    "action": f"Moved {move_name} to ({nr},{nc}). Cost: {cost_from_matrix}.",
                    "energy_after_action": -1, # Placeholder, will be updated when this state is popped
                    "black_holes_state": black_holes_for_this_state_frozen, 
                    "used_wormholes_state": wormholes_for_this_state_frozen 
                }
                new_path = path_taken + [next_step_info]
                
                stack.append((nr, nc, energy_after_moving_to_nr_nc, new_path,
                              black_holes_for_this_state_frozen, wormholes_for_this_state_frozen))

    def draw(self, screen: pygame.Surface):
        screen.fill((30,30,30)) # Dark background
        
        current_black_holes_for_display = self.base_black_holes # Default to original black holes
        current_used_wormholes_for_display = frozenset() # Default to no wormholes used

        if self.show_solution_path and self.solutions:
            current_path_steps = self.solutions[self.current_solution_idx]
            if self.show_step_by_step:
                step_idx = min(self.current_step, len(current_path_steps) - 1)
                if step_idx >= 0:
                    current_step_data = current_path_steps[step_idx]
                    current_black_holes_for_display = current_step_data.get("black_holes_state", self.base_black_holes)
                    current_used_wormholes_for_display = current_step_data.get("used_wormholes_state", frozenset())
            else:
                if current_path_steps:
                    final_step_data = current_path_steps[-1]
                    current_black_holes_for_display = final_step_data.get("black_holes_state", self.base_black_holes)
                    current_used_wormholes_for_display = final_step_data.get("used_wormholes_state", frozenset())


        # Draw grid and cells
        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                rect = pygame.Rect(c_idx * self.cell_size, r_idx * self.cell_size, self.cell_size, self.cell_size)
                cell_coord = (r_idx, c_idx)
                color = self.colors['empty']
                icon_text = None 

                if cell_coord == self.origin: color = self.colors['origin']; icon_text = "O"
                elif cell_coord == self.destination: color = self.colors['destination']; icon_text = "D"
                elif cell_coord in current_black_holes_for_display:
                    color = self.colors['black_hole']; icon_text = "BH"
                elif cell_coord in self.giant_stars: color = self.colors['giant_star']; icon_text = "GS"
                elif cell_coord in self.wormholes:
                    wh_id = self.wormholes[cell_coord]["id"]
                    if wh_id in current_used_wormholes_for_display:
                        color = (self.colors['wormhole_entry'][0] // 2, self.colors['wormhole_entry'][1] // 2, self.colors['wormhole_entry'][2] // 2)
                        icon_text = "WE(U)" 
                    else:
                        color = self.colors['wormhole_entry']; icon_text = "WE"
                elif any(wh['salida'] == cell_coord for wh in self.wormholes.values()):
                    wh_entry_for_exit = next(iter([entry for entry, wh_data in self.wormholes.items() if wh_data['salida'] == cell_coord]), None)
                    if wh_entry_for_exit:
                        wh_id_for_exit = self.wormholes[wh_entry_for_exit]["id"]
                        if wh_id_for_exit in current_used_wormholes_for_display:
                            color = (self.colors['wormhole_exit'][0] // 2, self.colors['wormhole_exit'][1] // 2, self.colors['wormhole_exit'][2] // 2)
                            icon_text = "WX(U)" 
                        else:
                            color = self.colors['wormhole_exit']; icon_text = "WX"
                elif cell_coord in self.recharge_zones: color = self.colors['recharge_zone']; icon_text = "RZ"
                elif cell_coord in self.required_charge_cells: color = self.colors['required_charge_cell']; icon_text = "RC"
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, self.colors['grid'], rect, 1) 

                if icon_text and self.font and self.cell_size > 15:
                    text_surf = self.font.render(icon_text, True, (200,200,200) if icon_text not in ["O", "D"] else (0,0,0))
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)
        
        if self.show_solution_path and self.solutions:
            current_path_steps = self.solutions[self.current_solution_idx]
            
            path_to_draw = current_path_steps
            if self.show_step_by_step:
                path_to_draw = current_path_steps[:min(self.current_step + 1, len(current_path_steps))]

            for i, step_data in enumerate(path_to_draw):
                r, c = step_data["coords"]
                rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
                
                if i == len(path_to_draw) - 1 and self.show_step_by_step:
                    pygame.draw.rect(screen, self.colors['player'], rect, 0) 
                    pygame.draw.rect(screen, (255,255,255), rect, 2)
                elif (r,c) != self.origin:
                    path_color = pygame.Color(self.colors['path'])
                    pygame.draw.rect(screen, path_color, rect.inflate(-self.cell_size//3, -self.cell_size//3)) 

        if self.font:
            info_text = self.get_hud_info()
            info_surf = self.font.render(info_text, True, (255, 255, 255))
            screen.blit(info_surf, (10, self.rows * self.cell_size + 10))

            if self.show_step_by_step and self.solutions and 0 <= self.current_solution_idx < len(self.solutions):
                if 0 <= self.current_step < len(self.solutions[self.current_solution_idx]):
                    step_detail = self.solutions[self.current_solution_idx][self.current_step]
                    action = step_detail["action"]
                    energy = step_detail.get("energy_after_action", step_detail.get("energy_before_move"))
                    detail_text = f"Step Action: {action} | Energy: {energy:.0f}"
                    detail_surf = self.font.render(detail_text, True, (220, 220, 100))
                    screen.blit(detail_surf, (10, self.rows * self.cell_size + 30))


    def get_hud_info(self) -> str:
        if self.search_in_progress:
            return "Searching for solutions..."
        if not self.solutions:
            return "No solutions found!"
        
        text = f"Solutions: {len(self.solutions)}"
        if self.show_solution_path:
            text += f" | Showing: {self.current_solution_idx + 1}/{len(self.solutions)}"
            path_len = len(self.solutions[self.current_solution_idx])
            text += f" | Length: {path_len} steps."
            if self.show_step_by_step:
                current_display_step = min(self.current_step + 1, path_len)
                text += f" | Animating Step: {current_display_step}/{path_len}"
        return text