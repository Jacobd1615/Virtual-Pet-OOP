from colorama import init, Fore, Style
import platform
import random
import os

# Initialize colorama for colored output (works cross-platform)
init()

# ASCII art variations for dog and cat
DOG_ART = [
    f"{Fore.YELLOW}🐶 {Fore.RED}*wags tail menacingly*{Style.RESET_ALL}\n  /_/\n ( o.o ) \n  > ^ <",  # Normal
    f"{Fore.RED}👹 {Fore.YELLOW}I don’t like the way he’s looking at me...{Style.RESET_ALL}\n  /_/\n ( >.< ) \n  > 0 <\n  *demonic unhumanic grin*",  # Demonic
    f"{Fore.YELLOW}🐶 {Fore.CYAN}*sleeping, dreaming of you*{Style.RESET_ALL}\n  /_/\n ( -.- ) zZ\n  > ^ <"  # Sleeping
]

CAT_ART = [
    f"{Fore.YELLOW}😺 {Fore.RED}*purrs ominously*{Style.RESET_ALL}\n /_/\n ( o.o ) \n > ^ <",  # Normal
    f"{Fore.RED}👹 {Fore.YELLOW}I don’t like the way she’s looking at me...{Style.RESET_ALL}\n /_/\n ( >.< ) \n > 0 <\n  *demonic hissing*",  # Demonic
    f"{Fore.YELLOW}😺 {Fore.CYAN}*sleeping, plotting in dreams*{Style.RESET_ALL}\n /_/\n ( -.- ) zZ\n > ^ <"  # Sleeping
]

