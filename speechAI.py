import speech_recognition as sr
from random import choice
from sys import exit
import wave
import pyaudio
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 0.7)
engine.setProperty('rate', 150)

class SpeechAI:

    def __init__(self):
        self.positive = ["Yes", "Affirmative", "Sure", "Of course", "Definitely"]
        self.negative = ["No", "Negative", "Definitely not", "Not really"]
        self.greetings = ["Hello, how are you?", "Hey there", "Hi", "Nice to see you", "What's up?"]
        self.f_greetings = ["Goodbye!", "See you", "Hasta la vista", "See you next time", "Have a nice day!"]

    @staticmethod
    def play_audio(filename):
        CHUNK = 1024
        wave_file = wave.open(filename, "rb")
        pa = pyaudio.PyAudio()

        stream = pa.open(
            format=pa.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True
        )

        data_stream = wave_file.readframes(CHUNK)
        while data_stream:
            stream.write(data_stream)
            data_stream = wave_file.readframes(CHUNK)
        stream.close()
        pa.terminate()

    def respond(self, speech):
        engine.say(speech)
        engine.runAndWait()

    def discover(self, text):
        text = text.lower()
        if "bye" in text:
            self.respond(choice(self.f_greetings))
            exit()
        elif "your name" in text:
            self.respond("My name is Amethyst")
            return
        elif "you" in text and "robot" in text:
            self.respond(choice(["Maybe", "Yes", "I think so"]))
            return
        for greeting in ['hello', 'hey', 'hi ', 'hola', 'ciao']:
            if greeting in text:
                self.respond(choice(self.greetings))
                return

    def speechInit(self):
        while True:
            input("Press ENTER to start speaking")
            print("Listening...")
            with sr.Microphone() as source:
                print("Say something")
                audio = r.listen(source)

            speech = None
            try:
                speech = r.recognize_google(audio)
            except:
                self.respond("Couldn't understand what you said. Please repeat")

            if speech:
                self.respond(speech)
                print(f"You said: {speech}")
                self.discover(speech)


if __name__ == '__main__':
    bot = SpeechAI()
    bot.speechInit()
