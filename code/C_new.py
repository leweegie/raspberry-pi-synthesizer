import webiopi
import numpy as np
import pygame
import time
import math
import pylab as pl


# Set up GPIO library
GPIO = webiopi.GPIO


# Syntax to import the MCP23S17 I/O expander chip .
# documentation on webiopi.trouch.com is not up to date .
from webiopi.devices.digital.mcp23XXX import MCP23S17


# Define the CS pin and hardware address (A0, A1, A2 all grounded)
mcp0= MCP23S17 ( chip =1, slave=0x20 )

# Some constants
outputRate = 44100
maxAmplitude = np.iinfo( np.int16 ).max

# Set up the audio output - only once!
# 2-channel (stereo), 16-bit signed integer value output at 44khz
pygame.mixer.init( frequency=outputRate, channels=2, size=-16)

notes = []

#define our piano notes to be played by keyboard
notes.append(pygame.mixer.Sound("piano_samples/C6.wav"))
notes.append(pygame.mixer.Sound("piano_samples/B5.wav"))
notes.append(pygame.mixer.Sound("piano_samples/A5.wav"))
notes.append(pygame.mixer.Sound("piano_samples/G5.wav"))
notes.append(pygame.mixer.Sound("piano_samples/F5.wav"))
notes.append(pygame.mixer.Sound("piano_samples/E5.wav"))
notes.append(pygame.mixer.Sound("piano_samples/D5.wav"))
notes.append(pygame.mixer.Sound("piano_samples/C5.wav"))


#create lists of KEYS
KEY = []
#create lists of LED pins
LED = []

for i in range(0,8):
    KEY.append(i)
    LED.append(i + 8)

#define low and high GPIO readings
low = GPIO.LOW
high = GPIO.HIGH

for i in range (0, len(LED)):
    # Set LED pins to output
    mcp0.setFunction(LED[i], GPIO.OUT)
    #Write LED channels to low
    mcp0.digitalWrite(LED[i],low)
    # Set KEY pins to input
    mcp0.setFunction(KEY[i], GPIO.IN)

#functiom to allow a song to be played in learn mode
def LearnMelody(song, leds, keys, high, low):
    for i in range (0, len(song)):
                mcp0.digitalWrite(leds[i], high)
                while True:
                    if (mcp0.digitalRead(keys[i]) == GPIO.HIGH):
                        song[i].play()
                        mcp0.digitalWrite(leds[i],low)
                        time.sleep(times[i])
                        break

#function to hear a song played in learn mode        
def HearMelody(song, leds, high, low):
    for i in range (0, len(song)):
                mcp0.digitalWrite(leds[i], high)
                song[i].play()
                time.sleep(times[i])
                mcp0.digitalWrite(leds[i], low)

#function to create the song using a string of numbers, song_order, corresponding to the notes
def CreateMelody(song_order, leds, song, keys):
    for i in range (0, len(song_order)):
            li = int(song_order[i])
            ki = 7 - li
            leds.append(LED[li])
            song.append(notes[li])
            keys.append(KEY[ki])

#Initialise choice for user free play or learn a song
print("Please enter '1' or '2' depending on whether you would like to: \n")
print("1: Free play \n")
print("2: Learn a melody \n")
choice = input()
if (choice == "1"): #free play
    
    base = mcp0.portRead()
    
    #loop forever
    while True:
        for i in range (0,len(LED)):
            #Write LED channels to low
            mcp0.digitalWrite(LED[i],low)
            read = mcp0.portRead()
            if (read > base):
                n = []
                diff = read - base
                diff_binary = "{0:08b}".format(diff)
                for i in range (0,8):
                    if diff_binary[i] == "1":
                        notes[i].play()
                        mcp0.digitalWrite(LED[i], high)
                        time.sleep(0.17)

            
if (choice == "2"): #learn a song
    
    leds = []
    keys = [] 
    song = []
    times = []
    #ask user for song choice
    print("Enter number to choose song: \n")
    print("1: Twinkle Twinkle Little Star")
    print("2: Old Macdonald \n")
    choice = input()

    if (choice == "1"): #twinkle twinkle
        
        song_order = "77332234455667"  #string of note numbers as they appear in pentatonic scale
        
        CreateMelody(song_order, leds, song, keys)

        #times of notes used in twinkle twinkle
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(1)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(1)
 
        print("Enter number to choose whether you would like to hear melody or learn melody: \n")
        print("1: Hear melody")
        print("2: Learn melody \n")
        choice = input()
        
        if (choice == "1"): #hear melody
            #play song
            HearMelody(song,leds,high,low)
            #switch to learn song
            print("Time to learn!")
            print("Play the note that corresponds to the LED as it lights up!")
            LearnMelody(song, leds, keys, high, low)
        
        if(choice == "2"):  #learn melody
            print("Play the note that corresponds to the LED as it lights up!")
            LearnMelody(song, leds, keys, high, low)
            
    if (choice =="2"): # old mcdonald
        
        song_order = "333655611223"  #string of note numbers as they appear in pentatonic scale
        
        CreateMelody(song_order, leds, song, keys)

        #times of notes used in old mcdonald
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(1)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(0.5)
        times.append(2)

        print("Enter number to choose whether you would like to hear melody or learn melody: \n")
        print("1: Hear melody")
        print("2: Learn melody \n")
        choice = input()

        if (choice == "1"): #hear melody
            
            HearMelody(song,leds,high,low)
            print("Time to learn!")
            print("Play the note that corresponds to the LED as it lights up!")
            LearnMelody(song, leds, keys, high, low)

        if(choice == "2"): #learn melody
            
            print("Play the note that corresponds to the LED as it lights up!")
            LearnMelody(song, leds, keys, high, low)
else:
    print("Please enter only '1' or '2'. Program self destructing.")