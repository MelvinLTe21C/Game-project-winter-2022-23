import random


class Monster:
    def __init__(self, monster_num):
        monster_file = open("monster.txt", encoding="utf-8")
        monsters = monster_file.readlines()
        monster_info = monsters[monster_num - 1].split(",")
        self.name = monster_info[0].replace('“', "")
        self.title = monster_info[1]
        self.strength = int(monster_info[2])
        self.health = int(monster_info[3])
        self.rarity = monster_info[4].replace("\n", "").replace('“', "")
        self.special_effect = monster_info[5].replace("\n", "").replace('“', "")
        self.last_health = self.health

    def encounter(self):
        return_list = ["Something lurks in the shadows...               ", "Suddenly, it pounces on you!          ",
                       "You've been attacked by a " + self.rarity + " " + self.name + "!          ",
                       "Press 1 to run away, or press 2 to fight the monster.          "]

        return return_list

    def attack(self, player):
        return_list = ["The " + self.name + " leaps forward and strikes!          "]
        damage_dealt = random.randint(int(self.strength * 0.2), int(self.strength * 2))
        player.health -= damage_dealt
        if damage_dealt > self.strength * 1.3:
            return_list.append("The " + self.name + " lands a heavy blow, dealing " +
                               str(damage_dealt) + " damage.          ")
        elif damage_dealt < self.strength * 0.7:
            return_list.append("The " + self.name + " only hits loosely, dealing " +
                               str(damage_dealt) + " damage.          ")
        else:
            return_list.append("The strike hits you, dealing " + str(damage_dealt) + " damage.          ")
        return return_list

    def update(self):
        return_message = ""
        if self.health <= 0:
            return_message = (self.name + ", " + self.title.replace("”", "") + " has been slain.          ")
            return return_message, "MONSTERDEAD"
        elif self.health < self.last_health:
            if self.special_effect == "Enrage":
                self.strength += 1
                return_message = "The beast is enraged, and grows stronger.          "
            self.last_health = self.health
        return return_message, "MONSTERALIVE"
