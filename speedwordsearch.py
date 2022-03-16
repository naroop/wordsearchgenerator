from ast import Index
import random
from time import sleep
from os import system, name
import string
from copy import deepcopy

# Returns True if there is a valid word placement horizontally at that start position.
def searchH(pos, word, wordsearch):
    for i in range(len(word)):
        if i + pos[0] >= 12:
            return False
        if wordsearch[pos[1]][pos[0] + i] != '-':
            if word[i] != wordsearch[pos[1]][pos[0] + i]:
                return False
    return True

# Returns True if there is a valid word placement vertically (going down) at that start position
def searchV(pos, word, wordsearch):
    for i in range(len(word)):
        if i + pos[1] >= 12:
            return False
        if wordsearch[i+pos[1]][pos[0]] != '-':
            if word[i] != wordsearch[i+pos[1]][pos[0]]:
                return False
    return True

# Returns True if there is a valid word placement diagonally downwards at that start position
def searchDD(pos, word, wordsearch):
    for i in range(len(word)):
        if i + pos[1] >= 12 or i + pos[0] >= 12:
            return False
        if wordsearch[i+pos[1]][i+pos[0]] != '-':
            if word[i] != wordsearch[i+pos[1]][i+pos[0]]:
                return False
    return True

# Returns True if there is a valid word placement diagonally upwards at that start position
def searchUD(pos, word, wordsearch):
    for i in range(len(word)):
        if i + pos[0] >= 12 or pos[1] - i <= 0:
            return False
        if wordsearch[pos[1]-i][pos[0]+i] != '-':
            if word[i] != wordsearch[pos[1]-i][pos[0]+i]:
                return False
    return True

# Prints the word search
def displayWordsearch(wordsearch):
  print(" _________________________")
  print("|                         |")
  for row in range(0,12):
    line="| "
    for col in range(0,12):
      line = line + wordsearch[row][col] + " "
    line = line + "|"
    print(line)
  print("|_________________________|")  

# Creates/modifies a word search that is filled with "-" at each location
def createEmpty(wordsearch):
    for row in range(0,12):
        wordsearch.append([])
        for col in range(0,12):
            wordsearch[row].append("-")
    return wordsearch

# Gets user input to create and return a list of the words that are to be included in the word search
def getWords():
    print("Enter the words you would like to include in the word search. Type 'D' when done.")
    words = []
    inp = ''
    count = 1
    while(inp != "D"):
        print("Word %d:" %(count))
        inp = input("- ")
        words.append(inp)
        count += 1
    words.pop(len(words)-1)
    return words

# Pass in a word search, a tuple representing the starting location, a direction to place the word, and the word itself. 
# Directions:   "H" for horizontal
#               "V" for vertical
#               "UD" for upwards diagonal
#               "DD" for downwards diagonal
# Validity of the placement is determined before this function is ran so there should be no errors.
def placeWord(wordsearch, pos, direction, word):
    if direction == "V":
        for i in range(len(word)):
            wordsearch[i+pos[1]][pos[0]] = word[i]
    elif direction == "H":
        for i in range(len(word)):
            wordsearch[pos[1]][i+pos[0]] = word[i]
    elif direction == "DD":
        for i in range(len(word)):
            wordsearch[i+pos[1]][i+pos[0]] = word[i]
    elif direction == "UD":
        for i in range(len(word)):
            wordsearch[pos[1]-i][pos[0]+i] = word[i]
    return wordsearch

# This will determine all valid starting coordinates for a given word
# Returns a dickionary containing all valid start coords and a list containing their possible directions.
def findValidStarts(wordsearch, word):
    dick = {}
    for row in range(0, 12):
        for col in range(0, 12):
            startPos = (col, row)
            directions = []
            if searchH(startPos, word, wordsearch) == True:
                directions.append("H")
                dick[startPos] = directions
            if searchV(startPos, word, wordsearch) == True:
                directions.append("V")
                dick[startPos] = directions
            if searchDD(startPos, word, wordsearch) == True:
                directions.append("DD")
                dick[startPos] = directions
            if searchUD(startPos, word, wordsearch) == True:
                directions.append("UD")
                dick[startPos] = directions
    if len(dick) == 0:
        print("There were no valid locations.")
    return dick

# Returns a tuple containing the start position and the direction chosen.
def getRandomPositionAndDirection(validStarts):
    startLoc = random.choice(list(validStarts))
    direction = random.choice(validStarts[startLoc])
    return (startLoc, direction)

# This will prioritize making diagonals since it seems to not like doing them.
def riggedRandom(validStarts):
    number = random.randrange(0,10)
    if number < 3: # 40% chance of forcing a diagonal
        diagonals = {}
        for key in validStarts: # This for block will create a new dictionary only containing the possible locations with only its corresponding diagonal options
            if "D" in validStarts[key][len(validStarts[key])-1]:
                dirList = []
                for dir in validStarts[key]:
                    if "D" in dir:
                        dirList.append(dir)

                diagonals[key] = dirList
        return getRandomPositionAndDirection(diagonals)
    else:
        return getRandomPositionAndDirection(validStarts)
    

def reverseString(string):
    return string[::-1]

def reverseSomeWords(words):
    choice = input("Would you like some of the words to be backwards? Enter [y/n]: ")
    if choice == "y":
        for i in range(len(words)):
            number = random.randrange(0, 2)
            if number == 1:
                words[i] = reverseString(words[i])
    return words

def populateSpaces(wordsearch):
    for row in range(0, 12):
        for col in range(0, 12):
            if wordsearch[row][col] == "-":
                wordsearch[row][col] = random.choice(string.ascii_letters[0:26])

def printWordList(words, errorWords):
    for i in range(len(words)):
        if words[i] not in errorWords:
            print("%d - %s" %(i, words[i]))

def generateWordSearch():
    wordsearch = []
    wordsearch = createEmpty(wordsearch) # First we generate an empty word search
    words = getWords() # Next, we get the list of words the user wants to include in their word search
    words = reverseSomeWords(words)
    errorWords = []
    for i in range(len(words)): # Then, we loop through each word and place it in the word search
        dick = findValidStarts(wordsearch, words[i]) # We find all valid starting points of a given word
        try: # Find valid starts could generate an empty list. In this case, we stop at the given word, print we were unable to do it and have the user rerun.
            posAndDir = riggedRandom(dick) # We get a random postion and an associated random direction
            placeWord(wordsearch, posAndDir[0], posAndDir[1], words[i]) # We place the word in the word search
        except IndexError:
            print("Couldn't place word %s. Try re-running!" %(words[i]))
            errorWords.append(words[i])
    answers = deepcopy(wordsearch)
    populateSpaces(wordsearch)
    displayWordsearch(wordsearch)
    displayWordsearch(answers)
    printWordList(words, errorWords)

generateWordSearch()









