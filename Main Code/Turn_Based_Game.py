from tkinter import *
from PIL import Image, ImageTk
import random
try:
    import pygame
    pygame.mixer.init()
    MUSIC_ENABLED = True
except Exception:
    MUSIC_ENABLED = False
pygame.mixer.init()
class MusicManager():
    def __init__(self):
        self._current_track = None


    def play_music(self, track_path, loop=True):
        if not MUSIC_ENABLED:
            return
        if self._current_track == track_path:
            return
        pygame.mixer.music.stop()
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play(-1 if loop else 0)
        self._current_track = track_path

    def stop(self):
        if not MUSIC_ENABLED:
            return
        pygame.mixer.music.stop()
        self._current_track = None

    def set_volume(self, volume):
        if not MUSIC_ENABLED:
            return
        pygame.mixer.music.set_volume(volume)

    def fade_out(self, milliseconds=2000):
        if not MUSIC_ENABLED:
            return
        pygame.mixer.music.fadeout(milliseconds)

music = MusicManager()
#music.set_volume(0.4)


root = Tk()
root.title("RPG")
root.geometry("1920x1200")
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.resizable(False, False)
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_client)


    def exit_client(self, event=None):
        if MUSIC_ENABLED:
            pygame.mixer.music.stop()
        root.destroy()

class Player():
    def __init__(self, hp, physical_attack, defense, potion):
        self._hp = hp
        self._max_hp = hp
        self._physical_attack = physical_attack
        self._defense = defense
        self._potion = potion

    def attack(self):
        return self._physical_attack

class Elf_Mage(Player):
    def __init__(self):
        super().__init__(hp=20, physical_attack=5, defense=5, potion=5)
        self._mana = 200
        self._max_mana = 200
        self._spell_attack = 35

    def attack(self):
        return self._physical_attack

    

class Warrior(Player):
    def __init__(self):
        super().__init__(hp=20, physical_attack=30, defense=50, potion=5)
        self._boost_def = self._defense + 20
        self._shield_block = 100
        self._is_blocking = False

    def attack(self):
        return self._physical_attack + 10

class Enemy():
    def __init__(self, hp, attack, shield):
        self._hp = hp
        self._max_hp = hp
        self._attack = attack
        self._shield = shield

class Normal(Enemy):
    def __init__(self):
        super().__init__(hp=100, attack=10, shield=20)


class Elite(Enemy):
    def __init__(self):
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
    def __init__(self):
        super().__init__(hp=500, attack=250, shield=200)
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

