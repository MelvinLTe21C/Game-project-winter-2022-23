# import packages and functions to be used
import random
import pygame
from utils.generate_room import roomgeneration
from utils.player import Player
from functions import trap, chest, end_screen, welcome, victory_screen,\
    monster_text_render, stats_text_render, inventory_text_render
import os
from utils.monster import Monster

# set amount of rooms to be create
room_amount = 75

# generate the map, and create a list of rooms created to be able to check if rooms exist later
room_locations = []
map_dict, final_room = roomgeneration(room_amount)
last_room_coords = (final_room.x, final_room.y)

map_dict.get(last_room_coords).contains = None

# add all rooms that exist to the list of room coordinates
for y in range(-10, 10):
    for x in range(-10, 10):
        if (x, y) in map_dict:
            room_locations.append((x, y))

# set the start room to visited, as the game only renders visited rooms as opened
map_dict.get((0, 0)).visited = True

# initiate an instance of the class Player()
player = Player()

# set up booleans and variables to be used later. player_input is the input the player gives,
# player_alive_check is used to check if the player is alive or not.
# The rest are booleans to be used when rendering rooms and fight scenes.
player_input = False
chest_input_bool = False
monster_fight_bool = False
monster_fight_check_bool = None
player_attack_turn = True
player_alive_check = "PLAYERALIVE"

items_to_render = []

# there is of course no monster to start with, so set current_monster
# to None so it can be changed later when encounter happens.
current_monster = None

# initiate and start up pygame, as well as the screen to be used
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# set scale_factor to game will look the same on all screen, set running to True so the game keeps running.
screen_size = pygame.display.get_window_size()
scale_factor = 1920 / screen_size[0]
running = True

# set variables for text rendering. text is the text to be rendered, text_counter is how much of the text should be
# hidden, text_queue is a list of text to be rendered after the current text is done rendering
text = ""
text_counter = 10
text_queue = welcome()

# load fonts
font = pygame.font.Font(os.path.join("fonts", "DeterminationSansWebRegular-369X.ttf"), int(60 * scale_factor))
end_font = pygame.font.Font(os.path.join("fonts", "DeterminationSansWebRegular-369X.ttf"), int(150 * scale_factor))

# load images for all rooms and the player character

intro_outro_room = pygame.image.load(os.path.join("img", "staircase.png"))
intro_outro_room = pygame.transform.scale(intro_outro_room, (250 * scale_factor, 250 * scale_factor))

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

