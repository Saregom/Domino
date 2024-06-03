import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
screen_width = 800
screen_height = 600

# Crear la ventana
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ejemplo de Alerta en Pygame')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fuente
font = pygame.font.Font(None, 36)

# Función para mostrar una alerta
def show_alert(message):
    alert_width = 400
    alert_height = 200
    alert_x = (screen_width - alert_width) // 2
    alert_y = (screen_height - alert_height) // 2
    
    alert_rect = pygame.Rect(alert_x, alert_y, alert_width, alert_height)
    pygame.draw.rect(screen, RED, alert_rect)
    pygame.draw.rect(screen, BLACK, alert_rect, 2)
    
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(alert_x + alert_width // 2, alert_y + alert_height // 2))
    screen.blit(text, text_rect)
    
    # Actualizar pantalla para mostrar alerta
    pygame.display.update()
    
    # Esperar a que el usuario presione una tecla para cerrar la alerta
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # Mostrar alerta al presionar la tecla 'A'
                show_alert('¡Alerta!')

    # Rellenar la pantalla con blanco
    screen.fill(WHITE)
    
    # Actualizar pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()