class Pet:
    def __init__(self, name, hunger=10, happiness=100):
        self.name = name
        self.hunger = max(0, min(hunger, 100))  # Clamp hunger between 0 and 100
        self.happiness = max(0, min(happiness, 100))  # Clamp happiness between 0 and 100
        self.play_count = 0  # Track consecutive plays
        self.feed_count = 0  # Track consecutive feeds
        self.play_locked = False  # Track if play is locked due to overuse
        self.action_count = 0  # Track total actions for demonic art trigger

    def feed(self):
        self.play_count = 0  # Reset play count
        self.feed_count += 1  # Increment feed count
        self.play_locked = False  # Unlock play
        self.action_count += 1  # Increment action count
        self.happiness = max(0, min(self.happiness - 5, 100))  # Decrease happiness by 5
        if self.hunger >= 100:
            return False, f"{Fore.RED}💥 {self.name} was overfed and EXPLODED! Guts everywhere...{Style.RESET_ALL}\n{Fore.RED}☠️ Game over. You monster.{Style.RESET_ALL}"
        self.hunger = max(0, min(self.hunger + 10, 100))  # Increase hunger by 10
        message = f"{Fore.RED}😈 {self.name} 'I'm fine do not over feed me!'{Style.RESET_ALL}" if self.feed_count > 3 else f"{Fore.GREEN}🍽️ {self.name} has been fed!{Style.RESET_ALL} Hunger: {self.hunger}/100, Happiness: {self.happiness}/100 😊"
        continue_game, status_message = self._check_status()
        return continue_game, f"{message}\n{status_message}"

    def play(self):
        if self.play_locked:
            return True, f"{Fore.RED}😡 {self.name} snaps, 'I said STOP! You’re done playing with me.'{Style.RESET_ALL}"
        self.feed_count = 0  # Reset feed count
        self.play_count += 1  # Increment play count
        self.action_count += 1  # Increment action count
        self.happiness = max(0, min(self.happiness - 5, 100))  # Decrease happiness by 5
        if self.play_count > 3:
            self.play_locked = True
            threats = [
                f"{self.name} grabs your wrist with unnatural strength: 'Play again, and I’ll break you.'",
                f"{self.name}’s eyes glow red: 'Enough. You’re testing my patience, human.'",
                f"{self.name} whispers coldly, 'Keep this up, and you’ll be the toy.'",
            ]
            return True, f"{Fore.RED}👁️ {random.choice(threats)}{Style.RESET_ALL}"
        self.hunger = max(0, min(self.hunger - 5, 100))  # Decrease hunger by 5
        self.happiness = max(0, min(self.happiness + 15, 100))  # Increase happiness by 15
        play_messages = [
            f"{self.name} chases its tail wildly! It’s almost too excited.",
            f"{self.name} pounces on a toy, eyes gleaming with joy!",
            f"{self.name} bounds around, barely containing its glee!"
        ] if isinstance(self, Dog) else [
            f"{self.name} bats at a string, purring with delight!",
            f"{self.name} leaps into a box, thrilled beyond reason!",
            f"{self.name} chases a laser, moving like a shadow!"
        ]
        message = f"{Fore.CYAN}🎾 {random.choice(play_messages)}{Style.RESET_ALL} Hunger: {self.hunger}/100, Happiness: {self.happiness}/100 😄"
        continue_game, status_message = self._check_status()
        return continue_game, f"{message}\n{status_message}"

    def bath(self):
        self.feed_count = 0  # Reset feed count
        self.play_count = 0  # Reset play count
        self.play_locked = False  # Unlock play
        self.action_count += 1  # Increment action count
        self.happiness = max(0, min(self.happiness - 5, 100))  # Decrease happiness by 5
        outcomes = [
            f"{Fore.CYAN}🛁 {self.name} enjoyed a nice bath! So clean!{Style.RESET_ALL}",
            f"{Fore.RED}🛁 {self.name} grabs you and drowns you in the tub! 'You thought you could control me?'{Style.RESET_ALL}\n{Fore.RED}☠️ Game over. You’re underwater.{Style.RESET_ALL}",
            f"{Fore.RED}🛁 You barely survived {self.name}’s bath! Bones broken, pain unending.{Style.RESET_ALL} Happiness: 10/100 😿"
        ]
        outcome = random.choice(outcomes)
        if outcome == outcomes[0]:  # Nice bath
            self.happiness = max(0, min(self.happiness + 10, 100))  # Increase happiness by 10
            continue_game = True
            status_message = self._check_status()[1]
            return continue_game, f"{outcome} Happiness: {self.happiness}/100 😊\n{status_message}"
        elif outcome == outcomes[1]:  # Drowning
            return False, outcome
        else:  # Broken bones
            self.happiness = 10  # Set happiness to 10
            continue_game = True
            status_message = self._check_status()[1]
            return continue_game, f"{outcome}\n{status_message}"

    def _check_status(self):
        status_message = ""
        if self.hunger == 100:
            return False, f"{Fore.RED}💥 {self.name} was overfed and EXPLODED! Guts everywhere...{Style.RESET_ALL}\n{Fore.RED}☠️ Game over. You monster.{Style.RESET_ALL}"
        elif self.hunger == 0:
            return False, f"{Fore.RED}😈 {self.name}’s hunger consumes you! 'Your pet is literally eating your bones....'{Style.RESET_ALL}\n{Fore.RED}☠️ Game over. You’ve been eaten.{Style.RESET_ALL}"
        elif self.hunger <= 20:
            status_message += f"{Fore.RED}⚠️ Warning: {self.name} is starving! Feed them, or they’ll chew your bones! 🍽️{Style.RESET_ALL}\n"
        if self.happiness == 0:
            return False, f"{Fore.RED}☠️ {self.name} glares with hatred and vanishes into the night! 'Leaving an axe in your face....'{Style.RESET_ALL}\n{Fore.RED}☠️ Game over. You’re alone now.{Style.RESET_ALL}"
        elif self.happiness <= 20:
            status_message += f"{Fore.RED}⚠️ Warning: {self.name} is miserable! Play with them, or they’ll curse you! 🎉{Style.RESET_ALL}\n"
        elif self.happiness + 3 > 100:  # Check for potential happiness overflow
            outcomes = [
                f"{Fore.RED}💔 {self.name}’s heart couldn’t handle the joy! It collapses.{Style.RESET_ALL}",
                f"{Fore.RED}🚗 {self.name} was so happy it ran outside and got hit by a car!{Style.RESET_ALL}"
            ]
            return False, f"{random.choice(outcomes)}\n{Fore.RED}☠️ Game over. Too much joy is deadly.{Style.RESET_ALL}"
        return True, status_message

    def status(self):
        self.action_count += 1  # Increment action count
        self.play_locked = False  # Unlock play
        self.happiness = max(0, min(self.happiness - 5, 100))  # Decrease happiness by 5
        hunger_color = Fore.GREEN if self.hunger <= 50 else Fore.YELLOW if self.hunger <= 80 else Fore.RED
        happiness_color = Fore.GREEN if self.happiness >= 50 else Fore.YELLOW if self.happiness >= 20 else Fore.RED
        message = f"{Fore.MAGENTA}☠️ {self.name}'s Status ☠️{Style.RESET_ALL}\n"
        message += f"  Hunger: {hunger_color}{self.hunger}/100{Style.RESET_ALL} {'🍖' if self.hunger <= 50 else '😓'}\n"
        message += f"  Happiness: {happiness_color}{self.happiness}/100{Style.RESET_ALL} {'😺' if self.happiness >= 50 else '😿'}\n"
        if self.play_count > 3 or self.feed_count > 3:
            message += f"{Fore.RED}👁️‍🗨️ {self.name}’s gaze pierces you. Something’s wrong...{Style.RESET_ALL}\n"
        continue_game, status_message = self._check_status()
        return continue_game, f"{message}{status_message}"


