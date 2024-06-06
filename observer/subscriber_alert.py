import pygame
from observer.interface_subscriber import Interface_subscriber

# Clase Notificacion del patron OBSERVER
class Subsciber_alert(Interface_subscriber): 
    def alert(self, screen, width, height, message): # Metodo Update de la clase OBSERVER
        alert_width = 400
        alert_height = 100

        alert_x = (width - alert_width) // 2
        alert_y = height

        font = pygame.font.Font(None, 27)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 71, 71)
        
        alert_rect = pygame.Rect(alert_x, alert_y, alert_width, alert_height)
        pygame.draw.rect(screen, RED, alert_rect)
        pygame.draw.rect(screen, BLACK, alert_rect, 2)
        
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(alert_x + alert_width // 2, alert_y + alert_height // 2))
        screen.blit(text, text_rect)

    