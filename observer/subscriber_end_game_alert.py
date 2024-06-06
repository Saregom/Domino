import pygame
from observer.interface_subscriber import Interface_subscriber

# Clase Notificacion del patron OBSERVER
class Subscriber_end_game_alert(Interface_subscriber):
    # Muestra la surface de game over
    def alert(self, screen, width, height, info):
        srfc_game_over = pygame.Surface((800, 400))
        srfc_game_over_rect = srfc_game_over.get_rect(x=(width-800)//2, y=(height-400)//2) #Rect: Recibe las colisiones

        play_again_option = pygame.Surface((213, 57), pygame.SRCALPHA) #pygame.SRCALPHA: permita la opacidad
        play_again_option_rect = play_again_option.get_rect(x=srfc_game_over_rect.x+295, y=srfc_game_over_rect.y+325)
        play_again_option.fill((0, 0, 0, 0)) # fill(R, G, B, Opacity)
        
        srfc_game_over.blit(pygame.image.load('assets/game_over.png'), (0,0))

        if info[0] != "Empate": winner_txt = pygame.font.SysFont("Fira Code", 55).render("Ganador: " + info[0], True, "black")
        else: winner_txt = pygame.font.SysFont("Fira Code", 55).render(info[0], True, "black")

        if info[0] == "Player": srfc_game_over.blit(winner_txt, (380,139))
        if info[0] == "Bot": srfc_game_over.blit(winner_txt, (410,139))
        if info[0] == "Empate": srfc_game_over.blit(winner_txt, (460,139))

        player_points = pygame.font.SysFont("Fira Code", 30).render(str(info[1]), True, "white")
        bot_points = pygame.font.SysFont("Fira Code", 30).render(str(info[2]), True, "white")
        total_player_points = pygame.font.SysFont("Fira Code", 30).render(str(info[3]), True, "white")
        total_bot_points = pygame.font.SysFont("Fira Code", 30).render(str(info[4]), True, "white")

        srfc_game_over.blit(player_points, (390,246))
        srfc_game_over.blit(total_player_points, (390,273))
        srfc_game_over.blit(bot_points, (530,246))
        srfc_game_over.blit(total_bot_points, (530,273))

        screen.blit(srfc_game_over, srfc_game_over_rect)
        screen.blit(play_again_option, play_again_option_rect)
    