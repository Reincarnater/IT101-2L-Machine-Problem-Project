from tkinter import *
from PIL import Image, ImageTk
import random


root = Tk()
root.title("RPG")

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.resizable(False, False)
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_client)


    def exit_client(self, event=None):
        exit()

# Create a class for both enemy and player base stats
# After that, create individual classes for the provided player bases (e.g. Elf mages get a plus on mana and spell attacks, and etc.)
# Elite enemies should have higher stats than the base enemy stats, and grant them a randomized one-hit attack.
        
class Player():
    def __init_player__(self, hp, physical_attack, defense, potion):
        self._hp = hp
        self._max_hp = hp
        self._physical_attack = physical_attack
        self._defense = defense
        self._potion = potion

class Elf_Mage(Player):
    def __init_mage__(self):
        super().__init__(hp=20, physical_attack=5, defense=5, potion=5)
        self._mana = 200
        self._max_mana = 200
        self._spell_attack = 35

class Warrior(Player):
    def __init_warrior__(self):
        super().__init__(hp=20, physical_attack=30, defense=50, potion=5)
        self._boost_def = self._defense + 20
        self._shield_block = 100

class Enemy():
    def __init_enemy__(self, hp, attack, shield):
        self._hp = hp
        self._attack = attack
        self._shield = shield

class Normal(Enemy):
    def __init_normal__(self):
        super().__init__(hp=100, attack=10, shield=20)


class Elite(Enemy):
    def __init_elite__(self):
        super().__init__(hp=250, attack=20, shield=30)
        self._name = "The Kuhren"
        self._OHK = True
        self._ohk_triggered = False

    def check_OHK(self):
        if random.random() < 0.30:
            self._ohk_triggered = True
            return True
        return False

    def resolve_OHK(self, player_choice):
        outcomes = {
            "manager": {
                "success_chance": 0.70,  # usually works, Karen hates this
                "success_msg": "You called the manager! The Kuhren backs down, furious!",
                "fail_msg":    "The manager sided with The Kuhren! The cops arrive!"
            },
            "apologize": {
                "success_chance": 0.50,  # 50/50, Karen might not accept
                "success_msg": "You apologized profusely. The Kuhren reluctantly lets it go... for now.",
                "fail_msg":    "The Kuhren doesn't accept your apology! The cops arrive!"
            },
            "receipt": {
                "success_chance": 0.90,  # hard evidence, almost always works
                "success_msg": "You showed your receipt! The Kuhren has no case. She storms off!",
                "fail_msg":    "The Kuhren ignores the receipt! The cops arrive anyway!"
            },
            "run": {
                "success_chance": 0.40,  # risky, might get caught
                "success_msg": "You bolted out of there! The Kuhren screams in the distance!",
                "fail_msg":    "You weren't fast enough! The cops caught you!"
            }
        }

        option = outcomes[player_choice]
        if random.random() < option["success_chance"]:
            self._ohk_triggered = False
            return True, option["success_msg"]
        else:
            return False, option["fail_msg"]

class Boss(Enemy):
    def __init_boss__(self):
        super().__init__(hp=500, attack=250, shield=250)
        self._max_hp = 500
        self._phase = 1
        self._name = "Reginald"

        
    def check_phase(self):
        if self._phase == 1 and self._hp <=250:
            self._phase = 2
            self._attack += 30
            self._shield += 50
            return "Boss has entered Phase 2!"

        elif self._phase == 2 and self._hp <=50:
            self._phase = 3
            self._attack += 50
            self._shield -= 200
            return "Boss discarded his shield! Final Phase!"
        
        return None

root.geometry("1920x1200")
app = Window(root)

BG_Canvas = Canvas(root, highlightthickness=0)
BG_Canvas.pack(fill=BOTH, expand=True)

BG_image = Image.open("Pictures/Background/BG_Temp_Template.png")
BG_Copy = BG_image.copy()

Player_image = Image.open("Pictures/Player/Mage_Elf.png")
elf_x, elf_y = -15, 650
BG_Copy.paste(Player_image, (elf_x, elf_y), mask=Player_image.split()[3])

Enemy_image = Image.open("Pictures/Enemies/2nd_Monster_design.png").resize((400, 450), Image.Resampling.LANCZOS)
NMonster_x, NMonster_y = 850, 650
BG_Copy.paste(Enemy_image, (NMonster_x, NMonster_y), mask=Enemy_image.split()[3])

final_image = ImageTk.PhotoImage(BG_Copy)

BG_Canvas.create_image(-70, -450, anchor=NW, image=final_image)
BG_Canvas.image = final_image

root.mainloop()