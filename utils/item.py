class Item:
    def __init__(self, item_num):
        """Creates an item object. input the number the item is on in items.txt.
        Items can be weapons, potions or relics, and have different attributes based on what they are."""
        item_file = open("items.txt", encoding="utf-8")
        items = item_file.readlines()
        item_info = items[item_num - 1].split(",")
        self.name = item_info[0]
        if item_info[1].endswith("hp"):
            self.type = "potion"
            self.healthGain = item_info[1].replace("hp", "")
        else:
            self.type = "weapon"
            self.strengthBonus = int(item_info[1])
