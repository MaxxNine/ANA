from gtts import gTTS
import speech_recognition as sr
from pygame import mixer


def talkToMe(audio):
    print(audio)
    tts = gTTS(text=audio, lang='pt-br')
    tts.save('audio.mp3')
    mixer.init()
    mixer.music.load('./audio.mp3')
    mixer.music.play()


def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='pt')
        print("You said: " + command + "\n")

    except sr.UnknownValueError:
       return sr.UnknownValueError

    return command


talkToMe("Olá, estou pronta!")
