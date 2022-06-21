#modules dans la librairie standard
import datetime
from urllib.request import urlopen
import json
from random import choice, shuffle
import webbrowser
from time import time, sleep
import os
from pprint import pprint
from tkinter import *
#modules installés avec pip
import pyttsx3
from fuzzywuzzy import process

#modules installés avec pip et utilisant internet
Internet = None
try:
    urlopen("http://google.com")  # on check la connexion Internet
except:
    Internet = False
    print("Pas d'internet")
else:
    Internet = True
    print("Y a Internet")
    import pywhatkit as kit
    import wikipedia
    wikipedia.set_lang("fr")
    from speech_recognition import Recognizer, Microphone #API
    recognizer = Recognizer()

tk = Tk()
tk.title("Anubis")
gif = process.extract(".gif", os.listdir())[0][0]
if ".gif" in gif:
    Image = PhotoImage(file=gif)
    w = Canvas(tk, width=Image.width(), height=Image.height())
    w.create_image(0, 0, anchor= NW, image=Image)
else:
    w = Canvas(tk, width=300, height=300, bg="black")
w.pack()
w.update()
window_x = w.winfo_width() - 4
window_y = w.winfo_height() - 4
    
engine = pyttsx3.init()

inutile = ["stp", "s'il te plait", "mais", "et", "donc", "or", "ni", "car", "mon", "ma", "mes"]
synonyms = {"joke": ["blague", "vanne", "joke", "fais moi rire", "fais rire"],
            "cmd": ["terminal", "commande", "invite de commande", "cmd"],
            "repeat":["dis", "répète"],
            "salut":["bonjour", "salut", "bonsoir", "au revoir", "bye", "bonne nuit"],
            "heure": ["heure", "date", "quel jour", "le combien"],
            "Quit":["au revoir", "tais-toi", "dors", "eteins toi", "va dormir", "quitter le programme"],
            "Merci":["merci", "je te remercie", "merci beaucoup"],
            "music": ["musique", "met de la musique", "met la musique", "lance la musique"],
            "presentation": ["Qui es-tu", "t'es qui", "fais ta presentation", "presente toi"],
            "search":["cherche", "recherche", "google"],
            #Internet seulement
            "where":["où suis je", "je suis où", "on est où", "localisation", "localise", "position"],
            "Wiki":["Sur wikipedia", "d'apres wikipedia", "cherche sur wikipedia", "wikipedia"],
            "Ytb" : ["Sur Youtube", "Youtube", "video sur Youtube", "cherche sur Youtube"],
            "":["azertyuiopqsdfghjklmwxcvbn", ""],
            }


def say(texte):
    w.itemconfigure("t1", state="hidden")
    w.update()
    w.create_text(window_x//2, (window_y*3)//4, text="Anubis: "+texte, fill="#ff0000", tag="t1")
    tk.update()
    engine.say(texte)
    engine.runAndWait()

if Internet:
    def listen(bot_text="Parlez, Maitre!", r=recognizer):
        with Microphone() as source:
            r.adjust_for_ambient_noise(source)
            say(bot_text)
            t=time()
            audio = r.listen(source)
            print(time()-t)
        try:
            text = r.recognize_google(audio, language="fr-FR").lower()
            print("Maitre: "+text)
        except Exception as ex:
            print(ex)
        else:
            w.itemconfigure("t", state="hidden")
        return text


def callback():
    global btn
    if Internet:
        btn.destroy()
    text=listen()
    recognize(text)


def recognize(text):
    global btn, enter
    enter.destroy()
    if Internet:
        btn.destroy()
    w.itemconfigure("t", state="hidden")
    w.itemconfigure("t1", state="hidden")
    w.create_text(window_x//2, (window_y)//4, text="Maitre: "+text, fill="#44ff44", tag="t")
    tk.update()
    cmd = ('', 0)
    Text = text
    nom = ""
    for i in inutile:
        Text = Text.replace("i", "").strip()
    for i in synonyms:
        var = process.extract(Text, synonyms[i])[0]
        if var[1] >= cmd[1] and var[1] > 70:
            cmd = var
    cmd2 = cmd[0]
    for i in synonyms:
        if cmd[0] in synonyms[i]:
            cmd = i
            break
    if cmd == "Wiki":
        try:
            text = text.replace(cmd2, "")
        except:
            pass
    if text[:3].lower() in ["dis","dit"]:
        cmd = "repeat"
    execute(cmd, text)


def execute(cmd, text):
    global btn, enter
    if cmd == "heure":
        now = datetime.datetime.now()
        say("Il est actuellement "+str(now.hour) + ":" + str(now.minute)+", le "+str(now.day)+" "+["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"][now.month-1]+" "+str(now.year))
    elif cmd == "joke":
        say(choice(["Quelle est la difference entre Dieu et un chirurgien?\nDieu ne se prend pas pour un chirurgien",
                    "Comment s'appelle un boomerang qui ne revient pas? Un cintre"]))
    elif cmd == "salut":
        say("rebonjour à vous, grand maitre")
    elif cmd == "cmd":
        os.system("start cmd")
    elif cmd == "Merci":
        say("Je vous en prie Maitre")
    elif cmd == "Quit":
        say("Au revoir")
        quit()
    elif cmd == "repeat":
        say(text[3:])
    elif cmd == "music":
        l = os.listdir()
        shuffle(l)
        say("tout de suite")
        for i in l:
            if (".mp3" in i):
                os.system(i)
                break
        else:
            say("Vous n'avez pas de musique disponible")
        say(i)
    elif cmd == "presentation":
        say("Je suis votre humble serviteur, Anubis")
    elif Internet:
        if cmd == "Ytb":
            text = listen("Que voulez vous chercher sur Youtube?")
            say("A vos ordres")
            try:
                kit.playonyt(text)
            except Exception as ex:
                print(ex)
        elif cmd == "where":
            loc = json.loads(urlopen("https://ipinfo.io/json").read().decode())
            say("Vous etes actuellement aux environ de "+str(loc["loc"])+",\nsoit vers "+str(loc["city"])+" en "+str(loc["region"]))
        elif cmd == "Wiki":
            text=listen("Que voulez vous chercher sur wikipedia?")
            say(wikipedia.summary(text, sentences=2))
        elif cmd=="search":
            text = text.replace(text.split()[0], "")
            say(choice(["oui Maitre", "tout de suite Maitre"]))
            webbrowser.open("https://www.google.fr/search?q="+text)
        else:
            say(choice(["je n'ai pas tres bien compris votre question", "Je comprend"]))
    else:
        say(choice(["je n'ai pas tres bien compris votre question", "Je comprend"]))
        
    if Internet:
        btn = Button(tk, text="parler", command=callback)
        btn.pack()
    enter = Entry(tk)
    enter.pack()
    enter.bind("<Return>", entree)

def entree(event):
    global enter
    text=enter.get()
    recognize(text)

if Internet:
    btn = Button(tk, text="parler(audio)", command=callback)
    btn.pack()

enter = Entry(tk)
enter.pack()

enter.bind("<Return>", entree)
tk.update()
say("Bien le bonjour, Ô grand Maitre!")
tk.mainloop()

