import pygame
from utils.generate_room import roomgeneration
from utils.item import Item
from utils.player import Player
from functions import trap, chest, end_screen, welcome
import os


room_amount = 75

room_locations = []
map_dict, final_room = roomgeneration(room_amount)
last_room_coords = (final_room.x, final_room.y)

map_dict.get(last_room_coords).contains = None

for y in range(-10, 10):
    for x in range(-10, 10):
        if (x, y) in map_dict:
            room_locations.append((x, y))

map_dict.get((0, 0)).visited = True

player = Player()

player_input = []
chest_input_bool = False
monster_fight_bool = False

items_to_render = []

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))

screen_size = pygame.display.get_window_size()
scale_factor = 1920 / screen_size[0]
running = True

text = ""
text_counter = 23
text_queue = welcome()

font = pygame.font.Font(os.path.join("fonts", "DeterminationSansWebRegular-369X.ttf"), int(60 * scale_factor))
end_font = pygame.font.Font(os.path.join("fonts", "DeterminationSansWebRegular-369X.ttf"), int(150 * scale_factor))

rock_room = pygame.image.load(os.path.join("img", "ROCK.gif"))
rock_room = pygame.transform.scale(rock_room, (250 * scale_factor, 250 * scale_factor))

monster_room = pygame.image.load(os.path.join("img", "monster_room.png"))
monster_room = pygame.transform.smoothscale(monster_room, (250 * scale_factor, 250 * scale_factor))

trap_room = pygame.image.load(os.path.join("img", "trap_room.png"))
trap_room = pygame.transform.smoothscale(trap_room, (250 * scale_factor, 250 * scale_factor))

chest_room = pygame.image.load(os.path.join("img", "chest_room.png"))
chest_room = pygame.transform.smoothscale(chest_room, (250 * scale_factor, 250 * scale_factor))

unvisited_room = pygame.image.load(os.path.join("img", "unvisited_room.png"))
unvisited_room = pygame.transform.smoothscale(unvisited_room, (250 * scale_factor, 250 * scale_factor))

player_image = pygame.image.load(os.path.join("img", "player_image.png"))
player_image = pygame.transform.smoothscale(player_image, (250 * scale_factor, 250 * scale_factor))

