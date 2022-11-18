#Welcome
def welcome():
    print("You were sent to a mysterious dungeon on a mission to locate a hidden tressure")
    print("After a rather long search you finally find the tressure")
    print("As you proceed to start looting it you step on a pressureplate")
    print("A mysterious sound echoes through the dungeon, and the ground begins to tremble")
    print("You run out of the room just to realize you are lost")
    print("Now you need to find a way out before it is too late...")
    
#All traps
def snake_trap(player):
    Print("You hear hissing from the wall just as poisonous snakes meander through")
    Print("You’ve got caught in a [SNAKE TRAP]")
    healthloss = random.randint(1, 2)
    player.health = player.health - healthloss
    if player.health > 0:
        print("You managed to escape the trap but lost", healthloss," health points during the action")
    else:
        print("The snakes overwhelmed you and filled your body with posion dealing", healthlost," damage")

def spike_trap(player):
    Print("You hear the ground tumbling beneath you and sharp spears appear through the ground")
    Print("You’ve got caught in a [SPIKE TRAP]")
    healthloss = random.randint(1, 2)
    player.health = player.health - healthloss
    if player.health > 0:
        print("You managed to escape the trap but lost", healthloss," health points during the action")
    else:
        print("The spikes pierced through your body dealing", healthloss, "damage")

def fire_trap(player):
    Print("You feel a warmth emanating from the ceiling")
    Print("You’ve got caught in a [FIRE TRAP]")
    healthloss = random.randint(1, 2)
    player.health = player.health - healthloss
    if player.health > 0:
        print("You managed to escape the trap but lost", healthloss," health points during the action")
    else:
        print("The fire burnt through your skin dealing", healthloss, "damage")

#Alternativ, check stats, check inventory or choose direction to go
def alternativ():
    print("What would you like to do now?")
    print("Check stats (1)")
    print("Check inventory (2)")
    print("Continue the journey (3)")
    answer = input("I choose to: ")
    if answer in ["1","2","3"]:
        answer = int(answer)
        return(answer)
    else:
        print("")
        print("Please choose an valid option")
        print("")
        alternativ()

#Options when opening inventory
def open_inventory(items, onhand):
    print(items)
    print(onhand)
    print("")
    print("What would you like to do in the inventory")
    print("Equip weapond (1)")
    print("Consume health potion (2)")
    print("Close inventory (3)")
    answer = input("I choose to: ")
    if answer in ["1","2","3"]:
        answer = int(answer)
        return(answer)
    else:
        print("")
        print("Please choose an valid option")
        print("")
        op_inventory(items, onhand)


