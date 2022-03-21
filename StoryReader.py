import os
import sys
import shutil
import time
import threading

from pygame import mixer

mixer.init()
wordWrap = 100  # The amount of characters the program will print before it wraps the words

def clearScreen():
    for i in range(0, 20):
        print("\n\n\n\n\n\n")

def scrollText(text, totalTime):
    charDelay = totalTime / len(text)
    wordCount = 0
    for i in text:
        sys.stdout.flush()
        sys.stdout.write(i)
        wordCount += 1
        if wordCount >= wordWrap and i == ' ':
            print("")
            wordCount = 0
        time.sleep(charDelay)

class ScrollTextClass(threading.Thread):
    def __init__ (self, threadID, name, text, textTime):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.text = text
        self.textTime = textTime

    def run(self):
        scrollText(self.text, self.textTime)

print("Loading story...")

f1 = open("audio/NARRATOR.txt", "r")
narratorName = f1.readline().strip()
f1.close()

linesVoicing = []
f1 = open("audio/Information.txt", "r")
for line in f1.readlines():
    workingLine = line.split(" | ")
    voicedLine = ["", "", []]
    voicedLine[0] = workingLine[0]
    voicedLine[1] = workingLine[1]
    wavFiles = workingLine[2].split(",")
    for j in wavFiles:
        if j.strip() != '':
            voicedLine[2].append(j.strip())

    linesVoicing.append(voicedLine)

clearScreen()
print("Story is ready! Press enter to start!")
input()

clearScreen()
for i in linesVoicing:
    textTime = 0
    for j in i[2]:
        tts = mixer.Sound(j)
        textTime += tts.get_length()
    sys.stdout.flush()
    if i[0] == narratorName:
        sys.stdout.write(i[0] + " (Narrator): ")
    else:
        sys.stdout.write(i[0] + ": ")
    t_thread = ScrollTextClass(1, "Thread-Text", i[1], textTime)
    t_thread.start()
    for j in i[2]:
        tts = mixer.Sound(j)
        tts.play()
        time.sleep(tts.get_length())
        tts.stop()
    input()
    t_thread.join()
    clearScreen()

print("Story is done!")
input()
clearScreen()