from tkinter import *
from PIL import Image, ImageTk
import os


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
    def init_player(self, hp, attack, defense, potion):
        self._hp = hp
        self._attack = attack
        self._defense = defense
        self._potion = potion


class Enemy():
    def init_enemy(self, hp, attack, shield):
        self._hp = hp
        self._attack = attack
        self._shield = shield


        
bg_image = Image.open("Pictures/Background/BG_Temp_Template.png").convert("RGBA")
photo = ImageTk.PhotoImage(bg_image)

background_label = Label(root, image=photo)
background_label.image = photo
background_label.place(x=0, y=0, relwidth=1, relheight=1)



player_image = Image.open("Pictures/Player/Mage_Elf.png").convert("RGBA")

background_copy = bg_image.copy()
elf_x, elf_y = 400, 500
background_copy.paste(player_image, (elf_x, elf_y), mask=player_image.split()[3])

final_image = ImageTk.PhotoImage(background_copy)

root.geometry("1920x1200")
app = Window(root)
root.mainloop()


