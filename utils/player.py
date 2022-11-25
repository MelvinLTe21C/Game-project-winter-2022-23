class Player:
    def __init__(self):
        self.health = 10
        self.inventory = []
        self.level = 1
        self.on_hand = Item(0)
        self.strength = self.on_hand.strengthBonus
        self.location = [0, 0]

    def change_weapon(self, slot):
        if slot - 1 > len(self.inventory):
            print("There is no item in that slot - 1. Try again.")
        else:
            old_weapon = self.on_hand
            new_weapon = self.inventory[slot - 1]
            if new_weapon.type == "Weapon":
                self.on_hand = new_weapon
                self.inventory.append(old_weapon)
            else:
                print("The item you chose is not a weapon. Please try again.")

    def consume(self, slot):
        if slot - 1 > len(self.inventory):
            print("There is no item in that slot. Try again.")
        else:
            if self.inventory[slot - 1].type == "potion":
                potion = self.inventory[slot - 1]
                self.health = self.health + potion.healthGain
                self.inventory.pop(slot - 1)

    def move(self, direction):
        if direction == "R":
            self.location[0] -= 1
        elif direction == "L":
            self.location[0] -= 1
        elif direction == "U":
            self.location[1] -= 1
        elif direction == "D":
            self.location[1] -= 1

    def detect_doors(self, map_dict):
        """""returns a list of booleans. Each bool stands for one direction,
         in the following direction: Left, Up, Right, Down"""
        return_list = []
        if [self.location[0]-1, self.location[1]] in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)
        if [self.location[0], self.location[1]-1] in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        if [self.location[0]+1, self.location[1]] in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

        if [self.location[0], self.location[1]+1] in map_dict:
            return_list.append(True)
        else:
            return_list.append(False)

    def print_stats(self, map_dict):
        room_counter = 0
        for item in map_dict:
            if item.visited:
                room_counter += 1
        return_list = (["Your level is " + str(self.level), "Your health is " + str(self.health),
                       "Your strenght is " + str(self.strength), "You have explored " + str(room_counter) + "rooms"])
        return return_list
