import pygame, sys, random, time
from typing import List

from tiles.factory.simpleTileFactory import SimpleTileFactory
from tiles.factory.doubleTileFactory import DoubleTileFactory
#from tiles.typeTiles.simpleTile import SimpleTile
from tiles.typeTiles.doubleTile import DoubleTile
from tiles.typeTiles.tile import Tile
from tiles.typeTiles.tile_decorator.image_decorator import Image_decorator
from fondo_singleton.Fondo import Fondo
from tiles.proxy.game import Game
from tiles.proxy.proxy_game import Proxy_game


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

#---------------------- eventos de tiempo
SET_CENTER_TILE_TIME = pygame.USEREVENT + 1
SET_BOT_TILE_TIME = pygame.USEREVENT + 2
SHOW_ALERT_TIME = pygame.USEREVENT + 3

#---------------------- Clase juego, inicilizacion de variables
game = Game(SET_CENTER_TILE_TIME)
proxy_game = Proxy_game()

#---------------------- Seteo de fichas, implementacion PATRON ABSTRACT FACTORY, y PATRON PROTOTYPE
simpleFactory = SimpleTileFactory()
doubleFactory = DoubleTileFactory()

simpleTile = simpleFactory.create_tile(0, 1)
doubleTile = doubleFactory.create_tile(0)

for i in range(0, 7):
    for j in range(i, 7):
        cloned_tile: Tile
        if i != j:
            cloned_tile = simpleTile.clone()
        else:
            cloned_tile = doubleTile.clone()
        
        cloned_tile.side1 = i
        cloned_tile.side2 = j
        cloned_tile.set_image()
        game.total_tiles.append(cloned_tile)

#----------------------Reparticion de fichas: tanto el juagdor como el bot cogen fichas de la lista de fichas restantes (lista, cantidad de fichas a coger)
game.remaining_tiles = game.total_tiles.copy()

def take_tiles(list: List, tiles_to_take):
    for i in range(tiles_to_take):
        random_tile = random.randint(0, len(game.remaining_tiles)-1)
        list.append(game.remaining_tiles.pop(random_tile))

#------- Verificar si hay una ficha doble, si no, vuelve a repartir fichas
there_is_double = False
while not there_is_double: 
    print("\nReparticion")
    game.player_tiles = []
    game.bot_tiles = []
    take_tiles(game.player_tiles, 7)
    take_tiles(game.bot_tiles, 7)
    for tiles_list in [game.player_tiles, game.bot_tiles]:
        for tile in tiles_list:
            if tile.is_class(DoubleTile):
                there_is_double = True
    if not there_is_double: print("No doble")

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
            
#---------------------- mostrar fichas jugadas 
def show_tiles():
    game.left_sides = []
    game.right_sides = []

    with_remaining_tiles = 10
    for tile in game.remaining_tiles:
        tile = Image_decorator(tile)
        tile.set_image()
        tile.set_position(with_remaining_tiles, HEIGHT-110)
        tile.set_vertical()

        with_remaining_tiles += 10 
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
    for i, tile in  enumerate(game.played_left_tiles):
        set_correct_position(tile, game.left_sides, positions, i, "left")
        tile.draw(screen)

    positions = [WIDHT/2-75, HEIGHT/2-25, "normal"]
    for i, tile in enumerate(game.played_right_tiles):
        set_correct_position(tile, game.right_sides, positions, i, "right")
        tile.draw(screen)

#---------------------- Ubica las fichas en la posicion correcta en el tablero
def set_correct_position(tile:Tile, list_sides:List, positions:List, cont, side):
    if side ==  "left":
        if tile.side1 == list_sides[cont]: #list_sides[-1] (borrar cont)
            list_sides.append(tile.side2)

            match positions[2]:
                case "normal" | "double": positions[0] -= 55
                case "reversed": positions[0] -= 105

            #--- Si la ficha es doble
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

            #--- Si la ficha es doble
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
   
