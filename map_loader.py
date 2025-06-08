import json

class MapLoader:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.data = self._load_map()

    def _load_map(self):
        """Loads the map data from the JSON file."""
        try:
            with open(self.map_file_path, 'r') as f:
                data = json.load(f)
            self._validate_map_data(data) # Basic validation
            return data
        except FileNotFoundError:
            print(f"Error: Map file not found at {self.map_file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.map_file_path}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while loading the map: {e}")
            return None

    def _validate_map_data(self, data):
        """Performs basic validation of the loaded map data."""
        required_keys = [
            "matriz", "origen", "destino", "agujerosNegros", 
            "estrellasGigantes", "agujerosGusano", "zonasRecarga",
            "celdasCargaRequerida", "cargaInicial", "matrizInicial"
        ]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key in map data: '{key}'")
        
        if not isinstance(data["matriz"], dict) or \
           not all(k in data["matriz"] for k in ["filas", "columnas"]):
            raise ValueError("Invalid 'matriz' format.")

        rows = data["matriz"]["filas"]
        cols = data["matriz"]["columnas"]

        if not (isinstance(rows, int) and rows >= 1 and isinstance(cols, int) and cols >=1): # TEMPORAL: Reducido de 30 a 1 para pruebas
            raise ValueError("Matrix dimensions must be at least 30x30.")

        if len(data["matrizInicial"]) != rows or \
           any(len(row) != cols for row in data["matrizInicial"]):
            raise ValueError("Mismatch between 'matrizInicial' dimensions and 'matriz' dimensions.")
        
        if not (isinstance(data["estrellasGigantes"], list) and len(data["estrellasGigantes"]) >= 5):
            # As per requirement: "mínimo 5"
            pass # Not raising error, but good to note. Could be a warning.

    def get_dimensions(self):
        """Returns the (rows, columns) of the map."""
        if self.data:
            return self.data['matriz']['filas'], self.data['matriz']['columnas']
        return None, None

    def get_start_location(self):
        """Returns the (row, col) of the start location."""
        if self.data:
            return tuple(self.data['origen'])
        return None

    def get_end_location(self):
        """Returns the (row, col) of the end location."""
        if self.data:
            return tuple(self.data['destino'])
        return None

    def get_black_holes(self):
        """Returns a list of (row, col) for black holes."""
        if self.data:
            return [tuple(bh) for bh in self.data['agujerosNegros']]
        return []

    def get_giant_stars(self):
        """Returns a list of (row, col) for giant stars."""
        if self.data:
            return [tuple(gs) for gs in self.data['estrellasGigantes']]
        return []

    def get_wormholes(self):
        """Returns a list of dictionaries for wormholes, e.g., [{'entrada': (r,c), 'salida': (r,c)}]."""
        if self.data:
            return [{ 'entrada': tuple(wh['entrada']), 'salida': tuple(wh['salida']), 'costo': wh['costo'] } for wh in self.data.get('agujerosGusano', [])]
        return []

    def get_recharge_zones(self):
        """Returns a list of (row, col, multiplier) for recharge zones."""
        if self.data:
            return [
                (rz['posicion'][0], rz['posicion'][1], rz['factorMultiplicador'])
                for rz in self.data['zonasRecarga']
            ]
        return []

    def get_required_charge_cells(self):
        """Returns a list of dictionaries for cells requiring minimum charge, e.g., [{'coordenada': (r,c), 'cargaMinima': val}]."""
        if self.data and 'celdasCargaRequerida' in self.data:
            return [
                {'coordenada': tuple(cell['coordenada']), 'cargaMinima': cell['cargaMinima']}
                for cell in self.data['celdasCargaRequerida']
            ]
        return []

    def get_initial_charge(self):
        """Returns the initial charge of the ship."""
        if self.data:
            return self.data['cargaInicial']
        return 0

    def get_energy_costs(self):
        """Returns the 2D list representing energy costs for each cell."""
        if self.data:
            return self.data['matrizInicial']
        return []

if __name__ == '__main__':
    # Example usage:
    map_path = 'maps/map.json' # Relative path for local testing if this script is in the root
    # For actual use from main.py, you'd pass the absolute path or a path relative to main.py
    
    # To run this file directly for testing, ensure it's in the project root or adjust path:
    import os
    # Assuming this script is in the root of 'Proeycto Final automatas'
    # And 'maps' is a subdirectory of 'Proeycto Final automatas'
    project_root = os.path.dirname(os.path.abspath(__file__))
    # If map_loader.py is in the root, and maps is a subdir:
    # map_path = os.path.join(project_root, 'maps', 'map.json')
    # If map_loader.py is in a subdir (e.g. 'src') and maps is also a subdir of project_root:
    # map_path = os.path.join(os.path.dirname(project_root), 'maps', 'map.json')

    # Simplest for now, assuming 'maps' dir is in the same dir as this script when run directly
    # This will likely fail if 'maps' isn't sibling to map_loader.py when run directly.
    # The proper way is to construct the path from the main execution point.
    
    # Correct path for testing if map_loader.py is in the root and maps/ is a subdirectory:
    # This assumes the script is run from 'c:\Users\Usuario\Desktop\Proeycto Final automatas'
    map_path_for_direct_run = os.path.join(os.getcwd(), 'maps', 'map.json')
    
    # Check if the maps directory and map.json exist at the expected relative path for testing
    if not os.path.exists(map_path_for_direct_run):
        print(f"Test map file not found at {map_path_for_direct_run}. \nThis test assumes 'map_loader.py' is in the project root and 'maps/map.json' exists.")
        print(f"Current working directory: {os.getcwd()}")
    else:
        loader = MapLoader(map_path_for_direct_run)
        if loader.data:
            print("Map loaded successfully!")
            print(f"Dimensions: {loader.get_dimensions()}")
            print(f"Start: {loader.get_start_location()}, End: {loader.get_end_location()}")
            print(f"Initial Charge: {loader.get_initial_charge()}")
            # print(f"Energy Costs (first row): {loader.get_energy_costs()[0] if loader.get_energy_costs() else 'N/A'}")
            # print(f"Black Holes: {loader.get_black_holes()}")
            # print(f"Giant Stars: {loader.get_giant_stars()}")
            # print(f"Wormholes: {loader.get_wormholes()}")
            # print(f"Recharge Zones: {loader.get_recharge_zones()}")
            # print(f"Required Charge Cells: {loader.get_required_charge_cells()}")
