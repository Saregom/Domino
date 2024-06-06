import pygame
from observer.interface_subsciber import AbstractSubscriber

# Clase Notificacion del patron OBSERVER
class Subsciber_alert(AbstractSubscriber): 
    def alert(self, screen ,width, height, message):
        alert_width = 800
        alert_height = 200
        alert_x = (width - alert_width) // 2
        alert_y = (height - alert_height) // 2
        font = pygame.font.Font(None, 36)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        
        alert_rect = pygame.Rect(alert_x, alert_y, alert_width, alert_height)
        pygame.draw.rect(screen, RED, alert_rect)
        pygame.draw.rect(screen, BLACK, alert_rect, 2)
        
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(alert_x + alert_width // 2, alert_y + alert_height // 2))
        screen.blit(text, text_rect)

    