while running:
    player_input = False
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if text_counter == 0:
                try:
                    if event.key == 119:
                        old_text = text
                        old_text_counter = text_counter
                        text = player.move("U", map_dict, room_locations)
                        text_counter = 35
                        if text == "SUCCESS_visited":
                            text = old_text
                            text_counter = old_text_counter

                        if text == "SUCCESS_unvisited":
                            room_type = map_dict.get(player.location).contains
                            if room_type == "trap":
                                text_queue = trap(player)
                            if room_type == "chest":
                                pass
                            if room_type == "monster":
                                pass

                    elif event.key == 115:
                        old_text = text
                        old_text_counter = text_counter
                        text = player.move("D", map_dict, room_locations)
                        text_counter = 35
                        if text == "SUCCESS_visited":
                            text = old_text
                            text_counter = old_text_counter

                        if text == "SUCCESS_unvisited":
                            room_type = map_dict.get(player.location).contains
                            if room_type == "trap":
                                text_queue = trap(player)
                            if room_type == "chest":
                                pass
                            if room_type == "monster":
                                pass

                    elif event.key == 100:
                        old_text = text
                        old_text_counter = text_counter
                        text = player.move("R", map_dict, room_locations)
                        text_counter = 35
                        if text == "SUCCESS_visited":
                            text = old_text
                            text_counter = old_text_counter

                        if text == "SUCCESS_unvisited":
                            room_type = map_dict.get(player.location).contains
                            if room_type == "trap":
                                text_queue = trap(player)
                            if room_type == "chest":
                                pass
                            if room_type == "monster":
                                pass

                    elif event.key == 97:
                        old_text = text
                        old_text_counter = text_counter
                        text = player.move("L", map_dict, room_locations)
                        text_counter = 35
                        if text == "SUCCESS_visited":
                            text = old_text
                            text_counter = old_text_counter

                        if text == "SUCCESS_unvisited":
                            room_type = map_dict.get(player.location).contains
                            if room_type == "trap":
                                text_queue = trap(player)
                                text = text_queue[0]
                                text_queue.pop(0)
                            if room_type == "chest":
                                text_queue, chest_response, new_item = chest(player, 3)
                                text = text_queue[0]
                                text_queue.pop(0)
                                if chest_response == "FAILURE_NO_SLOTS":
                                    chest_input_bool = True
                            if room_type == "monster":
                                pass

                    else:
                        player_input = event.key

                except AttributeError:
                    text = "You cannot walk in that direction."

    for x in range(player.location[0] - 6, player.location[0] + 6):
        for y in range(player.location[1] - 4, player.location[1] + 3):
            if (x, y) in room_locations:
                room = map_dict.get((x, y))
                if not room.visited:
                    screen.blit(unvisited_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                else:
                    if (x, y) == last_room_coords:
                        screen.blit(rock_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains == "monster":
                        screen.blit(monster_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains == "chest":
                        screen.blit(chest_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains == "trap":
                        screen.blit(trap_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains is None:
                        screen.blit(rock_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))

    # take and handle input
    if chest_input_bool:
        if player_input in range(49, 55):
            old_item = player.change_inventory_slot(new_item, player_input - 48)
            text_queue.append(old_item.name + " has been discarded.          ")
            text_queue.append(new_item.name + " has been added to inventory.          ")
            chest_input_bool = False
    else:
        try:
            if player_input in range(49, 55):
                if player.inventory[player_input - 49].type == "potion":
                    player.consume(player_input - 48)
                else:
                    print("SWWAAAAPAPP")
                    player.change_weapon(player_input - 48)
        except IndexError:
            pass

    # generate text box, handle text showcasing

    pygame.draw.rect(screen, (220, 220, 220), ((210 * scale_factor, 670 * scale_factor), (1500 * scale_factor, 350 * scale_factor)), width=10)

    # draw the line to separate the text box into text and stats
    pygame.draw.line(screen, (220, 220, 220), (210 * scale_factor, 845 * scale_factor), (1705 * scale_factor, 845 * scale_factor), width=10)

    # render and blit the stats
    hp_text = font.render("HP: " + str(player.health), True, (255, 0, 0))
    level_text = font.render("Level: " + str(player.level), True, (0, 0, 255))
    strength_text = font.render("Strength: " + str(player.strength), True, (0, 255, 0))
    rooms_explored = font.render("Rooms explored: " + str(player.count_explored_rooms(map_dict)), True, (255, 255, 255))
    on_hand_text = font.render("On hand: " + player.on_hand.name.replace('"', ""), True, (255, 255, 255))

    screen.blit(hp_text, (250 * scale_factor, 865 * scale_factor))
    screen.blit(strength_text, (832 * scale_factor, 865 * scale_factor))
    screen.blit(level_text, (1492 * scale_factor, 865 * scale_factor))
    screen.blit(rooms_explored, ((640 - rooms_explored.get_size()[0] / 2) * scale_factor, 938 * scale_factor))
    screen.blit(on_hand_text, ((1280 * scale_factor) - on_hand_text.get_size()[0] / 2, 938 * scale_factor))

    # render the box in which inventory and monsters are shown

    pygame.draw.rect(screen, (220, 220, 220), ((1260 * scale_factor, 100 * scale_factor), (450, 500)), width=10)

    # render and blit inventory if you are not fighting a monster as those take the same space on the screen
    if not monster_fight_bool:
        inventory_text = font.render("Inventory:", True, (255, 255, 255))
        for item_to_render in player.inventory:
            new_item_to_render = font.render(item_to_render.name.replace('"', ""), True, (255, 255, 255))
            items_to_render.append(new_item_to_render)

        for item_to_render in range(len(items_to_render)):
            screen.blit(items_to_render[0], (1300 * scale_factor, ((180 + 80 * item_to_render) * scale_factor)))
            items_to_render.pop(0)

        screen.blit(inventory_text, (1300 * scale_factor, 120 * scale_factor))

    else:
        pass

    # render text if no more new letters are to be added,
    # change the text variable to the first item in text_queue if current text variable is done rendering.
    if text_counter == 0:
        if not text_queue:
            text_rendered = font.render(text, True, (255, 255, 255))
        else:
            text_rendered = font.render(text, True, (255, 255, 255))
            if text_queue[0] != "Please select an item to remove from the inventory.          ":
                text_counter = len(text_queue[0])
            text = text_queue[0]
            text_queue.pop(0)

    elif text_counter > 0:
        text_to_render = text[:-text_counter]
        text_rendered = font.render(text_to_render, True, (255, 255, 255))
        text_counter -= 1

    screen.blit(text_rendered, (250 * scale_factor, 700 * scale_factor))

    screen.blit(player_image, (835 * (scale_factor * 0.85), 415 * (scale_factor * 0.85)))

    player_alive_check = player.update_stats()
    if player_alive_check == "PLAYERDEAD":
        if text_counter == 0:
            if not text_queue:
                end_screen(screen, end_font, font, scale_factor)

    pygame.display.flip()
    clock.tick(30)
