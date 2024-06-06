import pygame, sys, random, time
from typing import List

from fondo_singleton.Fondo import Fondo

from tiles.typeTiles.tile import Tile
from tiles.typeTiles.tile_decorator.image_decorator import Image_decorator

from proxy.game import Game
from proxy.proxy_game import Proxy_game

from observer.subscriber_alert import Subsciber_alert
from observer.subscriber_end_game_alert import Subscriber_end_game_alert

from state.access_deneid import Access_deneid
from state.game_over import Game_over
from state.player_need_tiles import Player_need_tiles
from state.pass_turn import Pass_turn


#---------------------- Inicializacion pygame, ventana y atributos
WIDHT = 1800
HEIGHT = 1013

pygame.init()
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption('DOMINO')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Fira code", 30)

#---------------------- Instancia unica del fondo, uso del patrón SINGLETON
fondo = Fondo.get_instance(WIDHT, HEIGHT)

#---------------------- surface muestra opciones si se puede poner ficha en ambos lados
srfc_side_options = pygame.Surface((200, 100))
srfc_side_options_rect = srfc_side_options.get_rect(x=WIDHT/2-100, y=HEIGHT-240) #Rect: Recibe las colisiones

left_side_option = pygame.Surface((70, 30), pygame.SRCALPHA) #pygame.SRCALPHA: permita la opacidad
left_side_option_rect = left_side_option.get_rect(x=srfc_side_options_rect.x+20, y=srfc_side_options_rect.y+57)
right_side_option = pygame.Surface((70, 30), pygame.SRCALPHA)
right_side_option_rect = right_side_option.get_rect(x=srfc_side_options_rect.x+111, y=srfc_side_options_rect.y+57)

