import os
import sys
import shutil
import time
import threading
import threading
import webbrowser

from pygame import mixer
from fifteen_api import FifteenAPI

#  Pre-defined values:
letterLimit = 199  # The limit that the AI can read. Do not change this to a number below 0 or a number above 199.
wordWrap = 100  # The amount of characters the program will print before it wraps the words

AI_R = FifteenAPI()  # Initialise reader AI
mixer.init()


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
    def __init__(self, threadID, name, text, textTime):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.text = text
        self.textTime = textTime

    def run(self):
        scrollText(self.text, self.textTime)

def readStory(storyName):
    clearScreen()
    print("Loading [Might take a while]...")
    f1 = open("stories/" + storyName + "/Narrator.txt", "r")
    narratorName = f1.readline().strip()
    f1.close()

    linesVoicing = []
    f1 = open("stories/" + storyName + "/audio/Information.txt", "r")
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
        t_thread.join()
        input()
        clearScreen()

    print("Story is done!")
    input()
    clearScreen()

def storyEditor(storyName):
    editDone = False
    clearScreen()
    while not editDone:
        print("Editing " + storyName + ":")
        print("1: Retake a line.")
        print("2: Recast a character.")
        print("3: Delete the story.")
        print("4: Back.")
        op = input("Selected option: ")
        clearScreen()
        if op == "1":
            doneRetake = False
            f1 = open("stories/" + storyName + "/Narrator.txt", "r")
            narratorName = f1.readline().strip()
            f1.close()

            charVocals = []
            f1 = open("stories/" + storyName + "/Characters.txt", "r")
            for line in f1.readlines():
                s_line = line.split(" | ")
                charVocal = [s_line[0].strip(), s_line[1].strip()]
                charVocals.append(charVocal)
            f1.close()

            linesVoicing = []
            f1 = open("stories/" + storyName + "/audio/Information.txt", "r")
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
            while not doneRetake:
                try:
                    r_op = int(input("Enter the number of the line you wish to retake: "))
                    clearScreen()
                    if r_op < 1 or r_op > len(linesVoicing):
                        print("Invalid selection.\n\n")
                    else:
                        clearScreen()
                        print("Is this the line you wish to retake?")
                        print(linesVoicing[r_op - 1][1])
                        print("Enter y for yes, anything else for no.")
                        c_op = input("Selection: ")
                        if c_op == "y" or c_op == "Y":
                            handlingRetake = True
                            while handlingRetake:
                                lineNumber = int(linesVoicing[r_op - 1][2][0].split("WAV")[1].split(".")[0])
                                clearScreen()
                                print("Processing request...")
                                totalVoice = [narratorName, linesVoicing[r_op - 1][1], []]
                                voiceLine = linesVoicing[r_op - 1][1]
                                letterCount = 0
                                targetLine = linesVoicing[r_op - 1][1]

                                charSpeaking = linesVoicing[r_op - 1][0]
                                for i in charVocals:
                                    if linesVoicing[r_op - 1][0] == i[0]:
                                        totalVoice[0] = i[1]
                                        charSpeaking = i[1]

                                parsedString = ""
                                for i in voiceLine:
                                    letterCount += 1
                                    if letterCount > letterLimit:
                                        hasSaved = False
                                        while not hasSaved:
                                            if AI_R.save_to_file(charSpeaking, parsedString,
                                                                 "stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")[
                                                "filename"] is None:
                                                pass
                                            else:
                                                hasSaved = True
                                        totalVoice[2].append("stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")
                                        lineNumber += 1
                                        letterCount = 0
                                        parsedString = ""
                                    else:
                                        parsedString += i
                                if len(parsedString) > 0:
                                    hasSaved = False
                                    while not hasSaved:
                                        if AI_R.save_to_file(charSpeaking, parsedString,
                                                             "stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")[
                                            "filename"] is None:
                                            pass
                                        else:
                                            hasSaved = True
                                    totalVoice[2].append("stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")
                                    lineNumber += 1
                                    letterCount = 0
                                    parsedString = ""
                                clearScreen()
                                print("Retake done. Playing...")
                                time.sleep(2)
                                textTime = 0
                                for j in totalVoice[2]:
                                    tts = mixer.Sound(j)
                                    textTime += tts.get_length()
                                sys.stdout.flush()
                                if totalVoice[0] == narratorName:
                                    sys.stdout.write(totalVoice[0] + " (Narrator): ")
                                else:
                                    sys.stdout.write(totalVoice[0] + ": ")
                                t_thread = ScrollTextClass(1, "Thread-Text", totalVoice[1], textTime)
                                t_thread.start()
                                for j in totalVoice[2]:
                                    tts = mixer.Sound(j)
                                    tts.play()
                                    time.sleep(tts.get_length())
                                    tts.stop()
                                print("\nEnter 1 to keep that retake or anything else to do another.")
                                t_thread.join()
                                time.sleep(1)
                                d_op = input("Selection: ")
                                clearScreen()
                                if d_op == "1":
                                    handlingRetake = False
                                    doneRetake = True
                        else:
                            pass
                except ValueError:
                    clearScreen()
                    print("Invalid selection.\n\n")
        elif op == "2":
            f1 = open("stories/" + storyName + "/Narrator.txt", "r")
            narratorName = f1.readline().strip()
            f1.close()

            charVocals = []
            f1 = open("stories/" + storyName + "/Characters.txt", "r")
            for line in f1.readlines():
                s_line = line.split(" | ")
                charVocal = [s_line[0].strip(), s_line[1].strip()]
                charVocals.append(charVocal)
            f1.close()

            linesVoicing = []
            f1 = open("stories/" + storyName + "/audio/Information.txt", "r")
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

            characterSwapDone = False
            while not characterSwapDone:
                print("Select the character you want to recast:")
                for i in charVocals:
                    print(i[0] + " - Voiced by " + i[1])
                option = input("Selection: ")
                clearScreen()
                targetID = -1
                for i in range(0, len(charVocals)):
                    if charVocals[i][0] == option:
                        targetID = i
                        break
                if targetID > -1:
                    oldChar = charVocals[targetID][0]
                    vocal = [charVocals[targetID][0], "Chell"]
                    newChar = input("Enter a character to voice " + vocal[0] + " (default is " + vocal[1] + "): ")
                    clearScreen()
                    print("Processing request...")
                    if AI_R.save_to_file(newChar, "A test", "Read.wav")["filename"] is None:
                        clearScreen()
                        print("Processing request...")
                        print("That character doesn't exist! Using " + vocal[1] + " instead...")
                    else:
                        print(vocal[0] + " is now voiced by " + newChar + ".")
                        vocal[1] = newChar

                    charVocals[targetID] = vocal
                    input()
                    clearScreen()

                    f = open("stories/" + storyName + "/Characters.txt", "w")
                    for char in charVocals:
                        f.write(char[0] + " | " + char[1] + "\n")
                    f.close()
                    if charVocals[targetID][0] == "Narrator":
                        f = open("stories/" + storyName + "/Narrator.txt", "w")
                        f.write(newChar)
                        f.close()
                        narratorName = newChar

                    lineIndexes = []
                    for i in linesVoicing:
                        if i[0] == oldChar:
                            lineIndexes.append(linesVoicing.index(i))

                    for id in lineIndexes:
                        clearScreen()
                        print("Retaking voice lines (Might take a while) [" + (str(round((lineIndexes.index(id) / (len(lineIndexes))) * 100))) + "%]")
                        print("Currently processing line:")
                        print(linesVoicing[id][1])
                        lineNumber = int(linesVoicing[id][2][0].split("WAV")[1].split(".")[0])
                        totalVoice = [narratorName, linesVoicing[id][1], []]
                        voiceLine = linesVoicing[id][1]
                        letterCount = 0
                        targetLine = linesVoicing[id][1]

                        charSpeaking = linesVoicing[id][0]
                        for i in charVocals:
                            if linesVoicing[id][0] == i[0]:
                                totalVoice[0] = i[1]
                                charSpeaking = i[1]

                        parsedString = ""
                        for i in voiceLine:
                            letterCount += 1
                            if letterCount > letterLimit:
                                hasSaved = False
                                while not hasSaved:
                                    if AI_R.save_to_file(charSpeaking, parsedString,
                                                         "stories/" + storyName + "/audio/WAV" + str(
                                                             lineNumber) + ".wav")[
                                        "filename"] is None:
                                        pass
                                    else:
                                        hasSaved = True
                                totalVoice[2].append("stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")
                                lineNumber += 1
                                letterCount = 0
                                parsedString = ""
                            else:
                                parsedString += i
                        if len(parsedString) > 0:
                            hasSaved = False
                            while not hasSaved:
                                if AI_R.save_to_file(charSpeaking, parsedString,
                                                     "stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")[
                                    "filename"] is None:
                                    pass
                                else:
                                    hasSaved = True
                            totalVoice[2].append("stories/" + storyName + "/audio/WAV" + str(lineNumber) + ".wav")
                            lineNumber += 1
                            letterCount = 0
                            parsedString = ""
                    clearScreen()
                    characterSwapDone = True
                else:
                    print("Invalid selection.\n\n")
        elif op == "3":
            d_op = input("Are you sure you want to delete this story? (Enter 'Sure' to delete): ")
            if d_op == "Sure":
                editDone = True
                for filename in os.listdir('stories/' + storyName + '/audio'):
                    file_path = os.path.join('stories/' + storyName + 'audio', filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                for filename in os.listdir('stories/' + storyName):
                    file_path = os.path.join('stories/' + storyName, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                try:
                    os.rmdir("stories/" + storyName + "/audio")
                except Exception as e:
                    pass
                try:
                    os.rmdir("stories/" + storyName)
                except Exception as e:
                    pass
                clearScreen()
        elif op == "4":
            editDone = True
        else:
            print("Invalid selection.\n\n")

def storyBrowser(type):
    hasSelected = False
    while not hasSelected:
        print("Enter the name of a story you want to read (Enter '|BACK|' to go back): ")
        stories = []
        for dirName in os.listdir("stories"):
            if os.path.isdir("stories/" + dirName):
                stories.append(dirName)
                print(dirName)

        option = input()
        clearScreen()
        if option in stories:
            if type == 1:
                readStory(option)
            else:
                storyEditor(option)
            hasSelected = True
        elif option == "|BACK|":
            hasSelected = True
        else:
            clearScreen()
            print("That story doesn't exist!\n\n")

def createStory():
    name = ""
    validName = False
    while not validName:
        name = input("Enter the story's name (Cannot contain any of the following: \ / : * ? \" < > |): ")
        clearScreen()
        invalidCharacters = "\/:*?\"<>|"
        validName = True
        for i in invalidCharacters:
            if i in name:
                validName = False
                print("Error: Invalid characters entered. Try again\n\n")
        if name == "":
            validName = False
            print("Error: Name cannot be empty.")

    print("Story name is " + name + " (Press enter to continue).")
    input()
    clearScreen()
    webbrowser.open("Story.txt")
    print("Enter the story's contents in the notepad file that opened just now.")
    print("Click here and press enter when you are done.")
    input()
    clearScreen()

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
        vocal = [char, "Chell"]
        newChar = input("Enter a character to voice " + vocal[0] + " (default is " + vocal[1] + "): ")
        clearScreen()
        print("Processing request...")
        if AI_R.save_to_file(newChar, "A test", "Read.wav")["filename"] is None:
            clearScreen()
            print("Processing request...")
            print("That character doesn't exist! Using " + vocal[1] + " instead...")
        else:
            print(vocal[0] + " is now voiced by " + newChar + ".")
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

    os.mkdir("stories/" + name)
    storyFolder = "stories/" + name

    os.mkdir(storyFolder + "/audio")
    f = open(storyFolder + "/Narrator.txt", "w")
    f.write(narratorName)
    f.close()

    f = open(storyFolder + "/Characters.txt", "w")
    f.write("Narrator | " + narratorName + "\n")
    for char in charVocals:
        f.write(char[0] + " | " + char[1] + "\n")
    f.close()

    lineNumber = 0
    linesVoicing = []

    for line in lines:
        clearScreen()
        print("Loading story (may take a while) [" + (
            str(round((lines.index(line) / (len(lines) - 1)) * 100))) + "%]...")
        print("Currently processing line:")
        print(line)
        totalVoice = [narratorName, line, []]
        voiceLine = line
        letterCount = 0
        targetLine = line
        if '|' in targetLine:
            targetLine = targetLine.split(" | ")
            totalVoice[0] = targetLine[0]
            totalVoice[1] = targetLine[1]
            voiceLine = targetLine[1]
            targetLine = targetLine[1]
            if "!!!" in targetLine:
                targetLine = targetLine.split(" !!! ")
                totalVoice[1] = targetLine[0]
                targetLine = targetLine[0] + " | " + targetLine[1]
                voiceLine = targetLine
        elif "!!!" in targetLine:
            targetLine = targetLine.split(" !!! ")
            totalVoice[1] = targetLine[0]
            targetLine = targetLine[0] + " | " + targetLine[1]
            voiceLine = targetLine

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
                    if AI_R.save_to_file(speakingCharacter, parsedString, storyFolder + "/audio/WAV" + str(lineNumber) + ".wav")[
                        "filename"] is None:
                        pass
                    else:
                        hasSaved = True
                totalVoice[2].append(storyFolder + "/audio/WAV" + str(lineNumber) + ".wav")
                lineNumber += 1
                letterCount = 0
                parsedString = ""
            else:
                parsedString += i
        if len(parsedString) > 0:
            hasSaved = False
            while not hasSaved:
                if AI_R.save_to_file(speakingCharacter, parsedString, storyFolder + "/audio/WAV" + str(lineNumber) + ".wav")[
                    "filename"] is None:
                    pass
                else:
                    hasSaved = True
            totalVoice[2].append(storyFolder + "/audio/WAV" + str(lineNumber) + ".wav")
            lineNumber += 1
            letterCount = 0
            parsedString = ""
        linesVoicing.append(totalVoice)

    clearScreen()
    f1 = open(storyFolder + "/audio/Information.txt", "a")
    for i in linesVoicing:
        f1.write(i[0].strip())
        f1.write(" | ")
        f1.write(i[1].strip())
        f1.write(" | ")
        for j in range(0, len(i[2])):
            f1.write(i[2][j].strip() + ",")
        f1.write("\n")
    f1.close()

    print("Story is ready to be read!")
    input()
    readStory(name)

isDone = False
clearScreen()
while not isDone:
    print("What would you like to do?")
    print("1: Read a story.")
    print("2: Create a new story.")
    print("3: Edit a story.")
    print("4: Exit.")
    try:
        op = int(input("Option selected: "))
        clearScreen()
        if op < 0 or op > 4:
            print("Error: Invalid value entered.\n\n")
        else:
            if op == 1:
                storyBrowser(1)
            elif op == 2:
                createStory()
            elif op == 3:
                storyBrowser(2)
            else:
                isDone = True
    except ValueError:
        clearScreen()
        print("Error: Invalid value entered.\n\n")