class BattleWindow(Frame):
    def __init__(self, master, player):
        self._master = master
        self._player = player
        self._wave = 1
        self._enemy = Normal()
        self._player_turn = True
        self._log_messages = []

        self._enemy_images = {
            1: "Pictures/Enemies/2nd_Monster_design.png",  
            2: "Pictures/Enemies/Kuhren.png",               
            3: "Pictures/Enemies/Reginald.png",          
}

        self._canvas = Canvas(master, highlightthickness=0, bg="#1a1a2e")
        self._canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
 
        bg = Image.open("Pictures/Background/BG_Temp_Template.png").convert("RGBA")
        bg = bg.resize((1280, 720), Image.LANCZOS)
        bg_copy = bg.copy()
 
        if isinstance(player, Elf_Mage):
            p_img = Image.open("Pictures/Player/Mage_Elf.png").convert("RGBA")
        else:
            p_img = Image.open("Pictures/Player/Warrior_Class.png").convert("RGBA")
        p_img = p_img.resize((160, 200), Image.LANCZOS)
        bg_copy.paste(p_img, (100, 430), mask=p_img.split()[3])
        
        self._bg_photo = ImageTk.PhotoImage(bg_copy)
        self._canvas.create_image(0, 0, anchor=NW, image=self._bg_photo)
        self._canvas.image = self._bg_photo


        e_img = Image.open("Pictures/Enemies/2nd_Monster_design.png").convert("RGBA")
        e_img = e_img.resize((220, 260), Image.LANCZOS)
        self._enemy_photo = ImageTk.PhotoImage(e_img)
        self._enemy_sprite = self._canvas.create_image(900, 360, anchor=NW, image=self._enemy_photo)
    
 
        self._build_hud()
        self._build_buttons()
        self._update_hud()
 
 
    def _build_hud(self):
        hud_bg = "#1a1a2e"
 
        self._canvas.create_rectangle(10, 620, 340, 710, fill=hud_bg, outline="#FFD700", width=2)
        self._canvas.create_text(20, 630, anchor=NW, text=self._player.__class__.__name__,
                                  fill="white", font=("Arial", 11, "bold"))
        self._hp_bar_bg   = self._canvas.create_rectangle(20, 650, 320, 668, fill="#555", outline="")
        self._hp_bar      = self._canvas.create_rectangle(20, 650, 320, 668, fill="#e74c3c", outline="")
        self._hp_text     = self._canvas.create_text(170, 659, fill="white",
                                                      font=("Arial", 9, "bold"), text="")
        if isinstance(self._player, Elf_Mage):
            self._mp_bar_bg = self._canvas.create_rectangle(20, 675, 320, 690, fill="#555", outline="")
            self._mp_bar    = self._canvas.create_rectangle(20, 675, 320, 690, fill="#3498db", outline="")
            self._mp_text   = self._canvas.create_text(170, 683, fill="white",
                                                        font=("Arial", 9, "bold"), text="")
        else:
            self._mp_bar = self._mp_bar_bg = self._mp_text = None
 
        self._canvas.create_rectangle(940, 20, 1270, 100, fill=hud_bg, outline="#FF4444", width=2)
        self._canvas.create_text(950, 28, anchor=NW, text="Enemy",
                                  fill="white", font=("Arial", 11, "bold"))
        self._ehp_bar_bg = self._canvas.create_rectangle(950, 50, 1260, 68, fill="#555", outline="")
        self._ehp_bar    = self._canvas.create_rectangle(950, 50, 1260, 68, fill="#e74c3c", outline="")
        self._ehp_text   = self._canvas.create_text(1105, 59, fill="white",
                                                     font=("Arial", 9, "bold"), text="")
 
        self._canvas.create_rectangle(10, 530, 540, 615, fill=hud_bg, outline="#FFD700", width=1)
        self._log_text = self._canvas.create_text(20, 540, anchor=NW, fill="#FFD700",
                                                   font=("Arial", 10), text="", width=510)
 
    def _update_hud(self):
        p_ratio = max(0, self._player._hp / self._player._max_hp)
        self._canvas.coords(self._hp_bar, 20, 650, 20 + int(300 * p_ratio), 668)
        self._canvas.itemconfig(self._hp_text,
                                 text=f"HP: {self._player._hp} / {self._player._max_hp}")
 
        if self._mp_bar and isinstance(self._player, Elf_Mage):
            m_ratio = max(0, self._player._mana / self._player._max_mana)
            self._canvas.coords(self._mp_bar, 20, 675, 20 + int(300 * m_ratio), 690)
            self._canvas.itemconfig(self._mp_text,
                                     text=f"MP: {self._player._mana} / {self._player._max_mana}")
 
        e_ratio = max(0, self._enemy._hp / self._enemy._max_hp)
        self._canvas.coords(self._ehp_bar, 950, 50, 950 + int(310 * e_ratio), 68)
        self._canvas.itemconfig(self._ehp_text,
                                 text=f"HP: {self._enemy._hp} / {self._enemy._max_hp}")
 
    def _log(self, msg):
        self._log_messages.append(msg)
        if len(self._log_messages) > 3:
            self._log_messages.pop(0)
        self._canvas.itemconfig(self._log_text, text="\n".join(self._log_messages))
 
 
    def _build_buttons(self):
        self._btn_frame = Frame(self._master, bg="#1a1a2e")
        self._btn_frame.place(relx=0.5, rely=0.93, anchor=CENTER)
 
        btn_style = {"width": 12, "font": ("Arial", 12, "bold"), "fg": "white", "cursor": "hand2"}

        
        self._atk_btn = Button(self._btn_frame, text="⚔ Attack",  bg="#8B0000",
                                command=self._on_attack, **btn_style)
        self._spl_btn = Button(self._btn_frame, text="✨ Spell",   bg="#00008B",
                                command=self._on_spell,  **btn_style)
        self._pot_btn = Button(self._btn_frame, text="🧪 Potion",  bg="#006400",
                                command=self._on_potion, **btn_style)
        
        

        
        self._atk_btn.grid(row=0, column=0, padx=10)
        self._spl_btn.grid(row=0, column=1, padx=10)
        self._pot_btn.grid(row=0, column=2, padx=10)

        if isinstance(self._player, Warrior):
            self._blockbtn = Button(self._btn_frame, text="Block", bg="#4B0082", command=self._on_block, **btn_style)
            self._blockbtn.grid(row=0, column=3, padx=10)
        else:
            self._blockbtn = None
 
        self._karen_frame = Frame(self._master, bg="#1a1a2e")
        btn_k = {"width": 14, "font": ("Arial", 12, "bold"), "fg": "white",
                 "bg": "#8B4513", "cursor": "hand2"}
        Button(self._karen_frame, text="📢 Call Manager", command=lambda: self._karen_choice("manager"),  **btn_k).grid(row=0, column=0, padx=8)
        Button(self._karen_frame, text="🙏 Apologize",    command=lambda: self._karen_choice("apologize"),**btn_k).grid(row=0, column=1, padx=8)
        Button(self._karen_frame, text="🧾 Show Receipt", command=lambda: self._karen_choice("receipt"),  **btn_k).grid(row=0, column=2, padx=8)
        Button(self._karen_frame, text="🏃 Run Away",     command=lambda: self._karen_choice("run"),      **btn_k).grid(row=0, column=3, padx=8)
 
    def _show_karen_buttons(self):
        self._btn_frame.place_forget()
        self._karen_frame.place(relx=0.5, rely=0.93, anchor=CENTER)
 
    def _show_normal_buttons(self):
        self._karen_frame.place_forget()
        self._btn_frame.place(relx=0.5, rely=0.93, anchor=CENTER)
 
 
    def _set_buttons_state(self, state):
        for btn in [self._atk_btn, self._spl_btn, self._pot_btn]:
            btn.config(state=state)
        if self._blockbtn:
            self._blockbtn.config(state=state)

    def _on_block(self):
        if isinstance(self._player, Warrior):
            self._player._is_blocking = True
            self._log("You brace for impact! Blocking the next attack!")
            self._enemy_turn()
 
    def _on_attack(self):
        dmg = max(1, self._player.attack() - self._enemy._shield)
        self._enemy._hp -= dmg
        self._log(f"⚔ You attacked for {dmg} damage!")
        self._update_hud()
        self._check_enemy_defeated()
 
    def _on_spell(self):
        if isinstance(self._player, Elf_Mage):
            if self._player._mana >= 20:
                dmg = self._player._spell_attack
                self._enemy._hp  -= dmg
                self._player._mana -= 20
                self._log(f"✨ Spell hit for {dmg} damage! (shield bypassed)")
                self._update_hud()
                self._check_enemy_defeated()
            else:
                self._log("❌ Not enough mana!")
        else:
            self._log("❌ This character can't cast spells!")
 
    def _on_potion(self):
        if self._player._potion > 0:
            heal = 100
            self._player._hp = min(self._player._hp + heal, self._player._max_hp)
            self._player._potion -= 1
            self._log(f"🧪 Used a potion! HP restored to {self._player._hp}")
            self._update_hud()
            self._enemy_turn()
        else:
            self._log("❌ No potions left!")

    def _next_wave(self):
        self._wave += 1


        if self._wave == 2:
            self._enemy = Elite()
            self._e_image = ""
            self._log("A disturbance is in the air...The Kuhren appears!")

            music.fade_out(800)
            self._master.after(800, lambda: music.play_music("Music/Kuhren_Music.mp3"))
            
            if isinstance(self._player, Elf_Mage):
                self._player._max_hp += 100
                self._player._hp = self._player._max_hp
                self._player._defense += 80
                self._player._spell_attack += 100
                self._player._mana = self._player._max_mana
                self._log("Leveled up! Mage has regenerated mana!")

            elif isinstance(self._player, Warrior):
                self._player._max_hp += 100
                self._player._hp = self._player._max_hp
                self._player._defense += 150
                self._player._shield_block += 80
                self._player._physical_attack += 120
                self._log("Leveled up! You gained better equipment!")

        elif self._wave == 3:
            self._enemy = Boss()
            self._log("Time seems to stop around you...The Gatekeeper of Time, Reginald, appears!")
            
            music.fade_out(800)
            self._master.after(800, lambda: music.play_music("Music/Boss.mp3"))


            if isinstance(self._player, Elf_Mage):
                self._player._max_hp += 100
                self._player._hp = self._player._max_hp
                self._player._defense += 60
                self._player._spell_attack += 60
                self._player._mana = self._player._max_mana
                self._log("Leveled up! Mage has regenerated mana!")

            elif isinstance(self._player, Warrior):
                self._player._max_hp += 100
                self._player._hp = self._player._max_hp
                self._player._defense += 50
                self._player._shield_block += 80
                self._player._physical_attack += 60
                self._log("Leveled up! You gained better equipment!")
        
        
        self._update_enemy_sprite()


        self._set_buttons_state(NORMAL)
        self._update_hud()

    def _update_enemy_sprite(self):
        path = self._enemy_images[self._wave]
        e_img = Image.open(path).convert("RGBA")
        e_img = e_img.resize((220, 260), Image.LANCZOS)
        self._enemy_photo = ImageTk.PhotoImage(e_img)
        self._canvas.itemconfig(self._enemy_sprite, image=self._enemy_photo)
 
    def _check_enemy_defeated(self):
        if self._enemy._hp <= 0:
            self._enemy._hp = 0
            self._update_hud()
            self._log("🏆 Enemy defeated! You win!")
            self._set_buttons_state(DISABLED)

            if self._wave == 1:
                self._log("Enemy has been defeated!")
                self._show_victory_message(title="Enemy Defeated!", message="You defeated a Normal Enemy!", next_action=self._next_wave)

            elif self._wave ==2:
                self._log("The Kuhren has been defeated!")
                self._show_victory_message(title="ELite Defeated!", message="You defeated an Elite Enemy!", next_action=self._next_wave)
            elif self._wave ==3:
                self._log("Reginald has been defeated!")
                self._show_victory_message(title="Reggie Defeated!", message="You defeated the Boss!", next_action=MainMenuScreen(root))
                music.fade_out(800)

        else:
            self._enemy_turn()
 
    def _enemy_turn(self):
        if isinstance(self._enemy, Normal):
            dmg = max(0,self._enemy._attack -  self._player._defense)
            self._log(f"The monster attacks for: {dmg}!")
            return

        if isinstance(self._enemy, Elite) and self._enemy.check_OHK():
            self._log("⚠ The Kuhren is calling someone! React!")
            self._show_karen_buttons()
            return
        
        if isinstance(self._player, Warrior) and self._player._is_blocking:
            dmg = max(0, self._enemy._attack - self._player._defense)
            self._log(f"You blocked! Reduced damge: {dmg}!")
            self._player._is_blocking = False
        else:
            dmg = max(1, self._enemy._attack - self._player._defense)
            self._log(f"👹 Enemy attacked for {dmg} damage!")

        self._player._hp -= dmg
        self._update_hud()
 
        if self._player._hp <= 0:
            self._player._hp = 0
            self._update_hud()
            self._log("💀 You were defeated... Game Over!")
            self._set_buttons_state(DISABLED)
            
            music.fade_out(800)
            self._show_message(title="Game Over!", message="You were defeated!", next_action=MainMenuScreen(root))
 
    def _karen_choice(self, choice):
        survived, msg = self._enemy.resolve_OHK(choice)
        self._log(msg)
        self._show_normal_buttons()
        if not survived:
            self._player._hp = 0
            self._update_hud()
            self._log("💀 You were arrested! Game Over!")
            self._set_buttons_state(DISABLED)

            self._master.after(800, lambda: music.play_music("Music/Comedic_Death.mp3"))

            self._show_message(title="Game Over!", message="You were arrested!", next_action=MainMenuScreen(root))

    def _show_message(self, title, message, next_action):
            popup = Frame(self._master, bg="#1a1a2e", bd=4, relief=RIDGE)
            popup.place(relx=0.5, rely=0.5, anchor=CENTER, width=420, height=220)

            Label(popup, text=title, font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=(20, 5))

            Label(popup, text=message, font=("Arial", 20, "bold"), bg="#1a1a2e", fg="white", justify=CENTER).pack(pady=5)

            def on_continue():
                popup.destroy()
                if next_action:
                    next_action()

            btn_text = "Finished!"
            Button(popup, text=btn_text, font=("Arial", 20, "bold"), 
               bg="#4CAF50", fg="white", width=16, cursor="hand2",
               command=on_continue).pack(pady=15)


    def _show_victory_message(self, title, message, next_action):
        popup = Frame(self._master, bg="#1a1a2e", bd=4, relief=RIDGE)
        popup.place(relx=0.5, rely=0.5, anchor=CENTER, width=420, height=220)

        Label(popup, text=title, font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=(20, 5))

        Label(popup, text=message, font=("Arial", 20, "bold"), bg="#1a1a2e", fg="white", justify=CENTER).pack(pady=5)

        def on_continue():
            popup.destroy()
            if next_action:
                next_action()

        btn_text = "New enemy" if next_action else "Finished!"
        Button(popup, text=btn_text, font=("Arial", 20, "bold"), 
               bg="#4CAF50", fg="white", width=16, cursor="hand2",
               command=on_continue).pack(pady=15) 
 
 
