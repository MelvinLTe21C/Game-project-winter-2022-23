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
def alternativ(player,mapdict):
    print("What would you like to do now?")
    print("Check stats (1)")
    print("Check inventory (2)")
    print("Continue the journey (3)")
    answer = input("I choose to: ")
    if answer in ["1","2","3"]:
        if answer == "1":
            player.print_stats(mapdict)
        elif answer == "2":
            open_inventory()
        elif answer == "3":
            choose_direction()
    
    else:
        print("")
        print("Please choose an valid option")
        print("")
        alternativ()


def open_inventory(items, onhand):
    print("Inventory:", items)
    print("You have a", onhand, "equipped")
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
        open_inventory(items, onhand)

def combat(player):
    player_hp = 100
    monster_hp = 100
    
    while player_hp > 0 or monster_hp > 0:
        playerdmg = max(0,random.range(player.strenth -5, player.strenth + 5))
        monster_hp -= playerdmg
        return "You hit the monster for",playerdmg
        
        monsterdmg = max(0,random.range(5,10*player.lv*(1/2))
        player_hp -= monsterdmg
        return "You lost", monsterdmg,"health from the monsters attack"
                         
    if monster_hp < 1:
        return "You won the battle and leveled upp"
        return "You are now lv", player.lv
                         
    if player_hp < 1:
        return "You lost the battle"
        if monster_hp > 75:
            player.health -= 4
        elif monster_hp > 50:
            player.health -= 3
        elif monster_hp > 25:
            player.health -= 2
        else:
            player.health -= 1
                 
                 
        
                         
