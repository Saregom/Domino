import pygame
from proxy.interface_game import Interface_game

class Proxy_game(Interface_game):
    def __init__(self):
        self.show_alert = False


    def alert(self, screen ,width, height):
        
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
        
        text = font.render('No se pueden seleccionar fichas del otro jugador', True, WHITE)
        text_rect = text.get_rect(center=(alert_x + alert_width // 2, alert_y + alert_height // 2))
        screen.blit(text, text_rect)
        
        # Actualizar pantalla para mostrar alerta
        pygame.display.update()

    def verify_player(self, player_turn):
        if player_turn is "player":
            return True
        else:
            return False
        
