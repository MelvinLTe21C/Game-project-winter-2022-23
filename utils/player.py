from utils.item import Item


class Player:
    def __init__(self):
        self.health = 10
        self.inventory = []
        self.level = 1
        self.on_hand = Item(0)
        self.strength = self.on_hand.strengthBonus

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
