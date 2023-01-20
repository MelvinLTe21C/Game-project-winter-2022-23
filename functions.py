import random
from utils.item import Item


def welcome():
    # list of messages to be shown at the start of a game, introducing the story and controls.
    return_list = ["You wake up in a mysterious dungeon.          ",
                   "As you look around, you spot different pathways.          ",
                   "Somewhere there must be an exit.          ",
                   "You must find it before it's too late.          ",
                   "Press W, A, S or D to move around.          ",
                   "You may either consume or equip items in your inventory          ",
                   "By pressing the number corresponding to the items position.          ",
                   "There are many mysterious treasures down here,          ",
                   "But also dangerous traps and monsters.          ",
                   "Move carefully. Good luck, explorer.          "]
    return return_list


# All traps


def snake_trap(player):
    # randomize an amount of damage, deal it to the player and send back a series of text messages indicating
    # what happened, as well as health lost, and if the player was killed, a message about the snakes overwhelming
    # the player
    return_list = ["You hear hissing from the wall.          ",
                   "Poisonous snakes meander through reaching for your soul.          ",
                   "You’ve got caught in a [SNAKE TRAP].          "]
    healthloss = random.randint(7, 18)
    player.health = player.health - healthloss
    if player.health > 0:
        return_list.append("You managed to escape the trap.          ")
        return_list.append("But lost " + str(healthloss) + " health points during the action.          ")
    else:
        return_list.append("The snakes overwhelmed you.          ")

    return return_list


def spike_trap(player):
    # same as snake_trap(), but with different pieces of text and different damage values.
    return_list = ["You hear the ground tumbling beneath you.          ",
                   "Sharp spears appear through the ground.          ",
                   "You’ve got caught in a [SPIKE TRAP].          "]
    healthloss = random.randint(6, 22)
    player.health = player.health - healthloss
    if player.health > 0:
        return_list.append("You managed to escape the trap.          ")
        return_list.append("You lost " + str(healthloss) + " health points during the action.          ")
    else:
        return_list.append("The spikes pierced through your body killing you.          ")

    return return_list


def fire_trap(player):
    # once again the same as the traps above, but with messages about a fire trapping and damaging the player
    return_list = ["You feel a warmth emanating from the ceiling", "You’ve got caught in a [FIRE TRAP].          "]
    healthloss = random.randint(10, 15)
    player.health = player.health - healthloss
    if player.health > 0:
        return_list.append("You managed to escape the trap.          ")
        return_list.append("You lost " + str(healthloss) + " health points during the action.          ")
    else:
        return_list.append("The fire burnt through your skin, killing you instantly.          ")

    return return_list


def trap(player):
    # randomize a value between one and three, then choose one of the trap functions to run based on the number
    # generated, then return what the trap function chosen returned. This function is the one used in main.py.
    trap_choice = random.randint(1, 3)
    if trap_choice == 1:
        return snake_trap(player)
    elif trap_choice == 2:
        return spike_trap(player)
    elif trap_choice == 3:
        return fire_trap(player)


def chest(player, item_amount):
    # Creates a random item, adds it to inventory if possible, and otherwise indicates that inventory is full

    # create a new item, randomize what the new item will be with random.randint
    # item_amount is decided in the main loop and is the amount of items in the game
    new_item = Item(random.randint(0, item_amount - 1))
    # create return list, put two messages in there to start with about the chest.
    return_list = ["You stumbled upon a chest!          ", "The chest contained a " + new_item.name + ".          "]
    # check if player.inventory is full (if it is less than five long
    if len(player.inventory) < 5:
        # put the new item into player.inventory
        player.inventory.append(new_item)
        # add a message about adding the item
        return_list.append(new_item.name + " was added to your inventory.          ")
        # return the list, return a message indicating that the item was successfully added, but do not return the new
        # item as there is no need for it in this case.
        return return_list, "SUCCESS", None
    # if the inventory is full
    if len(player.inventory) == 5:
        # append two messages about it, and what to do now
        return_list.append("You have too many items in your inventory.          ")
        return_list.append("Please select an item to remove from the inventory.          ")
        # return, return_list with the messages, a message indicating that there was a failure to add the item due to
        # a lack of item slots in inventory, and the new item as its needed for the process of replacing an item in
        # inventory for it
        return return_list, "FAILURE_NO_SLOTS", new_item


def end_screen(screen, font_big, font_small, scale_factor):
    # fill the screen with black color
    screen.fill((0, 0, 0))
    # render text about the player dying while trying to escape the dungeon
    death_text = font_big.render("YOU DIED", True, (255, 0, 0))
    restart_text = font_small.render("You were lost in the depths, and never found again.", True, (255, 255, 255))
    # blit those renders
    # choosing a set point on the display and then subtracting that points x and y values with half the x and y values
    # of the text object will lead to the text being centered on those points
    screen.blit(death_text, ((1920 * scale_factor) / 2 - (death_text.get_size()[0] / 2),
                             (1080 * scale_factor) / 2.2 - (death_text.get_size()[1] / 2)))
    screen.blit(restart_text, ((1920 * scale_factor) / 2 - (restart_text.get_size()[0] / 2), 650 * scale_factor))


