from map_loader import MapLoader
from game_logic import GameLogic
import gui # Importar GameGUI desde gui.py
import os

def run_game():
    # Construir la ruta absoluta al archivo del mapa
    project_root = os.path.dirname(os.path.abspath(__file__))
    MAP_FILENAME = 'maps/map_30x30_test.json'
    map_file_path = os.path.join(project_root, MAP_FILENAME)

    if not os.path.exists(map_file_path):
        print(f"Error: Archivo de mapa no encontrado en {map_file_path}")
        print("Por favor, asegúrate que el archivo de mapa exista en el directorio del proyecto.")
        return

    loader = MapLoader(map_file_path)

    if not loader.data: # Verificar si los datos se cargaron correctamente
        print("Error: Fallo al cargar los datos del mapa. Saliendo.")
        return

    game = GameLogic(loader)

    solution_path, solution_energy_levels = game.solve()

    if solution_path:
        pass # La GUI mostrará la solución
    else:
        pass # La GUI mostrará que no hay solución (camino vacío)

    # --- Integración de la GUI ---
    if game: # Asegurarse que la lógica del juego se inicializó
        game_interface = gui.GameGUI(game, solution_path, solution_energy_levels)
        game_interface.ejecutar()
    else:
        # Este caso es poco probable si las verificaciones anteriores pasaron,
        # pero se mantiene por seguridad.
        print("Error: No se pudo inicializar la lógica del juego para la GUI.")
        return

if __name__ == "__main__":
    run_game()

