import random

STARTING_HEALTH = 100
MIN_DAMAGE = 10
MAX_DAMAGE = 40
MISSTEP_DAMAGE = 5

def readHighScore():
    RecordName = None
    RecordHealth = -1

    try:
        with open("highscore.txt", "r") as File:
            CurrentRecord = File.read().strip()
            Parts = CurrentRecord.split()
            RecordName = Parts[0].rstrip(":")
            RecordHealth = int(Parts[1])
    except FileNotFoundError:
        pass

    return RecordName, RecordHealth


def startGame():

    while True:
        print("\n---- Welcome to the Debian Dungeon ----")
        RecordName, RecordHealth = readHighScore()

        if RecordName is not None:
            print(f"Current Record Holder -> {RecordName}: {RecordHealth} HP")
        else:
            print("Current Record Holder -> No scores recorded yet! Be the first.")
            print("---------------------------------")

        PlayerName = input("Enter your hero's name: ")

        Health = STARTING_HEALTH
        Inventory = ["torch"]

        print(f"\nWelcome, {PlayerName}! HP: {Health} | Inventory: {Inventory}")
        print("You enter dark corridor and scary Terminal Bug block's your way.")

        Choice1 = input("Do you FIGHT or RUN away? (fight/run): ").lower()

        if Choice1 == "fight":
            Damage = random.randint(MIN_DAMAGE, MAX_DAMAGE)
            Health = Health - Damage
            print(f"Current HP: {Health}")

            print("You found a 'health_potion' on the floor! Added to inventory.")
            Inventory.append("health_potion")

        elif Choice1 == "run":
            print("\nYou safely trip over a rock but escape into the next room.")
        else:
            print(f"\nYou hesitated. The bug nipped your ankles for 5 damage.")
            Health = Health - MISSTEP_DAMAGE

        print(f"\nMoving on... HP: {Health} | Inventory: {Inventory}")
        print("You reach a dark, locked chest. It requires a torch to inspect safely.")

        if "torch" in Inventory:
            Choice2 = input("Use your torch to open the chest? (yes/no):").lower()
            if Choice2 == "yes" and "health_potion" in Inventory:
                print("\nYou safely open chest, drink your Health potion, and find the golden Debian source code! YOU WIN!")
                if Health > RecordHealth:
                    print(f"Saving your high score of {Health} HP...")
                    with open("highscore.txt", "w") as File:
                        File.write(f"{PlayerName}: {Health} HP")
                else:
                    print("You won, but the old high score remains!")
            elif Choice2 == "yes":
                print("\nYou open the chest but it's a trap! Exploded. Game over!.")
            else:
                print("\nYou walked past the chest and left the dungeon safely.")
        else:
            print("\nWithout a torch, you stumble in the dark, break your neck and die. Game over!")

        print("\n==========================================")
        Replay = input("Do you want to play again? (yes/no): ").lower()
        if Replay != "yes":
            print("Thanks for playing the Debian Dungeon! Goodbye.")
            break


startGame()