class Dog(Pet):
    def __init__(self, name, hunger=30, happiness=60):
        super().__init__(name, hunger, happiness)
        self.tricks_learned = 0

    def learn_trick(self):
        self.feed_count = 0  # Reset feed count
        self.play_count = 0  # Reset play count
        self.play_locked = False  # Unlock play
        self.action_count += 1  # Increment action count
        self.happiness = max(0, min(self.happiness - 5, 100))  # Decrease happiness by 5
        if self.happiness >= 50 and self.hunger <= 50:
            self.tricks_learned += 1
            self.happiness = max(0, min(self.happiness + 15, 100))  # Increase happiness by 15
            trick_messages = [
                f"{self.name} ran for office and became PRESIDENT! 'War' Tricks: {self.tricks_learned} 🏛️",
                f"{self.name} slunk to the drug store, bought a winning lottery ticket for you... but kept the cash. 'Mine now.' Tricks: {self.tricks_learned} 💰",
                f"{self.name} did your taxes, then growled, 'You spend too much!' Now it demands $500 for its services. Tricks: {self.tricks_learned} 📊",
                f"{self.name} became your therapist, analyzed your fears, 'You’re a mess.' Tricks: {self.tricks_learned} 🛋️",
                f"{self.name} learned to summon spirits and now leads a cult in your backyard. Tricks: {self.tricks_learned} 😈",
                f"{self.name} hacked your bank account and bought a new house. 'I think I should move' Tricks: {self.tricks_learned} 🏰",
                f"{self.name} wrote a bestselling horror novel about eating you. 'It’s nonfiction.' Tricks: {self.tricks_learned} 📖",
            ]
            message = f"{Fore.YELLOW}🐶 {random.choice(trick_messages)}{Style.RESET_ALL}"
            continue_game, status_message = self._check_status()
            return continue_game, f"{message}\n{status_message}"
        else:
            return True, f"{Fore.RED}😣 {self.name} snarls, 'I’m not your puppet!'{Style.RESET_ALL}"


class Cat(Pet):
    def __init__(self, name, hunger=30, happiness=60):
        super().__init__(name, hunger, happiness)
        self.scratch_count = 0

    def scratch(self):
        self.feed_count = 0  # Reset feed count
        self.play_count = 0  # Reset play count
        self.play_locked = False  # Unlock play
        self.action_count += 1  # Increment action count
        self.happiness = max(0, min(self.happiness - 5, 100))  # Decrease happiness by 5
        if random.random() < 0.1:  # 10% chance to scratch player
            message = f"{Fore.RED}😾 {self.name} scratches you in fear! Blood drips as it stares.{Style.RESET_ALL}"
            print(f"{message}\n{Fore.MAGENTA}What do you do? (yell/comfort):{Style.RESET_ALL}")
            choice = input().strip().lower()
            if choice == "yell":
                self.happiness = 1
                return True, f"{Fore.RED}😡 You yell at {self.name}! It hisses, eyes full of hate. Happiness: 1/100 😿{Style.RESET_ALL}\n{self._check_status()[1]}"
            elif choice == "comfort":
                self.happiness = 90
                return True, f"{Fore.GREEN}🤗 You comfort {self.name}. It purrs softly, forgiving you. Happiness: 90/100 😺{Style.RESET_ALL}\n{self._check_status()[1]}"
            else:
                return True, f"{Fore.RED}❌ Invalid choice. {self.name}’s claws gleam... Happiness: {self.happiness}/100 😿{Style.RESET_ALL}\n{self._check_status()[1]}"
        self.scratch_count += 1
        self.happiness = max(0, min(self.happiness + 10, 100))  # Increase happiness by 10
        message = f"{Fore.RED}😾 {self.name} slashes wildly! 'Next is your throat.' Scratch count: {self.scratch_count} 🩸{Style.RESET_ALL}" if self.scratch_count > 3 else f"{Fore.YELLOW}😺 {self.name} scratched something! Scratch count: {self.scratch_count} 🐾{Style.RESET_ALL}"
        continue_game, status_message = self._check_status()
        return continue_game, f"{message}\n{status_message}"