#---------------------- ubicar la ficha inicial (central)
def set_center_tile(tiles_list):
    pygame.time.set_timer(SET_CENTER_TILE_TIME, 0) #detine el evento (0), para que se deje de llamar
    tile_center:Tile
    biggest_center = 0

    for list in tiles_list:
        for i in range(7):
            for tile in list:
                if tile.is_class(DoubleTile) and tile.side1 == i and i > biggest_center:
                    biggest_center = i
                    tile_center = tile
                    break

    game.center_tile.append(tile_center.clone())

    for j in range(2):
        for tile in tiles_list[j]:
            if tile == tile_center:
                if j == 0: game.player_turn = "bot"
                else: game.player_turn = "player"
                tile.removed = True

    game.playing_turn = False

#---------------------- Valida las fichas que se pueden jugar y las que no, las desabilita (baja la opacidad)
def valid_tiles(tiles_list):
    print("\n------Turno " + game.player_turn)
    game.can_take_tile = True

    for tile in tiles_list:
        tile.disable = True
        if not tile.removed:
            if tile.side1 == game.left_sides[-1] or tile.side2 == game.left_sides[-1]: 
                print("valid at left")
                tile.printTile()
                tile.valid_at_left = True
                tile.disable = False
                game.can_take_tile = False

            if tile.side1 == game.right_sides[-1] or tile.side2 == game.right_sides[-1]: 
                print("valid at right")
                tile.printTile()
                tile.valid_at_right = True
                tile.disable = False
                game.can_take_tile = False

#---------------------- valida todas las fichas para que se dejen de ver con opacidad
def reset_tile_values(tiles_list):
    for tile in tiles_list:
        tile.valid_at_left = False
        tile.valid_at_right = False
        tile.disable = False

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
        if not verify_win(game.bot_tiles):
            game.player_turn = "player"
            game.playing_turn = False
    else:
        print("BOT HAS NOT AVAILABLE TILES")
        available_remaining_tiles = [tile for tile in game.remaining_tiles if not tile.removed]

        if available_remaining_tiles: # devuelve true si la lista no es vacia, si no, devuelve false
            tile = random.choice(available_remaining_tiles)

            print("selected tile from remaining tiles: ")
            tile.printTile()

            game.bot_tiles.append(tile.clone())
            tile.removed = True
            
            reset_tile_values(game.bot_tiles)
            valid_tiles(game.bot_tiles)
            pygame.time.set_timer(SET_BOT_TILE_TIME, 1000)
        else:
            print("\nNOT MORE REMAININMG TILES")
            game.player_bot_can_play[1] = False

            if game.player_bot_can_play[0]:
                print("\nSALTO TURNO PLAYER")
                game.player_turn = "player"
                game.playing_turn = False
            else:
                game.finished = True
                
def verify_win(tiles_list):
    total_tiles_not_removed = [tile for tile in tiles_list if not tile.removed]
    if not total_tiles_not_removed:
        print("--------- THE WINNER IS: " + game.player_turn +" ---------")
        game.finished = True
        return True
    return False

def verify_if_player_lost():
    if not verify_win(game.player_tiles):
        available_remaining_tiles = [tile for tile in game.remaining_tiles if not tile.removed]
        if available_remaining_tiles: # Es false si la lista es vacia
            game.player_bot_can_play[0] = True
        else:
            print("\nNOT MORE REMAININMG TILES")
            game.player_bot_can_play[0] = False

            if game.can_take_tile:
                print("\nPLAYER CANT PLAY")
                if game.player_bot_can_play[1]:
                    print("\nSALTO TURNO BOT")
                    game.player_turn = "bot"
                    game.playing_turn = False
                else:
                    game.finished = True
    
#---------------
print("\nbot tiles")
for tile in game.bot_tiles:
    tile.printTile()
print("player tiles")
for tile in game.player_tiles:
    tile.printTile()