#---------------------- rect del boton para jugar de nuevo
srfc_game_over = pygame.Surface((800, 400))
srfc_game_over_rect = srfc_game_over.get_rect(x=(WIDHT-800)//2, y=(HEIGHT-400)//2) #Rect: Recibe las colisiones

play_again_option = pygame.Surface((213, 57), pygame.SRCALPHA) #pygame.SRCALPHA: permita la opacidad
play_again_option_rect = play_again_option.get_rect(x=srfc_game_over_rect.x+295, y=srfc_game_over_rect.y+325)

#---------------------- eventos de tiempo
SET_CENTER_TILE_TIME = pygame.USEREVENT + 1
SET_BOT_TILE_TIME = pygame.USEREVENT + 2
SET_PLAYER_TILE_TIME = pygame.USEREVENT + 3
ALERT_ACCESS_DENIED_TIME = pygame.USEREVENT + 4
PLAYER_NEED_TILES_TIME = pygame.USEREVENT + 5
BOT_NEED_TILES_TIME = pygame.USEREVENT + 6
PASS_TURN_TIME = pygame.USEREVENT + 7

#---------------------- Clase juego, inicilizacion de variables
game = Game(0, 0, SET_CENTER_TILE_TIME)
proxy_game = Proxy_game()

game.create_tiles()
game.distribute_tiles()

#---------------------- ubicar fichas de cada jugador (mano)
def show_hand_tiles(tiles_list:List, height, is_bot):
    pos_width = 190 #diferencia de posiciones de cada ficha en x

    for tile in tiles_list:
        tile:Tile
        if is_bot:
            tile = Image_decorator(tile) #patron DECORATOR, cambia imagen fichas (Se cambia la instancia de la tile en este instante pero despues vuelve a ser normal (Tile))
            
        tile.set_position((WIDHT/2)-pos_width, height) #(x, y)
        tile.set_vertical()

        pos_width -= 55
        if not tile.removed: 
            tile.draw(screen)
            
#---------------------- mostrar fichas jugadas y fichas restantes (Pozo)
def show_tiles():
    game.left_sides = []
    game.right_sides = []

    with_remaining_tiles = 24
    height_remaining_tiles = HEIGHT-148
    for tile in game.remaining_tiles:
        tile = Image_decorator(tile)
        tile.set_image()
        tile.set_position(with_remaining_tiles, height_remaining_tiles)
        tile.set_vertical()

        with_remaining_tiles += 10 
        height_remaining_tiles += 2
        if not tile.removed:
            tile.draw(screen)

    for tile in game.center_tile:
        tile.set_position(WIDHT/2-25, HEIGHT/2-50)
        tile.set_vertical()
        tile.draw(screen)

    if len(game.center_tile) != 0:
        game.left_sides.append(game.center_tile[0].side1)
        game.right_sides.append(game.center_tile[0].side1)

    positions = [WIDHT/2-25, HEIGHT/2-25, "normal"] #[pos x, pos y, "posicion final: (posicion de ficha doble / posicion invertida / posicion normal)"] 
    changed_line = False # saber si ya aso de line del centro a 200 pixeles arriba
    direction = "left"
    for i, tile in  enumerate(game.played_left_tiles):
        # Si la ficha alcanza el limite para seguir poniendo mas, pasan para arriba (width = 200) (y-200), test=715
        if positions[0] <= 200 and not changed_line: 
            changed_line = True
            direction = "right" # ahora las fichas se dibujaran hacia la derecha
            match positions[2]:
                case "double": positions = [positions[0]-55, positions[1]-250, "double"] #positions[0]-55: Es como si la ficha double(vertical) estuviera 55 pixeles atras
                case "reversed": positions = [positions[0]-105, positions[1]-250, "reversed"] #positions[0]-105: Es como si la ficha reversed(horizontal) estuviera 105 pixeles atras
                case "normal": positions = [positions[0]-105, positions[1]-250, "normal"] #positions[0]-105: Es como si la ficha normal(horizontal) estuviera 105 pixeles atras
        
        set_correct_position(tile, game.left_sides, positions, i, direction)
        tile.draw(screen)

    positions = [WIDHT/2-75, HEIGHT/2-25, "normal"]
    changed_line = False
    direction = "right"
    for i, tile in enumerate(game.played_right_tiles):
        # Si la ficha alcanza el limite para seguir poniendo mas, pasan para abajo (x = WIDHT-250) (y+200), test=1085
        if positions[0] >= WIDHT-300 and not changed_line: 
            changed_line = True
            direction = "left"
            match positions[2]:
                case "double": positions = [positions[0]+55, positions[1]+250, "double"]
                case "reversed": positions = [positions[0]+105, positions[1]+250, "reversed"]
                case "normal": positions = [positions[0]+105, positions[1]+250, "normal"] 

        set_correct_position(tile, game.right_sides, positions, i, direction)
        tile.draw(screen)

#---------------------- Ubica las fichas en la posicion correcta en el tablero
def set_correct_position(tile:Tile, list_sides:List, positions:List, cont, side):
    if side ==  "left":
        if tile.side1 == list_sides[cont]: #list_sides[-1] (borrar cont)
            list_sides.append(tile.side2)

            match positions[2]:
                case "normal" | "double": positions[0] -= 55
                case "reversed": positions[0] -= 105

            # Si la ficha es doble
            if tile.side1 == tile.side2: 
                tile.set_position(positions[0], positions[1]-25)
                tile.set_vertical()
                positions[2] = "double"
            else:
                tile.set_position(positions[0], positions[1])
                tile.set_horizontal_reverse()
                positions[2] = "reversed"
        else:
            list_sides.append(tile.side1)

            match positions[2]:
                case "normal" | "double": positions[0] -= 105
                case "reversed": positions[0] -= 155

            tile.set_position(positions[0], positions[1])
            tile.set_horizontal()
            positions[2] = "normal"
    else:
        if tile.side1 == list_sides[cont]:
            list_sides.append(tile.side2)

            match positions[2]:
                case "normal": positions[0] += 105
                case "reversed" | "double": positions[0] += 55

            # Si la ficha es doble
            if tile.side1 == tile.side2: 
                tile.set_position(positions[0], positions[1]-25)
                tile.set_vertical()
                positions[2] = "double"
            else:
                tile.set_position(positions[0], positions[1])
                tile.set_horizontal()
                positions[2] = "normal"
        else:
            list_sides.append(tile.side1)

            match positions[2]:
                case "normal": positions[0] += 155
                case "reversed" | "double": positions[0] += 105

            tile.set_position(positions[0], positions[1])
            tile.set_horizontal_reverse()
            positions[2] = "reversed"

#---------------------- Valida las fichas que se pueden jugar y las que no, las desabilita (baja la opacidad)
def valid_tiles(tiles_list):
    print("\n------Turno " + game.player_turn)
    for tile in tiles_list:
        if not tile.removed:
            tile.print_tile()

    game.can_take_tile = True

    for tile in tiles_list:
        if not tile.removed:
            if tile.side1 == game.left_sides[-1] or tile.side2 == game.left_sides[-1]: 
                print("valid at left")
                tile.print_tile()
                tile.valid_at_left = True
                tile.disable = False
                game.can_take_tile = False

            if tile.side1 == game.right_sides[-1] or tile.side2 == game.right_sides[-1]: 
                print("valid at right")
                tile.print_tile()
                tile.valid_at_right = True
                tile.disable = False
                game.can_take_tile = False
    
    if game.player_turn == "player" and game.can_take_tile:
        proxy_game.player_need_tiles_alert = True
        pygame.time.set_timer(PLAYER_NEED_TILES_TIME, 2000)

#---------------------- valida todas las fichas para que se dejen de ver con opacidad
def reset_tile_values(tiles_list):
    for tile in tiles_list:
        tile.valid_at_left = False
        tile.valid_at_right = False
        tile.disable = True

#---------------------- Jugada del bot
def play_bot():
    pygame.time.set_timer(SET_BOT_TILE_TIME, 0)

    playable_bot_tiles = [tile for tile in game.bot_tiles if not tile.disable]
    if len(playable_bot_tiles) > 0:
        game.player_bot_can_play[1] = True

        tile = random.choice(playable_bot_tiles)

        if tile.valid_at_right:
            game.played_right_tiles.append(tile.clone())
        else:
            game.played_left_tiles.append(tile.clone())

        tile.removed = True
        reset_tile_values(game.bot_tiles)
        if not verify_win(game.bot_tiles):
            game.player_turn = "player"
            game.playing_turn = False
    else:
        print("BOT HAS NOT AVAILABLE TILES")

        available_remaining_tiles = [tile for tile in game.remaining_tiles if not tile.removed]

        if available_remaining_tiles: # devuelve true si la lista no es vacia, si no, devuelve false
            selected_tile = random.choice(available_remaining_tiles)

            print("selected tile from remaining tiles: ")
            selected_tile.print_tile()

            proxy_game.bot_need_tiles_alert = True
            pygame.time.set_timer(BOT_NEED_TILES_TIME, 2000)
            
            add_tile_to_list(game.bot_tiles, selected_tile.clone())
            selected_tile.removed = True
            
            reset_tile_values(game.bot_tiles)
            valid_tiles(game.bot_tiles)
            pygame.time.set_timer(SET_BOT_TILE_TIME, 1000) # un segundo Para que se vuelva a llamar de nuevo la funcion play_bot()
        else:
            print("\nNOT MORE REMAININMG TILES")
            game.player_bot_can_play[1] = False

            if game.player_bot_can_play[0]:
                print("\nSALTO TURNO PLAYER")

                proxy_game.pass_turn = True
                pygame.time.set_timer(PASS_TURN_TIME, 2000)
            else:
                game.finished = True
                
def verify_win(tiles_list):
    total_tiles_not_removed = [tile for tile in tiles_list if not tile.removed]
    if not total_tiles_not_removed:
        print("--------- THE WINNER IS: " + game.player_turn +" (Ultima jugada) ---------")
        game.finished = True
        return True
    return False

#----------------------  verifica si el jugador real perdio
def verify_if_player_lost():
    pygame.time.set_timer(SET_PLAYER_TILE_TIME, 0)

    if not verify_win(game.player_tiles):
        available_remaining_tiles = [tile for tile in game.remaining_tiles if not tile.removed]
        if available_remaining_tiles: # Es true si la lista no es vacia
            game.player_bot_can_play[0] = True
        else:
            print("\nNOT MORE REMAININMG TILES")

            if game.can_take_tile:
                print("\nPLAYER CANT PLAY")
                game.player_bot_can_play[0] = False
                if game.player_bot_can_play[1]:
                    print("\nSALTO TURNO BOT")

                    proxy_game.pass_turn = True
                    pygame.time.set_timer(PASS_TURN_TIME, 2000)
                else:
                    game.finished = True

#---------------------- Añadir ficha tomada de las fichas restantes a la lista del jugador indicado (se agregan en los espacios de las fichas ya jugadas)
def add_tile_to_list(tiles_list:List, new_tile):
    tile_added = False
    for i, tile in enumerate(tiles_list):
        if tile.removed:
            tiles_list[i] = new_tile
            tile_added = True
            break
    
    if not tile_added:
        tiles_list.append(new_tile)

def calculate_points():
    player_points = [tile.side1+tile.side2 for tile in game.player_tiles if not tile.removed]
    bot_points = [tile.side1+tile.side2 for tile in game.bot_tiles if not tile.removed]

    total_player_points = sum(player_points)
    total_bot_points = sum(bot_points)

    if total_player_points < total_bot_points:
        if game.player_turn != "": 
            game.total_player_points += total_bot_points 
        return ["Player", total_bot_points, 0, game.total_player_points, game.total_bot_points]
    elif total_player_points > total_bot_points:
        if game.player_turn != "": 
            game.total_bot_points += total_player_points 
        return ["Bot", 0, total_player_points, game.total_player_points, game.total_bot_points]
    else: 
        if game.player_turn != "": 
            game.total_player_points += total_bot_points 
            game.total_bot_points += total_player_points 
        return ["Empate", total_bot_points, total_player_points, game.total_player_points, game.total_bot_points]

#--------------- Se muestran las fichas de todos
print("\nbot tiles")
for tile in game.bot_tiles:
    tile.print_tile()
print("\nplayer tiles")
for tile in game.player_tiles:
    tile.print_tile()

#-------------------------------------------------------------------- Bucle de juego
# following_mouse = False
# current_tile:Tile = None

while True:
    fondo.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #--------- evento al hacer click en las fichas restantes
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            # print(event.pos)
            selected_tile = None #Ficha seleccionada de las fichas restantes (pozo)
            for tile in game.remaining_tiles:
                if not tile.removed and (tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos)):
                    selected_tile = tile
            
            #--------- Si la ficha fue seleccionada
            if selected_tile != None:
                print("selected tile from remaining tiles: ")
                selected_tile.print_tile()
                if proxy_game.verify_player(game.player_turn) and game.can_take_tile:
                    add_tile_to_list(game.player_tiles, selected_tile.clone())
                    selected_tile.removed = True
                    reset_tile_values(game.player_tiles)
                    valid_tiles(game.player_tiles)
                    verify_if_player_lost()
                else:
                    proxy_game.alert_access_denied_alert = True
                    pygame.time.set_timer(ALERT_ACCESS_DENIED_TIME, 2000)

        #--------- si es el turno del jugador, el proxy le da acceso a las siguientes acciones
        if proxy_game.verify_player(game.player_turn):
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                #---------  Muestra la alerta proxy en caso de pulsar las fichas del bot
                for tile in game.bot_tiles:
                    if not tile.removed and (tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos)):
                        proxy_game.alert_access_denied_alert = True
                        pygame.time.set_timer(ALERT_ACCESS_DENIED_TIME, 2000)

                #--------- registra los clicks en las fichas del jugador
                for tile in game.player_tiles:
                    if not tile.disable and (tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos)):
                        print("valid tile pressed")
                        if tile.valid_at_left and tile.valid_at_right:
                            game.show_side_options = True
                            game.tile_available_both_sides = tile
                        else:
                            if tile.valid_at_left:
                                game.played_left_tiles.append(tile.clone())
                            else:
                                game.played_right_tiles.append(tile.clone())
                            
                            game.show_side_options = False
                            tile.removed = True
                            reset_tile_values(game.player_tiles)
                            if not verify_win(game.player_tiles):
                                game.player_turn = "bot"
                                game.playing_turn = False
                        
            #--------- opcion seleccionada si la ficha se puede poner en ambos lados
            if game.show_side_options and event.type == pygame.MOUSEBUTTONDOWN:
                if left_side_option_rect.collidepoint(event.pos): 
                    game.played_left_tiles.append(game.tile_available_both_sides.clone())
                elif right_side_option_rect.collidepoint(event.pos): 
                    game.played_right_tiles.append(game.tile_available_both_sides.clone())
                
                if left_side_option_rect.collidepoint(event.pos) or right_side_option_rect.collidepoint(event.pos):
                    game.tile_available_both_sides.removed = True
                    game.show_side_options = False
                    reset_tile_values(game.player_tiles)
                    if not verify_win(game.player_tiles):
                        game.player_turn = "bot"
                        game.playing_turn = False
        
        if game.finished and event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and play_again_option_rect.collidepoint(event.pos):
            game = Game(game.total_player_points, game.total_bot_points, SET_CENTER_TILE_TIME)
            game.create_tiles()
            game.distribute_tiles()

            print("\nbot tiles")
            for tile in game.bot_tiles:
                tile.print_tile()
            print("\nplayer tiles")
            for tile in game.player_tiles:
                tile.print_tile()

        #--------- Mover ficha con mouse
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     for tile in game.player_tiles:
        #         if tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos):
        #             if event.button == pygame.BUTTON_LEFT:
        #                 current_tile = tile
        #                 following_mouse = False #----------------------------------------------- Se deja o no?

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     if (event.button == 1):  # Botón izquierdo del mouse
        #         following_mouse = False

        # ---------- Tiempo inicial para poner ficha central
        if event.type == SET_CENTER_TILE_TIME:
            # set_center_tile([game.player_tiles, game.bot_tiles], SET_CENTER_TILE_TIME)
            game.set_center_tile(SET_CENTER_TILE_TIME)
            reset_tile_values(game.bot_tiles)
            reset_tile_values(game.player_tiles)
        
        # ---------- Demora de tiempo para q los jugadores pongan la ficha
        if event.type == SET_BOT_TILE_TIME:
            play_bot()

        if event.type == SET_PLAYER_TILE_TIME:
            valid_tiles(game.player_tiles)
            verify_if_player_lost()

        # ---------- despues de que pasa el tiempo de la alerta activa, se deja de mostrar
        if event.type == ALERT_ACCESS_DENIED_TIME:
            pygame.time.set_timer(ALERT_ACCESS_DENIED_TIME, 0)
            proxy_game.alert_access_denied_alert = False
        
        if event.type == PLAYER_NEED_TILES_TIME:
            pygame.time.set_timer(PLAYER_NEED_TILES_TIME, 0)
            proxy_game.player_need_tiles_alert = False

        if event.type == BOT_NEED_TILES_TIME:
            pygame.time.set_timer(BOT_NEED_TILES_TIME, 0)
            proxy_game.bot_need_tiles_alert = False

        if event.type == PASS_TURN_TIME:
            pygame.time.set_timer(PASS_TURN_TIME, 0)
            proxy_game.pass_turn = False

            if game.player_turn == "player": game.player_turn = "bot"
            else: game.player_turn = "player"

            game.playing_turn = False                   
    
    #--------- End of events
             
    #--------- Mover ficha con mouse
    # if following_mouse:
    #     proxy_game.alert(screen, HEIGHT, WIDHT, Subsciber_alert)

    show_hand_tiles(game.player_tiles, HEIGHT-120, False)
    if not game.finished: show_hand_tiles(game.bot_tiles, 20, True) #True: Para mostrar el decorator de las fichas del bots (Fichas en blanco)
    else: show_hand_tiles(game.bot_tiles, 20, False) 

    show_tiles()  

    #--------- verifica que el jugador o el bot no esten jugando y despues juega el player o el bot
    if not game.playing_turn:
        game.playing_turn = True
        if game.player_turn == "bot":
            valid_tiles(game.bot_tiles)
            pygame.time.set_timer(SET_BOT_TILE_TIME, 1000)
        elif game.player_turn == "player":
            pygame.time.set_timer(SET_PLAYER_TILE_TIME, 1000)

    #--------- mostrar opciones para seleccionar el lado donde poner la ficha
    if game.show_side_options:
        srfc_side_options.blit(pygame.image.load('assets/select_a_side.png'), (0,0))
        left_side_option.fill((0, 0, 0, 0)) # fill(R, G, B, Opacity)
        right_side_option.fill((0, 0, 0, 0))
        screen.blit(srfc_side_options, srfc_side_options_rect)
        screen.blit(left_side_option, left_side_option_rect)
        screen.blit(right_side_option, right_side_option_rect)

    #--------- Mostrar alertas
    if proxy_game.alert_access_denied_alert:
        proxy_game.set_state(Access_deneid())
        proxy_game.alert(screen, WIDHT, HEIGHT-250, Subsciber_alert, "")
    
    # Cuando un jugador no tinene fichas disponibles
    if proxy_game.player_need_tiles_alert:
        proxy_game.set_state(Player_need_tiles())
        proxy_game.alert(screen, WIDHT, HEIGHT-250, Subsciber_alert, "")
    if proxy_game.bot_need_tiles_alert:
        proxy_game.set_state(Player_need_tiles())
        proxy_game.alert(screen, WIDHT, 150, Subsciber_alert, "")

    # Cuando un jugador no tinene fichas disponibles y tampoco puede robar
    if proxy_game.pass_turn:
        proxy_game.set_state(Pass_turn())
        if game.player_turn == "player":
            proxy_game.alert(screen, WIDHT, HEIGHT-250, Subsciber_alert, "")
        else:
            proxy_game.alert(screen, WIDHT, 150, Subsciber_alert, "")
    
    # Cuando gana alguien o hay empate
    if game.finished:
        proxy_game.set_state(Game_over())
        proxy_game.alert(screen, WIDHT, HEIGHT, Subscriber_end_game_alert, calculate_points())

        game.playing_turn = False
        game.player_turn = ""
        
    pygame.display.update()
    clock.tick(60) # fps