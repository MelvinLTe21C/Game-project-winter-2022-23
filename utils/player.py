import random

from utils.item import Item


class Player:
    def __init__(self):
        self.max_health = 50
        self.health = self.max_health
        self.inventory = [Item(2)]
        self.level = 1
        self.on_hand = Item(1)
        if self.on_hand is not None:
            self.strength = 3 + self.on_hand.strengthBonus
        else:
            self.strength = 5
        self.location = (0, 0)

    def change_inventory_slot(self, new_item, slot):
        old_item = self.inventory[slot]
        if slot <= len(self.inventory):
            self.inventory.pop(slot)
            self.inventory.append(new_item)
            return old_item
        else:
            return "SLOT_DOES_NOT_EXIST"

    def update_stats(self, final_room):
        if self.on_hand is not None:
            self.strength = 3 + self.on_hand.strengthBonus + int((self.level * 0.7))
        else:
            self.strength = 3 + int((self.level * 0.7))
        if self.health < 0:
            self.health = 0
        if self.health > self.max_health:
            self.health = self.max_health
        if self.location == final_room:
            return "PLAYERESCAPED"
        elif self.health <= 0:
            return "PLAYERDEAD"
        else:
            return "PLAYERALIVE"

    def change_weapon(self, slot):
        if self.on_hand is not None:
            old_weapon = self.on_hand
            self.inventory.append(old_weapon)
        new_weapon = self.inventory[slot - 1]
        if new_weapon.type == "weapon":
            self.on_hand = new_weapon
            self.inventory.pop(slot - 1)

    def consume(self, slot):
        if self.inventory[slot - 1].type == "potion":
            potion = self.inventory[slot - 1]
            self.health = self.health + int(potion.healthGain * 3)
            self.inventory.pop(slot - 1)

    def move(self, direction, map_dict, room_list):
        if direction == "R":
            location_list = list(self.location)
            location_list[0] += 1
            if tuple((location_list[0], location_list[1])) in room_list:
                self.location = tuple(location_list)
                if not map_dict.get(self.location).visited:
                    map_dict.get(self.location).visited = True
                    return "SUCCESS_unvisited"
                else:
                    return "SUCCESS_visited"
            else:
                return "You can not walk in that direction."

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
        return_list = []
        if (self.location[0]-1, self.location[1]) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)
        if (self.location[0], self.location[1]-1) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        if (self.location[0]+1, self.location[1]) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        if (self.location[0], self.location[1]+1) in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)
        return return_list

    def attack(self, monster):
        damage_dealt = random.randint(int(self.strength * 0.5), int(self.strength * 2))
        monster.health -= damage_dealt
        return_list = []
        if self.on_hand is not None:
            return_list.append("You swing your " + self.on_hand.name + " at the " + monster.name + ".          ")
            if damage_dealt > self.strength * 1.3:
                return_list.append("The strike lands cleanly, dealing " + str(damage_dealt) + " damage.          ")
            elif damage_dealt < self.strength * 0.8:
                return_list.append("The attack only barely hits the monster, dealing " + str(damage_dealt) + "damage. "
                                                                                                             "        "
                                                                                                             " ") 
            else:
                return_list.append("The " + monster.name + " shrieks in pain as it's hit, taking " + str(damage_dealt) + " damage.          ")
        else:
            return_list.append("You hit the monster with your hands, dealing " + str(damage_dealt) + "damage.         "
                                                                                                     " ") 
        return return_list

    def throw_weapon(self, monster):
        damage_dealt = random.randint(int(self.on_hand.strengthBonus * 3), int(self.on_hand.strengthBonus * 6))
        return_list = ["In desperation, you hurl a " + self.on_hand.name + " at the monster.          ",
                       "It strikes the " + monster.name + " through the heart, dealing " + str(
                           damage_dealt) + " damage.          "]
        monster.health -= damage_dealt
        self.on_hand = None
        return return_list

    def soul_strike(self, monster):
        damage_dealt = random.randint(int(self.strength * 1.5), int(self.strength * 4))
        monster.health -= damage_dealt
        self.max_health -= 5
        self.health -= 5
        return_list = ["You feel an old, eldritch power flow through you...          ",
                       "With your newfound power, you strike the " + monster.name + "!          ",
                       "The strike lands with eldritch fury, dealing " + str(
                           damage_dealt) + " damage.          ",
                       "As the power drains away from you, you feel your chest hurt.          ",
                       "Your max health has been permanently reduced by 5.          "]
        return return_list

    @staticmethod
    def count_explored_rooms(map_dict):
        room_counter = 0
        for room in map_dict:
            if map_dict.get(room).visited:
                room_counter += 1
        return room_counter - 1
