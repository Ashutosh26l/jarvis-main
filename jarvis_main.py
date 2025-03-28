import struct
import pyaudio
import pvporcupine
from pydub.playback import play
from pydub import AudioSegment
import speech_recognition as sr
import pyttsx3
import jarvis_command
engine=pyttsx3.init("sapi5")
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
rate=engine.getProperty('rate')
engine.setProperty("rate",rate-30)
def speak(text):
    print("Jarvis:",text)
    engine.say(text)
    engine.runAndWait()

porcupine=None
pyaud=None
audio_stream=None
def startsound():
    audio=AudioSegment.from_wav("start up sound.wav")
    play(audio)


def endsound():
    audio=AudioSegment.from_wav("end up sound.wav")
    play(audio)
try:
    porcupine=pvporcupine.create(keywords=["jarvis","alexa","ok google"])
    paud=pyaudio.PyAudio()
    audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
    while True:
        keyword=audio_stream.read(porcupine.frame_length)
        keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
        keyword_index=porcupine.process(keyword)
        if keyword_index>=0:
            startsound()
            recognize=sr.Recognizer()
            with sr.Microphone() as source:
                audio=recognize.listen(source,3,3)
                endsound()
            try:
                query=recognize.recognize_google(audio,language='en-in')
                jarvis_command.command(query)
                file=open("myfile.txt","w")
                file.write(query)
                file.close()
                print(query)
            except sr.UnknownValueError:
                speak("not recognize")
            

finally:
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if paud is not None:
        paud.terminate()