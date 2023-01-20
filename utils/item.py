class Item:
    def __init__(self, item_num):
        """Creates an item object. input the number the item is on in items.txt.
        Items can be weapons, potions or relics, and have different attributes based on what they are."""

        # opens the text file containing the names and stats of all weapons
        item_file = open("items.txt", encoding="utf-8")
        # gets all of the items as strings containing their names, stats and rarities
        items = item_file.readlines()
        # gets the information about the specific item that the input wants, and splits them up at every ,
        item_info = items[item_num - 1].split(",")

        # assigns every value of the weapon or potion that the input asked for
        self.name = item_info[0]

        # weapons and potions have different types, as well as weapons having a strength_bonus, while potions have
        # a healthGain
        
        # potions second value in the text file end with hp if the item is a potion, meaning that the code below 
        # activates if the item is a potion
        if item_info[1].endswith("hp"):
            # if it is, set its type and healthGain
            self.type = "potion"
            self.healthGain = int(item_info[1].replace("hp", ""))
        else:
            # if it is not, set its type and strengthBonus
            self.type = "weapon"
            self.strengthBonus = int(item_info[1])