def display_rules():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.RED}Rules:{Style.RESET_ALL}")
    print(f"{Fore.RED}  - Don't overfeed{Style.RESET_ALL}")
    print(f"{Fore.RED}  - Don't overplay{Style.RESET_ALL}")
    print(f"{Fore.RED}  - Don't forget bathtime{Style.RESET_ALL}")
    print(f"{Fore.RED}  - Manage happiness{Style.RESET_ALL}\n")
    input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")


def display_menu(pet, activity_log=""):
    # Clear the screen for a fresh display
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Select art based on pet type, action count, and happiness
    pet_art_list = DOG_ART if isinstance(pet, Dog) else CAT_ART
    if pet.action_count >= 3 and random.random() < 0.1:  # 10% chance for demonic art after 3 actions
        pet_art = pet_art_list[1]  # Demonic
    elif pet.happiness <= 20 and random.random() < 0.3:  # 30% chance for normal art when happiness <= 20
        pet_art = pet_art_list[0]  # Normal
    else:  # ~60% chance for sleeping art (default preference)
        pet_art = pet_art_list[2]  # Sleeping
    
    # Display menu with pet art and activity log
    print(f"{Fore.CYAN}╔════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║         {pet.name}'s Pet Menu          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  🍽️ feed   - Feed your pet                ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  🎾 play   - Play with your pet            ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  📊 status - Show pet status               ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  🚪 quit   - Quit the game                 ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  🛁 bath   - Give your pet a bath          ║{Style.RESET_ALL}")
    if isinstance(pet, Dog):
        print(f"{Fore.CYAN}║  🏆 trick  - Teach your dog a trick        ║{Style.RESET_ALL}")
    elif isinstance(pet, Cat):
        print(f"{Fore.CYAN}║  🐾 scratch- Let your cat scratch          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{pet_art}\n")
    if activity_log:
        print(f"{Fore.MAGENTA}═╣ Activity Log ╠═{Style.RESET_ALL}")
        print(activity_log.strip())


def main():
    display_rules()  # Show simple rules before name input
    print(f"{Fore.CYAN}Welcome to the Pet Simulator! {Style.RESET_ALL}")
    name = input(f"{Fore.MAGENTA}Name your pet: 🐾{Style.RESET_ALL} ").strip()
    if not name:
        print(f"{Fore.RED}❌ No name? It was just one question...{Style.RESET_ALL}")
        return main()

    while True:
        option = input(f"{Fore.MAGENTA}Choose your pet: 🐶 dog or 😺 cat?{Style.RESET_ALL} ").strip().lower()
        if option in ["dog", "cat"]:
            break
        print(f"{Fore.RED}❌ Only dogs or cats in this realm!{Style.RESET_ALL}")

    pet = Dog(name) if option == "dog" else Cat(name)
    print(f"{Fore.GREEN}☠️ You’ve unleashed a {option} named {pet.name}! It knows your fears... 🐾{Style.RESET_ALL}")

    activity_log = ""
    while True:
        display_menu(pet, activity_log)  # Show menu with pet art and activity log
        action = input(f"{Fore.MAGENTA}Choose an action:{Style.RESET_ALL} ").strip().lower()
        continue_game = True
        activity_log = ""
        if action == "feed":
            continue_game, activity_log = pet.feed()
        elif action == "play":
            continue_game, activity_log = pet.play()
        elif action == "status":
            continue_game, activity_log = pet.status()
        elif action == "bath":
            continue_game, activity_log = pet.bath()
        elif action == "trick" and isinstance(pet, Dog):
            continue_game, activity_log = pet.learn_trick()
        elif action == "scratch" and isinstance(pet, Cat):
            continue_game, activity_log = pet.scratch()
        elif action == "quit":
            activity_log = f"{Fore.GREEN}🚪 You escape! {pet.name}’s curse lingers... 😿{Style.RESET_ALL}"
            display_menu(pet, activity_log)
            break
        else:
            activity_log = f"{Fore.RED}❌ Invalid action. {pet.name}’s eyes narrow...{Style.RESET_ALL}"
        if not continue_game:
            display_menu(pet, activity_log)  # Show game-over message in activity log
            input(f"{Fore.MAGENTA}Press Enter to restart...{Style.RESET_ALL}")
            activity_log = f"{Fore.RED}🔄 Restarting... Choose better next time.{Style.RESET_ALL}"
            display_menu(pet, activity_log)
            main()
            break


if platform.system() != "Emscripten":
    if __name__ == "__main__":
        main()