#-------------------------------------------------------------------- Bucle de juego
following_mouse = False
current_tile:Tile = None

while True:
    fondo.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #--------- evento al hacer click en las fichas restantes
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            selected_tile = None
            for tile in game.remaining_tiles:
                if not tile.removed and (tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos)):
                    selected_tile = tile
            
            #--------- Si la ficha fue seleccionada
            if selected_tile != None:
                print("selected tile from remaining tiles: ")
                selected_tile.printTile()
                if proxy_game.verify_player(game.player_turn) and game.can_take_tile:
                    game.player_tiles.append(selected_tile.clone())
                    selected_tile.removed = True
                    valid_tiles(game.player_tiles)
                    verify_if_player_lost()
                else:
                    proxy_game.show_alert = True
                    pygame.time.set_timer(SHOW_ALERT_TIME, 2000)

        #--------- si es el turno del jugador, el proxy le da acceso a las siguientes acciones
        if proxy_game.verify_player(game.player_turn):
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                #---------  Muestra la alerta proxy en caso de pulsar las fichas del bot
                for tile in game.bot_tiles:
                    if not tile.removed and (tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos)):
                        proxy_game.show_alert = True
                        pygame.time.set_timer(SHOW_ALERT_TIME, 2000)

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

        #--------- Mover ficha con mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in game.player_tiles:
                if tile.rect1.collidepoint(event.pos) or tile.rect2.collidepoint(event.pos):
                    if event.button == pygame.BUTTON_LEFT:
                        current_tile = tile
                        following_mouse = False #----------------------------------------------- Se deja o no?

        elif event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1):  # Botón izquierdo del mouse
                following_mouse = False

        # ---------- Tiempo inicial para poner ficha central
        if event.type == SET_CENTER_TILE_TIME:
            set_center_tile([game.player_tiles, game.bot_tiles])
        
        # ---------- Demora de tiempo para q el bot ponga la ficha
        if event.type == SET_BOT_TILE_TIME:
            play_bot()

        # ---------- despues de que pasa el tiempo de la alerta activa, se deja de mostrar
        if event.type == SHOW_ALERT_TIME:
            pygame.time.set_timer(SHOW_ALERT_TIME, 0)
            proxy_game.show_alert = False
    
    #--------- End of events
             
    #--------- Mover ficha con mouse
    if following_mouse:
        proxy_game.alert(screen, HEIGHT, WIDHT)

    show_hand_tiles(game.player_tiles, HEIGHT-120, False)
    show_hand_tiles(game.bot_tiles, 20, True)  

    show_tiles()  

    #--------- verifica que el jugador o el bot no esten jugando y despues juega el player o el bot
    if not game.playing_turn:
        game.playing_turn = True
        if game.player_turn == "bot":
            valid_tiles(game.bot_tiles)
            pygame.time.set_timer(SET_BOT_TILE_TIME, 1000)
        elif game.player_turn == "player":
            valid_tiles(game.player_tiles)
            verify_if_player_lost()

    #--------- mostrar opciones para seleccionar el lado donde poner la ficha
    if game.show_side_options:
        srfc_side_options.blit(pygame.image.load('assets/select_a_side.png'), (0,0))
        left_side_option.fill((0, 0, 0, 0)) # fill(R, G, B, Opacity)
        right_side_option.fill((0, 0, 0, 0))
        screen.blit(srfc_side_options, srfc_side_options_rect)
        screen.blit(left_side_option, left_side_option_rect)
        screen.blit(right_side_option, right_side_option_rect)

    if proxy_game.show_alert:
        proxy_game.alert(screen, WIDHT, HEIGHT)
        
    if game.finished:
        print("--------- THE GAME HAS FINISHED ---------")
        game.finished = False
        game.playing_turn = False
        game.player_turn = ""
        
    pygame.display.update()
    clock.tick(60) # fps