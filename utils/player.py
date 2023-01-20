import random

from utils.item import Item


class Player:
    def __init__(self):
        self.max_health = 50
        self.health = self.max_health
        # start with one tiny health potion (item code 2) in inventory
        self.inventory = [Item(2)]
        # start at level 1
        self.level = 1
        # start with a steel dagger (item code 1) on hand
        self.on_hand = Item(1)
        # prevent issues being caused by having thrown weapon, and thus self.on_hand being None
        if self.on_hand is not None:
            self.strength = 2 + self.on_hand.strengthBonus
        else:
            self.strength = 2
        self.location = (0, 0)

    def change_inventory_slot(self, new_item, slot):
        # keep old item in new variable so it can be used later to show which item has been discarded
        old_item = self.inventory[slot - 1]
        # only continue if the slot chosen is in the inventory, and not outside of it. There is no need to account for
        # negative numbers as only 1,2,3,4,5 and are possible within the domain of definition
        if slot - 1 <= len(self.inventory):
            # remove the old item from inventory
            self.inventory.pop(slot - 1)
            # append the new item to inventory
            self.inventory.append(new_item)
            # return old item for use in main loop
            return old_item
        else:
            # return error message if the slot is not in inventory, telling the main loop to let the player give input
            # again, hopefully this time a valid slot in inventory
            return "SLOT_DOES_NOT_EXIST"

    def update_stats(self, final_room):
        # this function serves two main purposes. It checks for the games end conditions having been reached
        # (the players health being <= 0 or the player having reached the final room), and returns a corresponding
        # message if either is true. Additionally, the function being called once per frame means that the players
        # stats are continually updated. This is relevant to for example player.strength, which can change during the
        # game. If it was not continually updated, the players strength would be stuck on the same value all game,
        # despite levelling up and finding new weapons.

        # if player has a weapon on hand:
        if self.on_hand is not None:
            # calculate strength as an int that depends on weapon on hand as well as level
            self.strength = 2 + self.on_hand.strengthBonus + int((self.level * 0.7))
        # if player does not have a weapon on hand:
        else:
            # strength is calculated based on level only.
            self.strength = 2 + int((self.level * 0.7))
        # make sure that health cannot go below zero for aesthetic purposes
        if self.health < 0:
            self.health = 0
        # make sure that a players health cannot go above its max value as that would remove all strategy around
        # drinking potions. If the players health is above its max health, it will be set to max_health
        if self.health > self.max_health:
            self.health = self.max_health
        # check if player has reached the final room and thus escaped
        if self.location == final_room:
            return "PLAYERESCAPED"
        # check if the player has died
        elif self.health <= 0:
            return "PLAYERDEAD"
        # if neither of the above conditions are true, return the normal code and keep the game running as normal
        else:
            return "PLAYERALIVE"

    def change_weapon(self, slot):
        # change which weapon you have on hand
        # replace the on hand weapon with a weapon from your inventory, and add the old on hand weapon to inventory

        # only continue if the player has a weapon on hand
        if self.on_hand is not None:
            # save the old item
            old_weapon = self.on_hand
            # choose the new weapon from inventory
            new_weapon = self.inventory[slot - 1]
            # only proceed if the new weapon has type "weapon", as the players on hand may not be a potion.
            if new_weapon.type == "weapon":
                # and add it to inventory
                self.inventory.append(old_weapon)
                # make the item chosen the on_hand weapon
                self.on_hand = new_weapon
                # remove the item chosen from inventory
                self.inventory.pop(slot - 1)

    def consume(self, slot):
        # only works if the item in question is a potion, so check if the item chosen is a potion
        if self.inventory[slot - 1].type == "potion":
            # pick out the potion
            potion = self.inventory[slot - 1]
            # increase player health by a value depending on the potion chosen
            self.health = self.health + int(potion.healthGain * 3)

            # remove the potion from inventory
            self.inventory.pop(slot - 1)

    def move(self, direction, map_dict, room_list):
        # check what direction was chosen, direction is given as an input in the main loop
        if direction == "R":
            # convert the tuple containing the players location to a list in order to make it mutable, as tuples
            # are naturally immutable, while lists are mutable
            location_list = list(self.location)
            # change the players x-coordinate in the grid by one. This means that the player moves one room to the
            # right of their current room. The start coordinates are (0, 0) and are the start room
            location_list[0] += 1
            # room_list is a list of tuples, therefore we have to convert location_list to a tuple to check if the room
            # the player is attempting to move into is in room_list. Without this check, the player could walk off the
            # map.
            if tuple((location_list[0], location_list[1])) in room_list:
                # set self.location to the new coordinates after addition to the x value
                self.location = tuple(location_list)
                # map_dict.get(self.location) returns the instance of class Room that the player is currently in, which
                # has an attribute visited that decides if the rooms content is rendered or not. If the Rooms visited
                # attribute is not set to visited, set it to visited to indicate that the player has visited the room
                if not map_dict.get(self.location).visited:
                    map_dict.get(self.location).visited = True
                    # return a code indicating that the player reached the room, and that the room was unvisited
                    return "SUCCESS_unvisited"
                else:
                    # if the room was visited, return a code matching that scenario.
                    return "SUCCESS_visited"
            else:
                # if the room the player is attempting to walk into doesnt exist, return a message that will be rendered
                # telling the player that they may not walk in that direction.
                return "You can not walk in that direction."

        # same as the segment above, except moving left instead of right.
        elif direction == "L":
            location_list = list(self.location)
            location_list[0] -= 1
            if tuple((location_list[0], location_list[1])) in room_list:
                self.location = tuple(location_list)
                if not map_dict.get(self.location).visited:
                    map_dict.get(self.location).visited = True
                    return "SUCCESS_unvisited"
                else:
                    return "SUCCESS_visited"
            else:
                return "You can not walk in that direction."

        # now moving up
        elif direction == "U":
            location_list = list(self.location)
            location_list[1] -= 1
            if tuple((location_list[0], location_list[1])) in room_list:
                self.location = tuple(location_list)

                if not map_dict.get(self.location).visited:
                    map_dict.get(self.location).visited = True
                    return "SUCCESS_unvisited"
                else:
                    return "SUCCESS_visited"
            else:
                return "You can not walk in that direction."

        # now moving down
        elif direction == "D":
            location_list = list(self.location)
            location_list[1] += 1
            if tuple((location_list[0], location_list[1])) in room_list:
                self.location = tuple(location_list)
                if not map_dict.get(self.location).visited:
                    map_dict.get(self.location).visited = True
                    return "SUCCESS_unvisited"
                else:
                    return "SUCCESS_visited"
            else:
                return "You can not walk in that direction."

    def detect_doors(self, map_dict):
        """""returns a list of booleans. Each bool stands for one direction,
         in the following direction: Left, Up, Right, Down"""
        # create return_list
        return_list = []
        # check if the room with players x coordinate - 1 and y coordinate (the room to the left of the player)
        # is in map_dict (if it does, it exists as a room)
        if (self.location[0] - 1, self.location[1]) in map_dict:
            # if room exists, append True to the return_list
            return_list.append(True)
        else:
            # if not, append False
            return_list.append(False)
        # repeat for the room above players location
        if (self.location[0], self.location[1] - 1) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        # repeat for the room right of players location
        if (self.location[0] + 1, self.location[1]) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        # repeat for the room below players location
        if (self.location[0], self.location[1] + 1) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        # return the list of booleans
        return return_list

    def attack(self, monster):
        # a normal attack, dealing damage to the monster without any extra effects.

        # randomize the damage dealt as ant int that is around the players strength value
        damage_dealt = random.randint(int(self.strength * 0.5), int(self.strength * 2))
        # reduce the monsters health by the randomized amount
        monster.health -= damage_dealt

        # create the return_list
        return_list = []

        # there are different messages depending on whether the player has a weapon on hand or not, therefore check
        # if the player has a weapon on hand
        if self.on_hand is not None:
            # append message about hitting the monster with your weapon
            return_list.append("You swing your " + self.on_hand.name + " at the " + monster.name + ".          ")
            # if the damage dealt was considerably higher than your strength value, add a message about a heavy hit
            if damage_dealt > self.strength * 1.3:
                return_list.append("The strike lands cleanly, dealing " + str(damage_dealt) + " damage.          ")
            # if the damage was considerably lower than strength value, add a message about a loose hit
            elif damage_dealt < self.strength * 0.8:
                return_list.append("The attack only barely hits the monster, dealing " + str(damage_dealt) + " damage. "
                                                                                                             "        "
                                                                                                             " ")
            # if the attack was neither high or low compared to player.strength, add a message about a normal attack
            else:
                return_list.append("The " + monster.name + " shrieks in pain as it's hit, taking " + str(damage_dealt) +
                                   " damage.          ")

        # if you have no weapon on hand, add a message about hitting the monster with your hands
        else:
            return_list.append("You hit the monster with your hands, dealing " + str(damage_dealt) + "damage.         "
                                                                                                     " ")

        # return the list of messages to be shown
        return return_list

    def throw_weapon(self, monster):
        # a more powerful attack towards a monster, where you sacrifice your on hand weapon for a higher damage attack

        # attack is only possible if player has a weapon on hand
        if self.on_hand is not None:
            # randomize attack value, with higher damage values than the normal attack
            damage_dealt = random.randint(int(self.on_hand.strengthBonus * 3), int(self.on_hand.strengthBonus * 6))
            # create return_list and add in messages about throwing your weapon at the monster
            return_list = ["In desperation, you hurl a " + self.on_hand.name + " at the monster.          ",
                           "It strikes the " + monster.name + " through the heart, dealing " + str(
                               damage_dealt) + " damage.          "]

            # subtract the monsters health with the damage you dealt
            monster.health -= damage_dealt

            # discard the on_hand weapon
            self.on_hand = None

            # return return_list
            return return_list
        else:
            # if there is no weapon to throw, the player may not use this attack, and it becomes the monsters
            # turn to attack, since the player made a mistake
            return ["You have no weapon to throw.          "]

    def soul_strike(self, monster):
        # a powerful attack with the drawback of dealing damage to you and permanently decreasing your max hp by 5

        # randomize damage to deal to the monster
        damage_dealt = random.randint(int(self.strength * 1.5), int(self.strength * 4))

        # subtract from monster hp
        monster.health -= damage_dealt

        # decrease health and max_health by 5
        self.max_health -= 5
        self.health -= 5

        # append messages about the attack
        return_list = ["You feel an old, eldritch power flow through you...          ",
                       "With your newfound power, you strike the " + monster.name + "!          ",
                       "The strike lands with eldritch fury, dealing " + str(
                           damage_dealt) + " damage.          ",
                       "As the power drains away from you, you feel your chest hurt.          ",
                       "Your max health has been permanently reduced by 5.          "]

        # return the list of messages to be rendered
        return return_list

    @staticmethod
    def count_explored_rooms(map_dict):
        # this function counts how many rooms the player have explored to showcase as a part of player stat display

        # set counter for rooms to zero
        room_counter = 0

        # loop through each room in map dict, room will be an instance of Room class
        for room in map_dict:
            # Room class has an attribute visited which can be True or False
            # Check if that is true, for all rooms in map_dict
            if map_dict.get(room).visited:
                # if it has, add one to the counter
                room_counter += 1

        # return the room counter minus one because of the first room being set to visited but not having been explored
        return room_counter - 1