class CharacterSelectScreen:
    def __init__(self, master, on_confirm):
        self._master     = master
        self._on_confirm = on_confirm
        self._selected   = None
 
        self._frame = Frame(master, bg="#1a1a2e")
        self._frame.place(relx=0, rely=0, relwidth=1, relheight=1)
 
        Label(self._frame, text="Choose Your Character",
              font=("Arial", 28, "bold"), bg="#1a1a2e", fg="white").pack(pady=30)
 
        cards_frame = Frame(self._frame, bg="#1a1a2e")
        cards_frame.pack(fill=BOTH, expand=True)

        inner = Frame(cards_frame, bg="#1a1a2e")
        inner.pack(anchor=CENTER, pady=40)
 
        self._stats_label = Label(self._frame, text="", font=("Arial", 13),
                                   bg="#1a1a2e", fg="#FFD700", justify=LEFT)
        self._stats_label.pack(pady=10)
 
        self._confirm_btn = Button(self._frame, text="✔ Confirm Selection",
                                    font=("Arial", 13, "bold"), bg="#4CAF50",
                                    fg="white", width=20, command=self._confirm)
 
        mage_img = Image.open("Pictures/Player/Mage_Elf.png").convert("RGBA").resize((180, 180), Image.LANCZOS)
        warr_img = Image.open("Pictures/Player/Warrior_Class.png").convert("RGBA").resize((180, 180), Image.LANCZOS)
        self._mage_photo = ImageTk.PhotoImage(mage_img)
        self._warr_photo = ImageTk.PhotoImage(warr_img)
 
        self._characters = [
            {"name": "Elf Mage",  "image": self._mage_photo, "class": Elf_Mage,
             "stats": "❤ HP: 20   ✨ Mana: 200\n⚔ Phys Attack: 5   🔮 Spell Attack: 35\n🛡 Defense: 5   🧪 Potions: 5",
             "desc":  "Fragile but powerful. Spells bypass enemy shields."},
            {"name": "Warrior",   "image": self._warr_photo, "class": Warrior,
             "stats": "❤ HP: 20   ⚔ Phys Attack: 30\n🛡 Defense: 50   🔰 Shield Block: 100\n🧪 Potions: 5",
             "desc":  "Tough frontline fighter. High defense and shield block."},
        ]
 
        self._card_frames = []
        for i, char in enumerate(self._characters):
            self._build_card(inner, char, i)
 
    def _build_card(self, parent, char, index):
        card = Frame(parent, bg="#16213e", bd=3, relief=RIDGE, width=260, height=380)
        card.grid(row=0, column=index, padx=40)
        card.pack_propagate(False)
 
        Button(card, image=char["image"], bg="#16213e", activebackground="#0f3460",
               bd=0, cursor="hand2",
               command=lambda c=char, f=card: self._select(c, f)).pack(pady=(15, 5))
 
        Label(card, text=char["name"], font=("Arial", 15, "bold"),
              bg="#16213e", fg="white").pack()
        Label(card, text=char["desc"], font=("Arial", 9), bg="#16213e",
              fg="#aaaaaa", justify=CENTER, wraplength=210).pack(pady=4)
 
        self._card_frames.append(card)
 
    def _select(self, char, card):
        self._selected = char
        for c in self._card_frames:
            c.config(bg="#16213e", bd=3)
        card.config(bg="#FFD700", bd=4)
        self._stats_label.config(text=f"── {char['name']} Stats ──\n{char['stats']}")
        self._confirm_btn.pack(pady=10)
 
    def _confirm(self):
        if self._selected:
            self._frame.destroy()
            self._on_confirm(self._selected["class"]())
 
 
 
