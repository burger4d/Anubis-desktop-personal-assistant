import wx
from time import sleep
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import sounddevice as sd
import torch

language = 'fr'
model_id = 'v3_fr'
sample_rate = 48000
speaker = 'fr_0'
device = torch.device('cpu')

try:
    model0, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
    model0.to(device)
except:
    print("no internet")


model = Model("vosk-model-small-fr-0.22")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

app = wx.App() 
window = wx.Frame(None, title = "Anubis", size = (600,400)) 
panel = wx.Panel(window) 
label = wx.StaticText(panel, label = "Hello World", pos = (200,100))
window.SetBackgroundColour("black")
window.Show(True)

engine = pyttsx3.init()

def user(text):
    global label2
    if text!="":
        try:
            label2.Destroy()
        except:
            pass
        label2 = wx.StaticText(panel, label = text, pos = (400,50))
        label2.SetForegroundColour((255,0,0))
        window.Show(True)


def say(text):
    global label
    if text == "":
        text = "..."
    words = text.split()
    text2 = ""
    for word in range(len(words)):
        text2+=words[word]
        if word%10==0 and word != 0:
            text2+="\n"
        else:
            text2+=" "
    if text!="...":
        label.Destroy()
        label = wx.StaticText(panel, label = text2, pos = (0,200))
        label.SetForegroundColour((0,255,0))
        #label.SetBackgroundColour((0,0,255))
        window.Show(True)
        engine.say(text)
        engine.runAndWait()
    print("Anubis: "+text)
    sleep(0.1)

def say2(text):
    global label
    if text == "":
        text = "..."
    words = text.split()
    text2 = ""
    for word in range(len(words)):
        text2+=words[word]
        if word%10==0 and word != 0:
            text2+="\n"
        else:
            text2+=" "
    if text!="...":
        label.Destroy()
        label = wx.StaticText(panel, label = text2, pos = (0,200))
        label.SetForegroundColour((0,255,0))
        #label.SetBackgroundColour((0,0,255))
        window.Show(True)
        audio = model0.apply_tts(text=text,
                        speaker=speaker,
                        sample_rate=sample_rate)
        sd.play(audio, sample_rate)
        sleep(1+len(audio)/sample_rate)
        sd.stop()
        #engine.say(text)
        #engine.runAndWait()
    print("Anubis: "+text)
    sleep(0.1)

def listen():
    while 1:
        data = stream.read(4096, exception_on_overflow = False)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()[14:-3]
            print("Vous: "+text)
            user(text)
            return text


