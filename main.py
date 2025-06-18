import pygame
import sys
import threading
from interstellar_mission import InterstellarMission

# --- Pygame Configuration ---
UI_INFO_AREA_HEIGHT = 60 # Extra space at the bottom for text
DEFAULT_CELL_SIZE = 20 # Adjust as needed, or make dynamic
ANIMATION_DELAY_MS = 200 # Milliseconds between animation steps

def run_game():
    pygame.init()
    pygame.font.init() # Initialize font module
    
    # Create mission object - it will load JSON and determine map size
    # IMPORTANT CHANGE: Updated config_filepath to "matriz_universo.json"
    mission = InterstellarMission(config_filepath="matriz_universo.json")
    
    # Dynamically set screen size based on map and cell size
    screen_width = mission.cols * mission.cell_size
    screen_height = mission.rows * mission.cell_size + UI_INFO_AREA_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Interstellar Mission")
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24) # Default Pygame font
    mission.font = font # Pass font to mission for its drawing methods

    search_finished_event = threading.Event()
    search_thread = None # Initialize thread variable

    def search_task_wrapper():
        mission.solve() # Call the main solve method
        search_finished_event.set()

    # Initial search
    print("Starting initial search...")
    mission.search_in_progress = True
    search_finished_event.clear()
    search_thread = threading.Thread(target=search_task_wrapper, daemon=True)
    search_thread.start()

    last_animation_update_time = pygame.time.get_ticks()

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN: # Moved all keydown handling into this block
                if event.key == pygame.K_SPACE: # Toggle solution visibility
                    mission.show_solution_path = not mission.show_solution_path
                    if not mission.solutions and not mission.search_in_progress: # Trigger search if no solution and trying to show
                        print("No solution to show. Starting search...")
                        mission.search_in_progress = True
                        search_finished_event.clear()
                        search_thread = threading.Thread(target=search_task_wrapper, daemon=True)
                        search_thread.start()
                elif event.key == pygame.K_s: # Toggle step-by-step animation
                    mission.show_step_by_step = not mission.show_step_by_step
                    mission.current_step = 0 # Reset animation to start
                    last_animation_update_time = pygame.time.get_ticks() # Reset timer
                elif event.key == pygame.K_n: # Next solution
                    if mission.solutions:
                        mission.current_solution_idx = (mission.current_solution_idx + 1) % len(mission.solutions)
                        mission.current_step = 0
                        last_animation_update_time = pygame.time.get_ticks() # Reset timer for new path
                elif event.key == pygame.K_r: # Reset and restart search
                    print("Resetting and starting new search...")
                    if search_thread and search_thread.is_alive():
                        print("Warning: Previous search thread is still running. This might cause issues if map data is mutable.")
                    
                    mission.load_map_from_json() # Reload map from JSON (clears solutions, resets state)
                    mission.search_in_progress = True
                    search_finished_event.clear()
                    search_thread = threading.Thread(target=search_task_wrapper, daemon=True)
                    search_thread.start()

        # Animation update logic
        if mission.show_step_by_step and mission.solutions:
            current_time = pygame.time.get_ticks()
            if current_time - last_animation_update_time > ANIMATION_DELAY_MS:
                if mission.current_step < len(mission.solutions[mission.current_solution_idx]) - 1:
                    mission.current_step += 1
                else:
                    # Animation finished for this path, can loop or stop
                    pass 
                last_animation_update_time = current_time

        # Drawing
        mission.draw(screen)
        pygame.display.flip()
        
        clock.tick(60) # Cap frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()