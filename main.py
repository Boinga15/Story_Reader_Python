import os
import shutil
import time

from pygame import mixer

from fifteen_api import FifteenAPI

letterLimit = 199  # The limit that the AI can read.

AI_R = FifteenAPI()  # Initialise reader AI
mixer.init()

def clearScreen():
    for i in range(0, 20):
        print("\n\n\n\n\n\n")

for filename in os.listdir('audio'):
    file_path = os.path.join('audio', filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

clearScreen()
narratorName = "HAL 9000"  # Default narrator
newNarrator = input("Enter a narrator (default is " + narratorName + "): ")
clearScreen()
print("Processing request...")
if AI_R.save_to_file(newNarrator, "A test", "Read.wav")["filename"] is None:
    clearScreen()
    print("Processing request...")
    print("That character doesn't exist! Using " + narratorName + " instead...")
else:
    print("Narrator switched to " + newNarrator + ".")
    narratorName = newNarrator

input()
clearScreen()

print("Loading story...")
lines = []
f1 = open("Story.txt", "r")
allLines = f1.readlines()
for line in allLines:
    newLine = line.strip()
    if newLine == "":
        pass
    else:
        lines.append(newLine)

print(lines)

characters = []  # Adding characters
for line in lines:
    if '|' in line:  # Is a character talking
        newLine = line.split(" | ")
        newLine = newLine[0]
        if newLine in characters:
            pass
        else:
            characters.append(newLine)

clearScreen()
charVocals = []
for char in characters:
    vocal = [char, "Sans"]
    newChar = input("Enter a character to voice " + vocal[0] + " (default is " + vocal[1] + "): ")
    clearScreen()
    print("Processing request...")
    if AI_R.save_to_file(newChar, "A test", "Read.wav")["filename"] is None:
        clearScreen()
        print("Processing request...")
        print("That character doesn't exist! Using " + vocal[1] + " instead...")
    else:
        print("Character is now voiced by " + newChar + ".")
        vocal[1] = newChar

    charVocals.append(vocal)
    input()
    clearScreen()

print("Story cast: ")
print("Narrated by " + narratorName + ".")
for vocal in charVocals:
    print(vocal[0] + " voiced by " + vocal[1] + ".")

input()
clearScreen()

lineNumber = 0
linesVoicing = []

for line in lines:
    clearScreen()
    print("Loading story (may take a while) [" + (str(round((lines.index(line) / (len(lines) - 1)) * 100))) + "%]...")
    totalVoice = [narratorName, line, []]
    voiceLine = line
    letterCount = 0
    targetLine = line
    if '|' in targetLine:
        targetLine = targetLine.split(" | ")
        totalVoice[0] = targetLine[0]
        totalVoice[1] = targetLine[1]
        voiceLine = targetLine[1]

    parsedString = ""
    wavNumber = 0
    speakingCharacter = narratorName
    if totalVoice[0] == narratorName:
        pass
    else:
        for i in charVocals:
            if i[0] == totalVoice[0]:
                speakingCharacter = i[1]
                break
    for i in voiceLine:
        letterCount += 1
        if letterCount > letterLimit:
            hasSaved = False
            while not hasSaved:
                if AI_R.save_to_file(speakingCharacter, parsedString, "audio/WAV" + str(lineNumber) + ".wav")["filename"] is None:
                    pass
                else:
                    hasSaved = True
            totalVoice[2].append("audio/WAV" + str(lineNumber) + ".wav")
            lineNumber += 1
            letterCount = 0
            parsedString = ""
        else:
            parsedString += i
    if len(parsedString) > 0:
        hasSaved = False
        while not hasSaved:
            if AI_R.save_to_file(speakingCharacter, parsedString, "audio/WAV" + str(lineNumber) + ".wav")["filename"] is None:
                pass
            else:
                hasSaved = True
        totalVoice[2].append("audio/WAV" + str(lineNumber) + ".wav")
        lineNumber += 1
        letterCount = 0
        parsedString = ""
    linesVoicing.append(totalVoice)

clearScreen()
input()

clearScreen()
for i in linesVoicing:
    if i[0] == narratorName:
        print(i[1])
    else:
        print(i[0] + ": " + i[1])
    for j in i[2]:
        tts = mixer.Sound(j)
        tts.play()
        time.sleep(tts.get_length())
        tts.stop()
    input()
    clearScreen()

print("Story is done!")
input()
clearScreen()
