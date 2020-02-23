import tkinter as Tk
import time
from PIL import ImageTk, Image
 
class Model():
    def __init__(self):
        self.energy_level = 1
        self.food_level = 100
        self.current_hour = 6
        self.weekday_index = 0
        self.weekdays = ["Monday", "Tuesday", "Wednessday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.alive = True
        self.message = ""
        self.timeout = 600
        self.start_time = time.time()
        self.level_index = 0
        self.level_name_and_speed = [
            ["Level 1 Judgemental Shoelace",     600, "./1.jpg"],
            ["Level 2 Screaming Worm Boi",       500, "./2.jpg"],
            ["Level 3 Uggo But Still Luvo Snek", 400, "./3.jpg"],
            ["Level 4 Shake Snek",               300, "./4.jpg"],
            ["Level 5 Cober",                    200, "./5.jpg"],
            ["Level 6 Danger Noodle",            100, "./6.jpg"],
            ["Level 7 Nope Rope",                 50, "./7.jpg"],
            ["Level 8 Caution Ramen",             30, "./8.jpg"],
            ["Level 9 Hazard Spaghetti",          20, "./9.png"],
            ["Level 10 Murder Spagurder",         10, "./10.jpg"],
        ]

class View():
    def __init__(self, master):
        self.frame = Tk.Frame(master)
        self.level_label = Tk.Label(master, text="", font='Arial 18 bold')
        self.img = Image.open("./1.jpg")
        self.img = self.img.resize((400, 400))
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Tk.Label(master, image = self.img)
        self.info_label = Tk.Label(master, text="")
        self.button_feed = Tk.Button(self.frame, text="Feed")
        self.button_walk = Tk.Button(self.frame, text="Walk")
        self.button_sleep = Tk.Button(self.frame, text="Sleep")

        self.frame.pack(side = "bottom")
        self.level_label.pack(side = "top")
        self.button_feed.pack(side  = "right")
        self.button_walk.pack(side  = "right")
        self.button_sleep.pack(side  = "right")
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.info_label.pack(side  = "bottom")


class Controller():
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root)
        self.view.button_feed.bind("<Button>",self.feed)
        self.view.button_walk.bind("<Button>",self.walk)
        self.view.button_sleep.bind("<Button>",self.sleep)

    def timer(self):
        self.setToNextHour()
        self.healthCheck()
        self.levelCheck()
        self.updateInfoLabels()
        self.updateImage()

        delay = self.model.level_name_and_speed[self.model.level_index][1]
        if self.model.alive == True:
            self.root.after(delay, self.timer)
        else:
            self.updateInfoLabels()

    def updateImage(self):
        path = self.model.level_name_and_speed[self.model.level_index][2]
        self.view.panel.destroy()
        img = Image.open(path)
        img = img.resize((400, 400))
        self.view.img = ImageTk.PhotoImage(img)
        self.view.panel = Tk.Label(self.root, image = self.view.img)
        self.view.panel.pack(side = "bottom", fill = "both", expand = "yes")
  
    def updateInfoLabels(self):
        hour_box = self.model.current_hour
        week_box = self.model.weekdays[self.model.weekday_index]

        message = f"ENERGY: {self.model.energy_level}\nFOOD: {self.model.food_level}\n\nHOUR: {hour_box}\nWEEKDAY: {week_box}\n{self.model.message}"

        self.view.info_label["text"] = message

        self.view.level_label['text'] = self.levelCheck()

    # Sæt til næste time
    def setToNextHour(self):
        self.model.current_hour += 1
        self.model.food_level -= 1
        self.model.energy_level += 1
        self.checkHourOverflow()

    # hvis current hour er oversteget 21 så skal den sættes til 6 igen
    def checkHourOverflow(self):
        if self.model.current_hour > 21:
            self.model.current_hour = 6
            self.model.weekday_index += 1
            self.checkWeekOverflow()

    # Tjek om weekday_index er oversteget 6
    def checkWeekOverflow(self):
        if self.model.weekday_index > 6:
            self.model.weekday_index = 0

    # Hvis energy_level eller food_level er 0 eller over 100, skal kæledyret dø   
    def healthCheck(self): 
        if self.model.energy_level <= 0:
            self.kill("Your snek lost all its energy and died..")

        if self.model.food_level <= 0:
            self.kill("Your snek died of hunger..")

        if self.model.energy_level > 100:
            self.kill("Your snek cooked from the inside..")

        if self.model.food_level > 100:
            self.kill("Your snek became too fat..")

    # Sætter level string og timeout efter hvor mange sekunder der er gået siden scriptet er startet
    def levelCheck(self):

        delta_time = round(time.time() - self.model.start_time)

        if delta_time % 10 == 0:
            level_index = int(delta_time/10)
            self.model.level_index = level_index
            self.model.timeout = self.model.level_name_and_speed[level_index][1]
            return self.model.level_name_and_speed[level_index][0]

    # Sørger for at while-løkken i main funktionen stopper med at loop'e
    def kill(self, reason):
        self.model.message = reason + "\ni don't feel so good, Mr. Stark"
        self.model.alive = False

    # Plus food_level med 10 og vis at der spises
    def feed(self, event):
        self.model.food_level += 10
        self.model.message = "Yum yum yum"

    # Minus energy_level med 10 og vis at der gåes.
    def walk(self, event):
        self.model.energy_level -= 10
        self.model.message = "*Breathing intensifies"

    # Plus energy_level med 10 og vis at der soves
    def sleep(self, event):
        self.model.energy_level += 10
        self.model.message = "*Yaaawn"

    def run(self):
        self.root.title("SNEKBOX")
        self.root.deiconify()
        self.timer()
        self.root.mainloop()
 
c = Controller()
c.run()