class MainMenuScreen:
    def __init__(self, master):
        self._master = master
 
        self._frame = Frame(master, bg="#1a1a2e")
        self._frame.place(relx=0, rely=0, relwidth=1, relheight=1)
 
        Label(self._frame, text="⚔  RPG Game  ⚔",
              font=("Arial", 42, "bold"), bg="#1a1a2e", fg="#FFD700").pack(pady=120)
 
        Label(self._frame, text="A turn-based adventure awaits...",
              font=("Arial", 14), bg="#1a1a2e", fg="#aaaaaa").pack()
 
        Button(self._frame, text="▶  New Game", font=("Arial", 16, "bold"),
               bg="#4CAF50", fg="white", width=16, cursor="hand2",
               command=self._new_game).pack(pady=30)
 
        Button(self._frame, text="✖  Quit", font=("Arial", 16, "bold"),
               bg="#8B0000", fg="white", width=16, cursor="hand2",
               command=master.destroy).pack()
 
    def _new_game(self):
        self._frame.destroy()
        CharacterSelectScreen(self._master, self._on_confirmed)
 
    def _on_confirmed(self, player):
        music.fade_out(800)
        self._master.after(800, lambda: music.play_music("Music/battle.ogg"))
        self._master.after(900, lambda: music.set_volume(0.4))
        BattleWindow(self._master, player)
 

app = Window(root)
MainMenuScreen(root)
root.mainloop()