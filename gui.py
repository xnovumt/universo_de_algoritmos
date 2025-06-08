import pygame
import sys
import os

# Definición de colores (RGB)
COLOR_TEXTO = (230, 230, 230) # Un color claro para el texto de estado
STATUS_BAR_HEIGHT = 30
COLOR_NEGRO = (0, 0, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_GRIS = (200, 200, 200)
COLOR_LINEA_CUADRICULA = (100, 100, 100)
COLOR_ORIGEN = (0, 255, 0)  # Verde
COLOR_DESTINO = (255, 0, 0) # Rojo
COLOR_CAMINO = (0, 0, 255)   # Azul

# Tamaño de cada celda en la cuadrícula y margen
TAMANO_CELDA = 20  # Puedes ajustar esto según el tamaño de tu mapa y pantalla
MARGEN = 1

class GameGUI:
    def __init__(self, game_logic, solution_path, solution_energy_levels):
        self.game_logic = game_logic
        self.map_data = game_logic.map_loader # Acceso a los datos crudos del mapa si es necesario
        self.rows, self.cols = self.game_logic.rows, self.game_logic.cols
        self.solution_path = solution_path
        self.solution_energy_levels = solution_energy_levels
        self.current_energy_display = 0
        if self.solution_path and self.solution_energy_levels:
            # Initialize with energy at the start of the path if available
            if len(self.solution_energy_levels) > 0:
                 # Assuming current_step_of_animation = 1 is the first step shown
                self.current_energy_display = self.solution_energy_levels[0] 
        if self.solution_path:
            self.current_step_of_animation = 1 # Start at step 1 to show the first position
        else:
            self.current_step_of_animation = 0

        pygame.init()
        pygame.font.init() # Para texto
        self.font = pygame.font.SysFont('Arial', 10) # Fuente para los costos de energía
        self.status_font = pygame.font.SysFont('Arial', 18) # Fuente para el texto de estado (energía)

        # Calcular dimensiones de la pantalla
        self.ancho_pantalla = self.cols * (TAMANO_CELDA + MARGEN) + MARGEN
        self.alto_pantalla = self.rows * (TAMANO_CELDA + MARGEN) + MARGEN + STATUS_BAR_HEIGHT # Añadir espacio para la barra de estado
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("Exploración Galáctica")

        self.clock = pygame.time.Clock()
        self.animating = False # Controla si la animación automática está activa
        self.animation_speed = 80  # Milisegundos por paso de animación
        self.animation_timer = 0

        # Cargar imágenes (placeholders por ahora, se cargarán desde assets/)
        self.imagenes_celdas = {}
        self.cargar_imagenes() # Descomentar cuando tengamos imágenes

    def cargar_imagenes(self):
        """Carga las imágenes para los diferentes tipos de celdas desde la carpeta 'assets'."""

        self.imagenes_celdas = {}
        tipos_imagenes = {
            'nave': 'nave.png',
            'agujero_negro': 'agujero_negro.png',
            'estrella_gigante': 'estrella_gigante.png',
            'agujero_gusano': 'agujero_gusano.png',
            'zona_recarga': 'zona_recarga.png',
            'celda_requerida': 'celda_requerida.png'
        }

        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_assets = os.path.join(ruta_base, 'assets')
        
        if not os.path.isdir(ruta_assets):
            return

        for tipo, nombre_archivo in tipos_imagenes.items():
            ruta_completa = os.path.join(ruta_assets, nombre_archivo)
            try:
                imagen = pygame.image.load(ruta_completa).convert_alpha()
                self.imagenes_celdas[tipo] = pygame.transform.scale(imagen, (TAMANO_CELDA, TAMANO_CELDA))
            except pygame.error as e:
                pass

    def dibujar_cuadricula(self):
        self.pantalla.fill(COLOR_NEGRO) 

        # Actualizar y mostrar la energía actual
        if self.solution_path and self.solution_energy_levels and self.current_step_of_animation > 0 and self.current_step_of_animation <= len(self.solution_energy_levels):
            self.current_energy_display = self.solution_energy_levels[self.current_step_of_animation -1]
        
        energy_text_surface = self.status_font.render(f"Energía: {self.current_energy_display:.2f}", True, COLOR_TEXTO)
        text_rect = energy_text_surface.get_rect(centerx=self.ancho_pantalla / 2, centery=STATUS_BAR_HEIGHT / 2) # Center in status bar
        # Or, for left alignment in status bar, vertically centered:
        # text_rect = energy_text_surface.get_rect(left=MARGEN + 5, centery=STATUS_BAR_HEIGHT / 2)
        self.pantalla.blit(energy_text_surface, text_rect.topleft) # Dibujar en la barra de estado


        for fila in range(self.rows):
            for columna in range(self.cols):
                rect = pygame.Rect(
                    columna * (TAMANO_CELDA + MARGEN) + MARGEN,
                    fila * (TAMANO_CELDA + MARGEN) + MARGEN + STATUS_BAR_HEIGHT, # Offset por la barra de estado
                    TAMANO_CELDA,
                    TAMANO_CELDA
                )
                pos_actual = (fila, columna)
                color_celda = COLOR_GRIS 

                if pos_actual == self.game_logic.start_pos:
                    color_celda = COLOR_ORIGEN
                elif pos_actual == self.game_logic.end_pos:
                    color_celda = COLOR_DESTINO
                
                pygame.draw.rect(self.pantalla, color_celda, rect)

                icono_dibujado = False

                # --- Inicio del bloque de dibujo de íconos ---
                if 'agujero_negro' in self.imagenes_celdas:
                    if pos_actual in self.game_logic.black_holes:
                        self.pantalla.blit(self.imagenes_celdas['agujero_negro'], rect.topleft)
                        icono_dibujado = True
                
                if not icono_dibujado and 'estrella_gigante' in self.imagenes_celdas:
                    if pos_actual in self.game_logic.giant_stars:
                        self.pantalla.blit(self.imagenes_celdas['estrella_gigante'], rect.topleft)
                        icono_dibujado = True

                if not icono_dibujado and 'agujero_gusano' in self.imagenes_celdas:
                    if pos_actual in self.game_logic.wormholes_map: # Verifica si pos_actual es una entrada de agujero de gusano
                        self.pantalla.blit(self.imagenes_celdas['agujero_gusano'], rect.topleft)
                        icono_dibujado = True
                
                if not icono_dibujado and 'zona_recarga' in self.imagenes_celdas:
                    if pos_actual in self.game_logic.recharge_zones: # Verifica si pos_actual es una zona de recarga
                        self.pantalla.blit(self.imagenes_celdas['zona_recarga'], rect.topleft)
                        icono_dibujado = True

                if not icono_dibujado and 'celda_requerida' in self.imagenes_celdas:
                    if pos_actual in self.game_logic.min_charge_cells: # Verifica si pos_actual es una celda con carga mínima
                        self.pantalla.blit(self.imagenes_celdas['celda_requerida'], rect.topleft)
                        icono_dibujado = True
                # --- Fin del bloque de dibujo de íconos ---

                if not icono_dibujado and pos_actual != self.game_logic.start_pos and pos_actual != self.game_logic.end_pos:
                    # Comprobación para no dibujar costo sobre ninguna celda especial (incluso si el ícono no se cargó)
                    is_any_special_cell = (
                        pos_actual in self.game_logic.black_holes or
                        pos_actual in self.game_logic.giant_stars or
                        pos_actual in self.game_logic.wormholes_map or 
                        pos_actual in self.game_logic.recharge_zones or 
                        pos_actual in self.game_logic.min_charge_cells
                    )
                    if not is_any_special_cell:
                        costo = self.game_logic.energy_costs[fila][columna]
                        texto_costo = self.font.render(str(costo), True, COLOR_NEGRO)
                        text_rect = texto_costo.get_rect(center=rect.center)
                        self.pantalla.blit(texto_costo, text_rect.topleft)

        # Dibujar el camino encontrado (hasta el paso actual de la animación)
        if self.solution_path:
            for i in range(self.current_step_of_animation):
                paso = self.solution_path[i]
                rect_camino = pygame.Rect(
                    paso[1] * (TAMANO_CELDA + MARGEN) + MARGEN,
                    paso[0] * (TAMANO_CELDA + MARGEN) + MARGEN,
                    TAMANO_CELDA,
                    TAMANO_CELDA
                )
                # No sobrescribir origen y destino con el color del camino
                if paso != self.game_logic.start_pos and paso != self.game_logic.end_pos:
                    # Define el rectángulo para dibujar el segmento del camino, aplicando el offset de la barra de estado
                    rect_path_segment_draw = pygame.Rect(
                        paso[1] * (TAMANO_CELDA + MARGEN) + MARGEN,  # Posición X del paso del camino
                        paso[0] * (TAMANO_CELDA + MARGEN) + MARGEN + STATUS_BAR_HEIGHT, # Posición Y del paso del camino + offset
                        TAMANO_CELDA,
                        TAMANO_CELDA
                    )
                    pygame.draw.rect(self.pantalla, COLOR_CAMINO, rect_path_segment_draw) # Dibuja el fondo azul del camino
                
                # Dibujar la nave en la posición actual del camino animado
                if i == self.current_step_of_animation - 1: # 'paso' es self.solution_path[i]
                    if 'nave' in self.imagenes_celdas and self.imagenes_celdas['nave']:
                        img_nave_actual = self.imagenes_celdas['nave']
                        # Calcular la esquina superior izquierda de la celda base para la nave (con offset)
                        celda_x_base_nave = paso[1] * (TAMANO_CELDA + MARGEN) + MARGEN
                        celda_y_base_nave = paso[0] * (TAMANO_CELDA + MARGEN) + MARGEN + STATUS_BAR_HEIGHT
                        
                        # Centrar la imagen de la nave en la celda
                        pos_x_nave = celda_x_base_nave + (TAMANO_CELDA - img_nave_actual.get_width()) // 2
                        pos_y_nave = celda_y_base_nave + (TAMANO_CELDA - img_nave_actual.get_height()) // 2
                        self.pantalla.blit(img_nave_actual, (pos_x_nave, pos_y_nave))
                    else: # Placeholder si no hay imagen de nave (dibuja un círculo amarillo)
                        pygame.draw.circle(self.pantalla, (255, 255, 0), rect_camino.center, TAMANO_CELDA // 3)
    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # Terminar el bucle principal
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.solution_path:
                        if self.animating:
                            self.animating = False # Pausar animación
                        else:
                            # Si está al final, reiniciar antes de empezar
                            if self.current_step_of_animation >= len(self.solution_path):
                                self.current_step_of_animation = 0
                            self.animating = True # Iniciar o reanudar animación
                            self.animation_timer = pygame.time.get_ticks() # Reset timer
                elif event.key == pygame.K_RIGHT:
                    if self.solution_path and not self.animating: # Solo avanzar si está pausado
                        if self.current_step_of_animation < len(self.solution_path):
                            self.current_step_of_animation += 1
                        # Si se avanza manualmente al último paso, la animación no debe continuar automáticamente
                        if self.current_step_of_animation >= len(self.solution_path):
                             self.animating = False 
                elif event.key == pygame.K_r: # Tecla R para reiniciar animación
                    if self.solution_path:
                        self.current_step_of_animation = 0
                        self.animating = False # Dejar pausado en el inicio
        return True

    def actualizar_animacion(self):
        if self.animating and self.solution_path:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_speed:
                if self.current_step_of_animation < len(self.solution_path):
                    self.current_step_of_animation += 1
                    self.animation_timer = current_time
                else:
                    self.animating = False # Detener al final del camino 

    def ejecutar(self):
        """Bucle principal del juego."""
        corriendo = True
        while corriendo:
            corriendo = self.manejar_eventos()
            self.actualizar_animacion()
            self.dibujar_cuadricula()
            pygame.display.flip()  # Actualizar la pantalla completa
            self.clock.tick(30)  # Limitar a 30 FPS

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    # Esto es solo para probar gui.py de forma aislada.
    # Necesitaríamos un mock de GameLogic y solution_path
    print("Para probar GameGUI, ejecútalo desde main.py después de resolver el mapa.")
    
    # Ejemplo de cómo podría ser un mock (muy simplificado):
    class MockMapLoader:
        def __init__(self):
            self.data = True # Simula que hay datos
            self.matriz = {'filas': 10, 'columnas': 10}
            self.origen = (0,0)
            self.destino = (9,9)
            self.cargaInicial = 100
            self.matrizInicial = [[1]*10 for _ in range(10)]
            self.agujerosNegros = []
            self.estrellasGigantes = []
            self.agujerosGusano = []
            self.zonasRecarga = []
            self.celdasCargaRequerida = []
        def get_dimensions(self): return self.matriz['filas'], self.matriz['columnas']
        def get_start_location(self): return self.origen
        def get_end_location(self): return self.destino
        def get_initial_charge(self): return self.cargaInicial
        def get_energy_costs(self): return self.matrizInicial
        def get_black_holes(self): return self.agujerosNegros
        def get_giant_stars(self): return self.estrellasGigantes
        def get_wormholes(self): return self.agujerosGusano
        def get_recharge_zones(self): return self.zonasRecarga
        def get_required_charge_cells(self): return self.celdasCargaRequerida

    class MockGameLogic:
        def __init__(self):
            self.map_loader = MockMapLoader()
            self.rows, self.cols = self.map_loader.get_dimensions()
            self.start_pos = self.map_loader.get_start_location()
            self.end_pos = self.map_loader.get_end_location()
            self.initial_energy = self.map_loader.get_initial_charge()
            self.energy_costs = self.map_loader.get_energy_costs()
            self.black_holes = set()
            self.giant_stars = set()
            self.wormholes_map = {}
            self.recharge_zones = {}
            self.min_charge_cells = {}

    mock_game_logic = MockGameLogic()
    # Simula un camino solución para probar la animación
    mock_solution = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3)] 
    
    # Para que el test funcione, Pygame debe estar inicializado
    # y las fuentes también, lo cual ocurre en GameGUI.__init__
    # gui_test = GameGUI(mock_game_logic, mock_solution)
    # gui_test.ejecutar()
    pass # Evitar que se ejecute automáticamente al importar

