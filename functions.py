import random
from utils.item import Item


def welcome():
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
    return_list = ["You hear hissing from the wall.          ",
                   "Poisonous snakes meander through reaching for your soul.          ",
                   "You’ve got caught in a [SNAKE TRAP].          "]
    healthloss = random.randint(1, 2)
    player.health = player.health - healthloss
    if player.health > 0:
        return_list.append("You managed to escape the trap.          ")
        return_list.append("But lost " + str(healthloss) + " health points during the action.          ")
    else:
        return_list.append("The snakes overwhelmed you.          ")

    return return_list


def spike_trap(player):
    return_list = ["You hear the ground tumbling beneath you.          ", "Sharp spears appear through the ground.          ",
                   "You’ve got caught in a [SPIKE TRAP].          "]
    healthloss = random.randint(1, 2)
    player.health = player.health - healthloss
    if player.health > 0:
        return_list.append("You managed to escape the trap.          ")
        return_list.append("You lost" + str(healthloss) + " health points during the action.          ")
    else:
        return_list.append("The spikes pierced through your body killing you.          ")

    return return_list


def fire_trap(player):
    return_list = ["You feel a warmth emanating from the ceiling", "You’ve got caught in a [FIRE TRAP].          "]
    healthloss = random.randint(1, 2)
    player.health = player.health - healthloss
    if player.health > 0:
        return_list.append("You managed to escape the trap.          ")
        return_list.append("You lost " + str(healthloss) + " health points during the action.          ")
    else:
        return_list.append("The fire burnt through your skin, killing you instantly.          ")

    return return_list


def trap(player):
    trap_choice = random.randint(1, 3)
    if trap_choice == 1:
        return snake_trap(player)
    elif trap_choice == 2:
        return spike_trap(player)
    elif trap_choice == 3:
        return fire_trap(player)


# Alternativ, check stats, check inventory or choose direction to go
def alternativ(player, mapdict):
    print("What would you like to do now?          ")
    print("Check stats (1)          ")
    print("Check inventory (2)          ")
    print("Continue the journey (3)          ")
    answer = input("I choose to:           ")
    if answer in ["1", "2", "3"]:
        if answer == "1":
            player.print_stats(mapdict)
        elif answer == "2":
            open_inventory()
        elif answer == "3":
            choose_direction()

    else:
        print("          ")
        print("Please choose an valid option          ")
        print("          ")
        alternativ(player, mapdict)


def open_inventory(items, onhand):
    print("Inventory:", items)
    print("You have a", onhand, "equipped          ")
    print("          ")
    print("What would you like to do in the inventory          ")
    print("Equip weapond (1)          ")
    print("Consume health potion (2)          ")
    print("Close inventory (3)          ")
    answer = input("I choose to:           ")
    if answer in ["1", "2", "3"]:
        answer = int(answer)
        return answer
    else:
        print("          ")
        print("Please choose an valid option          ")
        print("          ")
        open_inventory(items, onhand)


"""""
def encounter(player):
    if player.strenth > monster.strenth:
        print("The monster had", monster.strenth, "and you successfully won the battle!          ")
        player.lv += 1
    elif player.strenth < monster.strenth:
        print("The monster had", monster.strenth, "and left you harmed taking 2 damage          ")
        player.hp -= 2
    else:
        print("After an exhausting fight the monster ran away and the fight ended in a draw          ")
        
"""


def chest(player, item_amount):
    new_item = Item(random.randint(0, item_amount - 1))
    return_list = ["You stumbled upon a chest!", "The chest contained a " + new_item.name + ".          "]
    if len(player.inventory) < 5:
        player.inventory.append(new_item)
        return_list.append(new_item.name + " was added to your inventory.          ")
        return return_list, "SUCCESS", None
    if len(player.inventory) == 5:
        return_list.append("You have too many items in your inventory.          ")
        return_list.append("Please select an item to remove from the inventory.          ")
        return return_list, "FAILURE_NO_SLOTS", new_item


def end_screen(screen, font_big, font_small, scale_factor):
    screen.fill((0, 0, 0))
    death_text = font_big.render("YOU DIED", True, (255, 0, 0))
    restart_text = font_small.render("You were lost in the depths, and never found again.", True, (255, 255, 255))
    screen.blit(death_text, ((1920 * scale_factor) / 2 - (death_text.get_size()[0] / 2),
                             (1080 * scale_factor) / 2.2 - (death_text.get_size()[1] / 2)))
    screen.blit(restart_text, ((1920 * scale_factor) / 2 - (restart_text.get_size()[0] / 2), 650 * scale_factor))
