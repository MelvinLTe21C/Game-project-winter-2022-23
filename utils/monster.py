import random


class Monster:
    def __init__(self, monster_num):
        # open the file containing monsters
        monster_file = open("monster.txt", encoding="utf-8")
        # read the lines
        monsters = monster_file.readlines()
        # split the line of the monster given through input into parts separated by ,
        monster_info = monsters[monster_num - 1].split(",")
        # assign the monsters values and attributes to variables
        self.name = monster_info[0].replace('“', "")
        self.title = monster_info[1]
        self.strength = int(monster_info[2])
        self.health = int(monster_info[3])
        self.rarity = monster_info[4].replace("\n", "").replace('“', "")
        self.special_effect = monster_info[5].replace("\n", "").replace('“', "")
        self.last_health = self.health

    def encounter(self):
        # returns a list of text messages to be rendered when the monster is encountered
        return_list = ["Something lurks in the shadows...               ", "Suddenly, it pounces on you!          ",
                       "You've been attacked by a " + self.rarity + " " + self.name + "!          ",
                       "Press 1 to run away, or press 2 to fight the monster.          "]

        return return_list

    def attack(self, player):
        # randomizes and deals an amount of damage to the player, and returns a list of messages to be rendered about it

        # create and put first piece of text in return_list
        return_list = ["The " + self.name + " leaps forward and strikes!          "]

        # randomize an amount of damage based on the monsters strength
        damage_dealt = random.randint(int(self.strength * 0.2), int(self.strength * 2))
        # subtract that value from the players health
        player.health -= damage_dealt

        # append a different piece of text to return_list depending on how hard the attack hit compared to strength
        # if it was a heavy blow (dealt more than 1.3 * strength
        if damage_dealt > self.strength * 1.3:
            # message indicates a heavy hit
            return_list.append("The " + self.name + " lands a heavy blow, dealing " +
                               str(damage_dealt) + " damage.          ")
        # if the attack was weaker
        elif damage_dealt < self.strength * 0.7:
            # text indicates a weak attack that barely hit
            return_list.append("The " + self.name + " only barely hits, dealing " +
                               str(damage_dealt) + " damage.          ")
        else:
            # if the attacks damage was close to the monsters attack, the text indicates nothing special about it.
            return_list.append("The strike hits you, dealing " + str(damage_dealt) + " damage.          ")
        return return_list

    def update(self):
        # similar to player.update_stats(), this function is used to check if the monster is alive or not, as well
        # as letting the monster apply special effects

        # as this will be used on every frame, a list cannot be used to replace text_queue, but rather a message will
        # have to be appended to it in the main loop, which is why this function returns a string instead of a list
        # the way most other functions do
        return_message = ""
        # if the monsters health is 0 or lower, it has died and the fight has ended
        if self.health <= 0:
            # return_message is set to a message indicating that the monster has been slain.
            return_message = (self.name + ", " + self.title.replace("”", "") + " has been slain.          ")
            # returns the message as well as a code indicating that the monster has been killed, and that the fight
            # has therefore ended.
            return return_message, "MONSTERDEAD"
        # self.last_health is the last hp value that was recorded, meaning that it will be higher than the monsters
        # current health if the monster has recently been attacked and taken damage
        elif self.health < self.last_health:
            # if this has happened, we must check if the monster has the specific "enrage" effect that makes it increase
            # its own strength value by one after taking damage.
            if self.special_effect == "Enrage":
                # if it does, its strength is increased by one
                self.strength += 1
                # the message tells the player about how the monster has grown stronger.
                return_message = "The beast is enraged, and grows stronger.          "
            # self.last_health is set to self.health, as enrage monster would otherwise gain more strength infinitely
            # after taking damage. Also needed to detect new value changes after the first one
            self.last_health = self.health

        # this part of the code is only reachable if the monsters health was not 0 or lower, meaning that it only runs
        # if the monster is alive, and returns a return message of either an enrage message or nothing, as well as a
        # code indicating that the monster is still alive
        return return_message, "MONSTERALIVE"