def victory_screen(screen, font_big, font_small, scale_factor):
    # same as above, but with text indicating that you escaped the dungeon.
    screen.fill((0, 0, 0))
    victory_text = font_big.render("YOU ESCAPED", True, (0, 255, 0))
    message = font_small.render("You escaped the dungeon alive with all of the loot you collected.", True,
                                (255, 255, 255))
    screen.blit(victory_text, ((1920 * scale_factor) / 2 - (victory_text.get_size()[0] / 2),
                               (1080 * scale_factor) / 2.2 - (victory_text.get_size()[1] / 2)))
    screen.blit(message, ((1920 * scale_factor) / 2 - (message.get_size()[0] / 2), 650 * scale_factor))


def monster_text_render(screen, font, current_monster, scale_factor):
    # render and blit all of the information about the current monster onto the screen
    monster_text = font.render(current_monster.name + ",", True, (255, 255, 255))
    title_text = font.render(current_monster.title.replace("”", ""), True, (255, 255, 255))
    monster_hp_text = font.render("HP: " + str(current_monster.health), True, (255, 255, 255))
    monster_strength_text = font.render("Strength: " + str(current_monster.strength), True, (255, 255, 255))
    attack_text = font.render("1: Attack", True, (255, 255, 255))
    throw_text = font.render("2: Throw weapon", True, (255, 255, 255))
    demon_strike_text = font.render("3: Demon strike", True, (255, 255, 255))
    # this also takes advantage of the text centering from end_screen() to center the monsters values in the box its
    # contained in
    screen.blit(monster_text, (1535 - monster_text.get_size()[0] / 2 * scale_factor, 120 * scale_factor))
    screen.blit(title_text, (1535 - title_text.get_size()[0] / 2 * scale_factor, 200 * scale_factor))
    screen.blit(monster_hp_text, (1398 * scale_factor - monster_hp_text.get_size()[0] / 2, (280 * scale_factor)))
    screen.blit(monster_strength_text,
                (1633 * scale_factor - monster_strength_text.get_size()[0] / 2, 280 * scale_factor))
    screen.blit(attack_text, (1535 - attack_text.get_size()[0] / 2 * scale_factor, 360 * scale_factor))
    screen.blit(throw_text, (1535 - throw_text.get_size()[0] / 2 * scale_factor, 440 * scale_factor))
    screen.blit(demon_strike_text, (1535 - demon_strike_text.get_size()[0] / 2 * scale_factor, 520 * scale_factor))


def stats_text_render(screen, font, player, scale_factor, map_dict):
    # same as above, however now render information about the player and blit it onto its part of the screen. This
    # function does also take advantage of text centering.
    hp_text = font.render("HP: " + str(player.health), True, (255, 0, 0))
    level_text = font.render("Level: " + str(player.level), True, (0, 0, 255))
    strength_text = font.render("Strength: " + str(player.strength), True, (0, 255, 0))
    rooms_explored = font.render("Rooms explored: " + str(player.count_explored_rooms(map_dict)), True, (255, 255, 255))
    if player.on_hand is not None:
        on_hand_text = font.render("On hand: " + player.on_hand.name.replace('"', ""), True, (255, 255, 255))
    else:
        on_hand_text = font.render("On hand: None", True, (255, 255, 255))
    screen.blit(hp_text, (250 * scale_factor, 865 * scale_factor))
    screen.blit(strength_text, (832 * scale_factor, 865 * scale_factor))
    screen.blit(level_text, (1492 * scale_factor, 865 * scale_factor))
    screen.blit(rooms_explored, ((640 - rooms_explored.get_size()[0] / 2) * scale_factor, 938 * scale_factor))
    screen.blit(on_hand_text, ((1280 * scale_factor) - on_hand_text.get_size()[0] / 2, 938 * scale_factor))


def inventory_text_render(screen, font, player, items_to_render, scale_factor):
    # first render, text that only says inventory, then render all items currently in the players inventory
    inventory_text = font.render("Inventory:", True, (255, 255, 255))
    for item_to_render in player.inventory:
        new_item_to_render = font.render(item_to_render.name.replace('"', ""), True, (255, 255, 255))
        items_to_render.append(new_item_to_render)

    for item_to_render in range(len(items_to_render)):
        # the y coordinate increases as you go through the list,
        # making each item appear 80 pixels below the one before it
        screen.blit(items_to_render[0], (
            1535 * scale_factor - items_to_render[0].get_size()[0] / 2, ((180 + 80 * item_to_render) * scale_factor)))
        items_to_render.pop(0)

    screen.blit(inventory_text, (1535 - inventory_text.get_size()[0] / 2 * scale_factor, 120 * scale_factor))