# main loop
while running:
    # reset player input so the same action doesnt keep repeating itself.
    player_input = False
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        # quit the game if player wishes to exit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # close the game when escape is pressed
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            # only take input if no text is to be rendered and player is alive
            if text_counter == 0:
                if player_alive_check == "PLAYERALIVE":
                    # input may be taken even if there is currently dialogue happening.
                    if event.key not in [119, 115, 100, 97]:
                        player_input = event.key
                    if not monster_fight_bool:
                        if not monster_fight_check_bool:
                            # however, movement is not allowed unless there
                            # is currently no dialogue or text to be rendered
                            try:
                                if event.key == 119:
                                    # move up when W is pressed
                                    # save current text variable in another variable as text will be used here
                                    old_text = text
                                    old_text_counter = text_counter
                                    # see player.py for more information
                                    text = player.move("U", map_dict, room_locations)
                                    text_counter = 35
                                    # if the player has already visited the move they just moved into, no further action
                                    # is to be taken, and the text variable can be reset to its value before player.move
                                    if text == "SUCCESS_visited":
                                        text = old_text
                                        text_counter = old_text_counter

                                    # however, if the player has not visited the room, further events will occur.
                                    if text == "SUCCESS_unvisited":
                                        # get the room type/content of the room the player has just entered
                                        room_type = map_dict.get(player.location).contains
                                        if room_type == "trap":
                                            # use trap function from functions.py
                                            text_queue = trap(player)
                                            # set text and text_counter to match
                                            # the first message returned by the trap function.
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                        if room_type == "chest":
                                            # see functions.py for more about chest
                                            # text_queue is a list of messages to be printed
                                            # chest_response is a variable for the chest function to report if the item
                                            # could be added to inventory or if the player will have discard an item
                                            # new_item is the item found in the chest, and 105 is the
                                            # amount of items in the game
                                            text_queue, chest_response, new_item = chest(player, 105)
                                            # same as above, set the text and text_counter to match the first message
                                            # returned by the chest function
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            # "FAILURE_NO_SLOTS indicates that the players inventory is full.
                                            if chest_response == "FAILURE_NO_SLOTS":
                                                # chest_input_bool being set to True will trigger a part of the program
                                                # later that will make the player swap an item in their inventory with
                                                # new_item
                                                chest_input_bool = True
                                        if room_type == "monster":
                                            # if a monster is in the room, create a new instance of the monster class.
                                            # The choice of monster is given by a number between 1 and 13, meaning that
                                            # random.randint(1, 13) will choose a random monster
                                            current_monster = Monster(random.randint(1, 13))
                                            # same as above
                                            text_queue = current_monster.encounter()
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            # this boolean will trigger a part of the program later which will prompt
                                            # the player to decide whether to fight the monster or not
                                            monster_fight_check_bool = True

                                # as all of these are the same as the ones above bar the direction the player moves in,
                                # I will not comment them. Refer to the paragraph above if any questions appear.
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
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop()
                                        if room_type == "chest":
                                            text_queue, chest_response, new_item = chest(player, 105)
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            if chest_response == "FAILURE_NO_SLOTS":
                                                chest_input_bool = True
                                        if room_type == "monster":
                                            current_monster = Monster(random.randint(1, 13))
                                            text_queue = current_monster.encounter()
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            monster_fight_check_bool = True

                                # identical to the ones above bar direction
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
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)

                                        if room_type == "chest":
                                            text_queue, chest_response, new_item = chest(player, 105)
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            if chest_response == "FAILURE_NO_SLOTS":
                                                chest_input_bool = True

                                        if room_type == "monster":
                                            current_monster = Monster(random.randint(1, 13))
                                            text_queue = current_monster.encounter()
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            monster_fight_check_bool = True

                                # identical to the ones above bar direction
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
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                        if room_type == "chest":
                                            text_queue, chest_response, new_item = chest(player, 105)
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            if chest_response == "FAILURE_NO_SLOTS":
                                                chest_input_bool = True
                                        if room_type == "monster":
                                            current_monster = Monster(random.randint(1, 13))
                                            text_queue = current_monster.encounter()
                                            text = text_queue[0]
                                            text_counter = len(text_queue[0])
                                            text_queue.pop(0)
                                            monster_fight_check_bool = True

                            # AttributeError will occur when the player tries to walk off the map.
                            # If this happens, text is changed to a message telling the player not to
                            # walk in said direction. Using a try/except method here guarantees that the player cannot
                            # walk off the map, and guarantees that the game cannot intentionally be crashed by someone
                            # attempting to walk off the map
                            except AttributeError:
                                text = "You cannot walk in that direction."

    # render all of the rooms, player.location +- 6 are how many rooms behind and in front of the one the player is
    # currently in should be rendered as rendering too many rooms will cause performance issues on slower computers.
    for x in range(player.location[0] - 6, player.location[0] + 6):
        # render distance can be lower vertically as rooms are square, but the screen is rectangular (16:9)
        for y in range(player.location[1] - 4, player.location[1] + 3):
            # only render the room if it exists, and if it exists it is in room_locations
            if (x, y) in room_locations:
                # room needs to be extracted as information is to grabbed from the instance of the class Room
                # that map_dict contains
                room = map_dict.get((x, y))
                # if the room has not been visited, its contents will be hidden
                if not room.visited:
                    screen.blit(unvisited_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                # if the room has been visited by the player, its contents will be revealed
                else:
                    if (x, y) == last_room_coords:
                        # if the room is the final room, intro_outro_room will be used.
                        # x - player-location[0] and y - player.location[1] give the rooms coordinates compared to the
                        # players current room, meaning that the room behind the one the player is in will its x value
                        # -1 * 350 (the width of a room + 50 for visual clarity) + 835(1920/2 - room width), also the
                        # x coordinate of the room the player is in as that rooms value will be 0 * 350 + 835.
                        # this entire value is set for 1920x1080 screens, but multiplying it by scale_factor means that
                        # the value will be the same relative to screen size on all screens. The 0.85 value sets the
                        # size of the room, and can be changed for aesthetic purposes, however 0.85 seems a good
                        # compromise between looks and not being to small that you cannot see what is happening.
                        # The Y value works the same, with the only difference being that its start value for the
                        # players current room being 415.
                        screen.blit(intro_outro_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains == "monster":
                        # X and Y coords are the same as above, but monster_room image is used in monster room
                        screen.blit(monster_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains == "chest":
                        # here, chest image is used
                        screen.blit(chest_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains == "trap":
                        # and here, the trap image is used
                        screen.blit(trap_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))
                    elif room.contains is None:
                        # the only room to contain None is (0, 0) which is the start room, meaning that intro_outro_room
                        # image is to be used here
                        screen.blit(intro_outro_room, (((x - player.location[0]) * 350 + 835) * (scale_factor * 0.85),
                                    ((y - player.location[1]) * 350 + 415) * (scale_factor * 0.85)))

    # this part of code will be triggered if monster_fight_check_bool has been set to True, meaning that player needs
    # to make a decision if they want to fight a given monster.
    if monster_fight_check_bool:
        # only continue if player_input is a value that does something in this instance
        if player_input in range(49, 51):
            # choosing 2 (which has the PyGame key code of 50) means that the player wishes to fight the monster.
            # therefore, monster_fight_bool is set to True, to indicate that the player is currently fighting a monster.
            # monster_fight_check_bool is set to None as there is currently no such dialogue needed.
            # player_attack_turn is set to True as the player always attacks first, and if player_attack_turn is True,
            # it is the players turn to attack.
            if player_input == 50:
                monster_fight_bool = True
                monster_fight_check_bool = None
                player_attack_turn = True
            # choosing 1 (PyGame keycode 49) means that the player wants to run from the monster
            elif player_input == 49:
                # player.detect_doors() will return a list of booleans indicating if there are rooms around the room
                # the player is currently in
                doors = player.detect_doors(room_locations)
                # set room_found to False as the code will otherwise stop looking for rooms to move the player into.
                room_found = False
                # the first item in the list doors will say if there is a room or not on the left of the player,
                # expressed as a boolean. If there is, the boolean is True, and the code below will run
                if doors[0]:
                    # check if the room the player is attempting move into has been visited,
                    # as the player may only flee to rooms they've previously visited
                    if map_dict.get(tuple([player.location[0] - 1, player.location[1]])).visited:
                        # set the room the player is currently in (the one with the monster) to unvisited,
                        # as the player has not fully explored it
                        map_dict.get(player.location).visited = False
                        # move the player into the room to the left of its current coordinates
                        player.move("L", map_dict, room_locations)
                        # room has been found, so there is no need to keep looking for a room
                        room_found = True
                # only keep searching if room has not yet been found
                if not room_found:
                    # same as above, only that the direction being looked at is up instead of left
                    if doors[1]:
                        if map_dict.get(tuple([player.location[0], player.location[1] - 1])).visited:
                            map_dict.get(player.location).visited = False
                            player.move("U", map_dict, room_locations)
                            room_found = True
                if not room_found:
                    # now look if the room on the right fits requirements for the player being able to escape in there
                    if doors[2]:
                        if map_dict.get(tuple([player.location[0] + 1, player.location[1]])).visited:
                            map_dict.get(player.location).visited = False
                            player.move("R", map_dict, room_locations)
                            room_found = True
                if not room_found:
                    # finally, check the left
                    if doors[3]:
                        if map_dict.get(tuple([player.location[0], player.location[1] + 1])).visited:
                            map_dict.get(player.location).visited = False
                            player.move("D", map_dict, room_locations)
                            room_found = True
                if room_found:
                    # add messages to be shown to text_queue if a room was found, and set monster_fight_check_bool to
                    # None as the player has escaped, and there is no longer dialogue to be had
                    text_queue.append("You barely fled away from the monsters grasp.          ")
                    text_queue.append("However, he may still lurk in the dark...          ")
                    text_queue.append("Do not return until you are ready to fight the beast.          ")
                    monster_fight_check_bool = None
                else:
                    # there should be no way for the player to get into a room without having visited a room next to it.
                    # If this edge case occurs, something else has gone wrong, and it is best that the game is shut down
                    # with a ValueError to avoid further weird behaviors.
                    raise ValueError("Something has gone wrong. Please restart the game.")

    # this segment kicks in if the player chooses to fight a monster they encounter.
    elif monster_fight_bool:
        # segment belows runs if it is the players turn to attack (if player_attack_turn is True)
        if player_attack_turn:
            # the player may choose between 3 different attacks, which are chosen by pressing 1, 2 or 3 (PyGame keycodes
            # 49, 50, 51. 1 Is regular attack, 2 is a weapon throw dealing extra damage but getting rid of your on hand
            # weapon, and 3 is an attack dealing more damage but also damaging you and permanently reducing your max hp
            # by five. After the attack is finishes, player_attack_turn is set to False, meaning it is the monsters
            # turn to attack
            if player_input in range(49, 52):
                if player_input == 49:
                    text_queue = player.attack(current_monster)
                    player_attack_turn = False
                if player_input == 50:
                    text_queue = player.throw_weapon(current_monster)
                    player_attack_turn = False
                if player_input == 51:
                    text_queue = player.soul_strike(current_monster)
                    player_attack_turn = False
        # this runs if player_attack_turn is False (its the monsters turn to attack)
        else:
            if text_counter == 0:
                # the monster will only attack once the players
                if not text_queue:
                    # the monster attacks, messages are added to text_queue and it becomes the players turn to attack.
                    # text_queue also appends a message informing players what their attack options are
                    text_queue = current_monster.attack(player)
                    text_queue.append("Press 1 to attack, 2 to throw your weapon or 3 to demon strike.          ")
                    player_attack_turn = True
    elif chest_input_bool:
        # if the chest message deems that there is no place in inventory for the new item, the player chooses an item
        # to discard from inventory to remove in favor of the new item. Only accepts inputs in the range 1-5 as those
        # are the only inventory slots possible-
        if player_input in range(49, 55):
            # player.change_inventory_slot() returns the item that used to be in the slot now freed up so it can be
            # shown in a message
            old_item = player.change_inventory_slot(new_item, player_input - 48)
            # this error code will be returned if the player chooses a slot that does not exist.
            if old_item != "SLOT_DOES_NOT_EXIST":
                # append said messages to text_queue
                text_queue.append(old_item.name + " has been discarded.          ")
                text_queue.append(new_item.name + " has been added to inventory.          ")
                # indicate that the chest input part of the loop is done for now
                chest_input_bool = False
            else:
                text_queue.append("There is not item in that inventory slot. Try again.          ")
    # if none of the conditions above are true, the player is currently not in a dialogue or fight, and may therefore
    # change their on hand weapon freely, as well as drink potions.
    else:
        # try/except to make sure that the player cannot choose an item not in their inventory
        try:
            # only accept input in the acceptable range (1-5)
            if player_input in range(49, 55):
                # check if the chosen item is a potion
                if player.inventory[player_input - 49].type == "potion":
                    # if it is, consume it to restore health to the player character
                    player.consume(player_input - 48)
                else:
                    # if it is not, change player.on_hand to the item
                    # (which must be a weapon due to it not being a potion.)
                    player.change_weapon(player_input - 48)
        # the error which would be raised should the player choose an item outside the inventory
        except IndexError:
            pass

    # generate text box, handle text showcasing

    pygame.draw.rect(screen, (220, 220, 220), ((210 * scale_factor, 670 * scale_factor), (1500 * scale_factor, 350 * scale_factor)), width=10)

    # draw the line to separate the text box into text and stats
    pygame.draw.line(screen, (220, 220, 220), (210 * scale_factor, 845 * scale_factor), (1705 * scale_factor, 845 * scale_factor), width=10)

    # render and blit the stats
    stats_text_render(screen, font, player, scale_factor, map_dict)

    pygame.draw.rect(screen, (220, 220, 220), ((1260 * scale_factor, 100 * scale_factor), (550, 500)), width=10)

    # render and blit inventory if you are not fighting a monster as those take the same space on the screen
    if not monster_fight_bool:
        inventory_text_render(screen, font, player, items_to_render, scale_factor)

    else:
        # render the monsters name, health and strength as well as possible attacks if you are in a fight
        monster_text_render(screen, font, current_monster, scale_factor)

    # render text if no more new letters are to be added to the current text.
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

    # if there are still letters/signs to be unhidden, show one. This gives the effect of the text "creeping" onto
    # the screen, which is an aesthetically nice fit for the game
    elif text_counter > 0:
        text_to_render = text[:-text_counter]
        text_rendered = font.render(text_to_render, True, (255, 255, 255))
        text_counter -= 1

    # blit the text rendered by the part of the program above to the screen in a set location.
    screen.blit(text_rendered, (250 * scale_factor, 700 * scale_factor))

    # blit the player image. As the room that player is in will always have the same coordinates, so will the player.
    screen.blit(player_image, (835 * (scale_factor * 0.85), 415 * (scale_factor * 0.85)))

    # check the health of the monster, if there is one. If the monster has had its health reduced below zero, set the
    # current_monster to None as there is no longer a monster. Also increase the player level by one, as theyve slain
    # a monster. It is also here that monsters with the enrage effect detect the enragement, and have their attack
    # increased accordingly
    if current_monster is not None:
        item_to_append_to_text_queue, monster_alive_check = current_monster.update()
        if item_to_append_to_text_queue:
            text_queue.append(item_to_append_to_text_queue)
        if monster_alive_check == "MONSTERDEAD":
            player.level += 1
            monster_fight_bool = False
            current_monster = None

    # check if the players health has went below zero, or if their current coordinates match those of the final room
    # if health is <= 0, the function returns "PLAYERDEAD", if the player has reached the final room, it returns
    # "PLAYERESCAPED"
    player_alive_check = player.update_stats(last_room_coords)
    # only do an endscreen if there is no more text to be rendered.
    if text_counter == 0:
        if not text_queue:
            # play the victory screen if the player escaped
            if player_alive_check == "PLAYERESCAPED":
                victory_screen(screen, end_font, font, scale_factor)
            # play the loss screen if they player died.
            if player_alive_check == "PLAYERDEAD":
                end_screen(screen, end_font, font, scale_factor)

    # update the diaplay with all of the things that were blitted onto the canvas above, and set FPS with clock.tick().
    # FPS is important to the game, as it regulates the speed at which the text moves. The best results are reached
    # around 15-20 fps, as it gives the text a slot but not boring crawl.
    pygame.display.flip()
    clock.tick(15)
