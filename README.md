# Story_Reader_Python
A program that uses 15.AI to read out stories. Read the README file for a better description on how to use.

Feel free to delete both Read.wav files before use. They're used to check the validity of a character.

Story Reader is a program made in Python 3.7 which uses a library that allows python to communicate with 15.ai (https://15.ai/ for program link. It was made by someone smarter than me). It takes in text from "Story.txt" and has characters on 15.ai read out different lines. Each character can be voiced by a different character (inputted in the program) and the narration can be spoken by a character as well.

To use: Seperate lines with new lines:

"This is one line"



"This is another line"

Use "CHARACTER | TEXT" to have a character speak, for example:

Heavy | It is a good day!

Note: You must ensure that each line has a letter in them and doesn't use { or }.

Finally, putting !!! after a character's sentance will allow you to define their emotion afterwards (Such as using | in 15.ai):

Heavy | It is a good day! !!! SPY!

After the program parses the text and creates the audio files, you'll be able to listen to your story one line at a time with each appropriate character reading out each line.

StoryReader.py is a secondary file which you can run to read the current story stored in the "audio" folder. Note that you'll have to have first run main.py to initialise the story before running StoryReader.py.
