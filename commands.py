import datetime
import json
import datetime
import json
from urllib.request import urlopen
from random import choice, shuffle
import webbrowser
import pyautogui as pg
import os
from pprint import pprint
from fuzzywuzzy import process
from common import *

INTERNET = None
last_mode = None

try:
    urlopen("http://google.com")  # on check la connexion Internet
except:
    INTERNET = False
    print("(Pas d'internet)")
else:
    INTERNET = True
    import pywhatkit as kit
    import wikipedia
    from bs4 import BeautifulSoup
    wikipedia.set_lang("fr")
    print("(Y a Internet)")
    
commands = {"joke": ["blague", "vanne", "joke", "fais moi rire", "fais rire"],
            "salut":["bonjour", "salut"],
            "heure": ["heure", "date", "quel jour", "le combien"],
            "Quit":["au revoir", "tais-toi", "dors", "eteins toi", "va dormir", "quitter le programme", "quitter", "stop"],
            "Merci":["merci", "je te remercie", "merci beaucoup"],
            "music": ["musique", "met de la musique", "met la musique", "music"],
            "presentation": ["Qui es-tu", "t'es qui", "fais ta presentation", "presente toi"],
            "search":["cherche", "recherche", "google"],
            "voldown":["met le son moins fort", "baisse le volume", "baisse le son"],
            "volup":["met le son plus fort", "plus de volume", "augmente", "augmente le son", "monte le son", "augmente le volume", "augmente le son"],
            #Internet seulement
            "news":["c'est quoi les news", "quelles sont les nouvelles", "quelles news", "dans journal", "nouvelles"],
            "where":["où suis je", "je suis où", "on est où", "localisation", "localise", "position"],
            "Ytb" : ["Sur Youtube", "Youtube", "video sur Youtube", "cherche sur Youtube"],
            "":["azertyuiopqsdfghjklmwxcvbn", ""],
            }


def get_news(topic="sciences"):
    NEWS = "https://www.lemonde.fr/"
    r=urlopen(NEWS+topic).read()
    soup=BeautifulSoup(r, features="html.parser")
    articles=soup.find_all("a")
    #print(len(articles), "articles")
    news_links = {}
    news_titles = []
    #print(NEWS+"/"+topic+"/article")
    iterator = 0
    for article in articles:
        a=article.get("href")
        if NEWS+topic+"/article" in a and iterator<5:
            b=a[:a.find("_")][::-1]
            b=b[:b.find("/")][::-1]
            news_titles.append(b)
            news_links[b]=a
            iterator+=1
    return (news_titles, news_links)


def recognize(TEXT):
    text = TEXT.split()
    best_command = ""
    best_var = 0
    for command in commands:
        synonyms = commands[command]
        var = process.extract(TEXT, synonyms)[0][1]
        if var>best_var:
            best_var = var
            best_command = command
    if best_var<90 and TEXT !="":
        TEXT = "?"
    print(best_var)
    return [best_command, TEXT]
            
def execute(command):
    global last_mode
    cmd = command[0]
    last_mode = cmd
    TEXT = command[1]
    text = ""
    if TEXT == "":
        text = ""
        return ""
    elif TEXT == "?":
        text = "..."
    elif cmd == "heure":
        now = datetime.datetime.now()
        text = "Il est actuellement "+str(now.hour) + ":" + str(now.minute)+", le "+str(now.day)+" "+["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"][now.month-1]+" "+str(now.year)
    elif cmd == "joke":
        text = choice(["Quelle est la difference entre Dieu et un chirurgien?\nDieu ne se prend pas pour un chirurgien",
                    "Comment s'appelle un boomerang qui ne revient pas? Un cintre"])
    elif cmd == "salut":
        text = "rebonjour à vous, grand maitre"
    elif cmd == "cmd":
        os.system("start cmd")
    elif cmd == "volup":
        for i in range(10):pg.press("volumeup")
        text = "oui Maître"
    elif cmd == "voldown":
        for i in range(10):pg.press("volumedown")
        text = "oui Maître"
    elif cmd == "Merci":
        text = "Je vous en prie Maitre"
    elif cmd == "Quit":
        text = "Au revoir"
        quit()
    elif cmd == "repeat":
        text = TEXT[3:]
    elif cmd == "music":
        l = os.listdir()
        shuffle(l)
        text = "tout de suite"
        for i in l:
            if (".mp3" in i):
                os.system(i)
                break
        else:
            text = "Vous n'avez pas de musique disponible"
    elif cmd == "presentation":
        text = "Je suis votre humble serviteur, Anubis"
    elif INTERNET:
        
        if cmd == "news":
            say("Quel genre de nouvelles voulez vous? sciences, politique, sport ou international?")
            text = listen()
            topic = process.extract(text, ["sciences", "politique", "sport", "international"])[0][0]
            news=get_news(topic)
            say("Pour les questions suivantes, répondez par oui ou par non s'il vous plait.")
            for title in news[0]:
                say("Voulez vous voir: "+title.replace("-", " ")+" ?")
                answer=listen()
                answer = process.extract(answer, ["oui", "non"])[0][0]
                if answer == "oui":
                    url = news[1][title]
                    say("Voulez vous que je vous le lise moi même?")
                    text = listen()
                    text = process.extract(text, ["oui", "non"])[0][0]
                    if text == "oui":
                        request = urlopen(url).read()
                        soup=BeautifulSoup(request, features="html.parser")
                        maybe = soup.find_all("p")
                        great_text = ""
                        for sentence in maybe:
                            try:
                                if "article__paragraph" in sentence["class"]:
                                    text=sentence.getText()
                                    if text != "class":
                                        great_text+=text
                            except Exception as err:
                                print(err)
                        say(great_text)
                    else:
                        webbrowser.open(url)
                    break

        if cmd == "Ytb":
            say("Que voulez vous chercher sur Youtube?")
            text=listen()
            say("A vos ordres")
            try:
                kit.playonyt(text)
            except Exception as ex:
                print(ex)
                
        if cmd == "where":
            loc = json.loads(urlopen("https://ipinfo.io/json").read().decode())
            text = "Vous etes actuellement aux environ de "+str(loc["city"])+" en "+str(loc["region"])
            
        elif cmd=="search":
            TEXT = TEXT.replace(TEXT.split()[0], "")
            text = wikipedia.summary(TEXT, sentences=2)
        else:
            text = "..."
    else:
        text = text="..."
    return text

