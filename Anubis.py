from common import *
import commands

say("Bien le bonjour")
sleep(2)
while 1:
    data = stream.read(4096, exception_on_overflow = False)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()[14:-3]
        print("Vous: "+text)
        user(text)
        try:
            answer=commands.execute(commands.recognize(text))
            say(answer)
        except Exception as err:
            print(err)
        text=""
