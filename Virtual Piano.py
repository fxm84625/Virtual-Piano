'''
DSP Project - Virtual Piano

By: Frank Cen, Dong Yu

'''

import pyaudio
import pygame
import struct
import numpy as np
from math import sin, cos, pi
from matplotlib import pyplot as plt

# Variable and Setup

WIDTH = 2
CHANNELS = 1
RATE = 4000
MAX = 2**15 - 1

win_wid = 800
win_len = 600

black = (0, 0, 0)
white = (255, 255, 255)
lgray = (211, 211, 211)
skin = (255, 0, 0)

pygame.init()
pge = pygame.event.get()
pygame.display.init()
game_disp = pygame.display.set_mode((win_wid, win_len))
game_disp.fill(lgray)
pygame.display.set_caption('Virtual Piano')

#pygame.key.set_repeat(1,1)

# Functions

def clip16( x ):
    '''
        Takes in a number and clips it at MAX for signed 16-bit
    '''
    if x > MAX:
        x = MAX
    if x < -1 * MAX - 1:
        x = -1 * MAX - 1
    return x

def get_freq(note):
    '''
        Takes in note index and return the frequency for the note
    '''
    if note == 0:       return 261.63   # C
    elif note == 1:     return 277.18   # C Sharp
    elif note == 2:     return 293.66   # D
    elif note == 3:     return 311.13   # D Sharp
    elif note == 4:     return 329.63   # E
    elif note == 5:     return 349.23   # F
    elif note == 6:     return 369.99   # F Sharp
    elif note == 7:     return 392      # G
    elif note == 8:     return 415.3    # G Sharp
    elif note == 9:     return 440      # A
    elif note == 10:    return 466.16   # A Sharp
    elif note == 11:    return 493.88   # B

def txt_obj(txt, font, color):
    '''
        Parameters: txt - String text
                    font - font information
                    color - color of the text

        returns text surface and text position to display for pygame
    '''
    
    txt_surf = font.render(txt, True, color)
    return txt_surf, txt_surf.get_rect()

def disp_txt(txt, width, height, ft = 28, color = black):
    '''
        Parameters: txt - String text to display
                    width - width position
                    height - height position
                    ft - font size default 28
                    color - color of the text, default black

        display the text in pygame window
    '''
    
    dtxt = pygame.font.Font('freesansbold.ttf', ft)
    txt_surf, txt_rect = txt_obj(txt, dtxt, color)
    txt_rect.center = (width, height)
    game_disp.blit(txt_surf, txt_rect)

    pygame.display.update()

def disp_key_pic(position):

    '''
        Only parameter is the width position for the keyboard picture.
        This code display the picture of piano keyboard in pygame
    '''
    
    pw = position
    disp_txt("Press 'ESC' to Quit", (win_wid*0.175), (win_len*0.05))
    
    # C
    pygame.draw.rect(game_disp, white, [pw, 100, 75, 400])
    pygame.draw.rect(game_disp, black, [pw, 100, 75, 400], 1)
    disp_txt("C", (pw + (75/2.5)), 300, 20)
    disp_txt("A", (pw + (75/2)), 525, 18)
    # D
    pygame.draw.rect(game_disp, white, [(pw + 75), 100, 75, 400])
    pygame.draw.rect(game_disp, black, [(pw + 75), 100, 75, 400], 1)
    disp_txt("D", ((pw + 75) + (75/2.5)), 300, 20)
    disp_txt("S", ((pw + 75) + (75/2)), 525, 18)
    # E
    pygame.draw.rect(game_disp, white, [(pw + (2 * 75)), 100, 75, 400])
    pygame.draw.rect(game_disp, black, [(pw + (2 * 75)), 100, 75, 400], 1)
    disp_txt("E", ((pw + (2 * 75)) + (75/2.5)), 300, 20)
    disp_txt("D", ((pw + (2 * 75)) + (75/2)), 525, 18)
    # F
    pygame.draw.rect(game_disp, white, [(pw + (3 * 75)), 100, 75, 400])
    pygame.draw.rect(game_disp, black, [(pw + (3 * 75)), 100, 75, 400], 1)
    disp_txt("F", ((pw + (3 * 75)) + (75/2.5)), 300, 20)
    disp_txt("F", ((pw + (3 * 75)) + (75/2)), 525, 18)
    # G
    pygame.draw.rect(game_disp, white, [(pw + (4 * 75)), 100, 75, 400])
    pygame.draw.rect(game_disp, black, [(pw + (4 * 75)), 100, 75, 400], 1)
    disp_txt("G", ((pw + (4 * 75)) + (75/2.5)), 300, 20)
    disp_txt("G", ((pw + (4 * 75)) + (75/2)), 525, 18)
    # A
    pygame.draw.rect(game_disp, white, [(pw + (5 * 75)), 100, 75, 400])
    pygame.draw.rect(game_disp, black, [(pw + (5 * 75)), 100, 75, 400], 1)
    disp_txt("A", ((pw + (5 * 75)) + (75/2.5)), 300, 20)
    disp_txt("H", ((pw + (5 * 75)) + (75/2) + 5), 525, 18)
    # B
    pygame.draw.rect(game_disp, white, [(pw + (6 * 75)), 100, 75, 400])
    pygame.draw.rect(game_disp, black, [(pw + (6 * 75)), 100, 75, 400], 1)
    disp_txt("B", ((pw + (6 * 75)) + (75/2.5)), 300, 20)
    disp_txt("J", ((pw + (6 * 75)) + (75/2) + 5), 525, 18)

    # C#
    pygame.draw.rect(game_disp, black, [(pw + 56), 100, (75/2), (400/1.5)])
    disp_txt("C#", (pw + (75)), 250, 20, white)
    disp_txt("W", (pw + 75), 85, 18)
    # D#
    pygame.draw.rect(game_disp, black, [(pw + 56 + 75), 100, (75/2), (400/1.5)])
    disp_txt("D#", (pw + (2 * 75)), 250, 20, white)
    disp_txt("E", (pw + (2 * 75)), 85, 18)
    # F#
    pygame.draw.rect(game_disp, black, [(pw + 56 + (3 * 75)), 100, (75/2), (400/1.5)])
    disp_txt("F#", (pw + (4 * 75)), 250, 20, white)
    disp_txt("T", (pw + (4 * 75)), 85, 18)
    # G#
    pygame.draw.rect(game_disp, black, [(pw + 56 + (4 * 75)), 100, (75/2), (400/1.5)])
    disp_txt("G#", (pw + (5 * 75)), 250, 20, white)
    disp_txt("Y", (pw + (5 * 75)), 85, 18)
    # A#
    pygame.draw.rect(game_disp, black, [(pw + 56 + (5 * 75)), 100, (75/2), (400/1.5)])
    disp_txt("A#", (pw + (6 * 75)), 250, 20, white)
    disp_txt("U", (pw + (6 * 75)), 85, 18)

def disp_press(key, pw):

    '''
        Parameter pw is the reference width position for the key pressed
        indicator circle. key is a list of key condition
        (Pressed (1) or not Pressed (0))

        This code detects key being pressed and indicate it in pygame
    '''
    
    # Press key detect

    # C
    if key[0] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + (75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw + (75/2)), 475], 10)
    # C#
    if key[1] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 75), 325], 10)
    else:
        pygame.draw.circle(game_disp, black, [(pw + 75), 325], 10)
    # D
    if key[2] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 3*(75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw + 3*(75/2)), 475], 10)
    # D#
    if key[3] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 2*75), 325], 10)
    else:
        pygame.draw.circle(game_disp, black, [(pw + 2*75), 325], 10)
    # E
    if key[4] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 5*(75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw + 5*(75/2)), 475], 10)
    # F
    if key[5] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 7*(75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw + 7*(75/2)), 475], 10)
    # F#
    if key[6] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 4*75), 325], 10)
    else:
        pygame.draw.circle(game_disp, black, [(pw + 4*75), 325], 10)
    # G
    if key[7] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 9*(75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw + 9*(75/2)), 475], 10)
    # G#
    if key[8] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 5*75), 325], 10)
    else:
        pygame.draw.circle(game_disp, black, [(pw + 5*75), 325], 10)
    # A
    if key[9] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 11*(75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw +11*(75/2)), 475], 10)
    # A#
    if key[10] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 6*75), 325], 10)
    else:
        pygame.draw.circle(game_disp, black, [(pw + 6*75), 325], 10)
    # B
    if key[11] == 1:
        pygame.draw.circle(game_disp, skin, [(pw + 13*(75/2)), 475], 10)
    else:
        pygame.draw.circle(game_disp, white, [(pw + 13*(75/2)), 475], 10)
    

def keydown( pressed, x ):
    pressed[x] = 1

def keyup( x ):
    pressed[x] = 0


def main():

    gain = MAX / 4
    
##    # Plot code (only plot max of 10000 samples)
##    plt.ion()
##    fig1 = plt.figure(1)
##    samp_len = 10000
##    plt.ylim(-16000, 16000)
##    plt.xlim(0, 5100)
##    line1, = plt.plot([], [], color = 'blue')
##    samp = [n+1 for n in range(samp_len)]
##    line1.set_xdata(samp)
##    pdata = []

    stop = False
    decay = 0.0005       # Decay Rate
    decay2 = 0.0002     # Slow Decay Rate (When button is held down)

    ## Data Variables
    x = 0.0             # Right Hand
##    y = 0.0             # Left Hand
##    out = [0.0, 0.0]    # Stereo Output
    angles = [ -1 for i in range(12) ]     # Angle for the sine wave for each key
                                                # Angle is set to be negative if the Note is not played
    notes = [ 0.0 for i in range(12) ]      # Amplitude of the sound wave (0.0 to 1.0)
    pressed = [ 0 for i in range(12) ]      # pressed[x] = 1 if note x is pressed
    prev = [ 0 for i in range(12) ]       # previous frame pressed keys

    BLOCKSIZE = 1024/16
    blocks = np.zeros(BLOCKSIZE)
    bcount = 0 # Block index counter

    pcount = 0 # Synthesizer counter
    
    disp_key_pic(120)

    p = pyaudio.PyAudio()
    stream = p.open( format     = p.get_format_from_width(WIDTH),
                     channels   = CHANNELS,
                     rate       = RATE,
                     input      = False,
                     output     = True )

    while stop == False:
        for x in range(12):
            if( pressed[x] == 0 ):          # Update previous frame pressed keys
                prev[x] = 0
            elif( pressed[x] == 1 ):
                prev[x] = 1
            pressed[x] = 0                  # Reset pressed keys for current frame

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: stop = True
        if keys[pygame.K_a]: keydown( pressed, 0 )   # C
        if keys[pygame.K_w]: keydown( pressed, 1 )   # C Sharp
        if keys[pygame.K_s]: keydown( pressed, 2 )   # D
        if keys[pygame.K_e]: keydown( pressed, 3 )   # D Sharp
        if keys[pygame.K_d]: keydown( pressed, 4 )   # E
        if keys[pygame.K_f]: keydown( pressed, 5 )   # F
        if keys[pygame.K_t]: keydown( pressed, 6 )   # F Sharp            
        if keys[pygame.K_g]: keydown( pressed, 7 )   # G
        if keys[pygame.K_y]: keydown( pressed, 8 )   # G Sharp
        if keys[pygame.K_h]: keydown( pressed, 9 )   # A
        if keys[pygame.K_u]: keydown( pressed, 10 )  # A Sharp
        if keys[pygame.K_j]: keydown( pressed, 11 )  # B

        for x in range(12):
            if( pressed[x] == 0 ):
                notes[x] = notes[x] - decay     # Decay the Note while not pressed
            elif( pressed[x] == 1 and prev[x] == 0 ):
                notes[x] = 1.0                  # Start playing the Note
                angles[x] = 0                   # Start wave angle
            elif( pressed[x] == 1 and prev[x] == 1 and pcount < 1500):
                notes[x] = notes[x] - decay2    # Slower decay while Pressed

##                pcount += 1 # Synthesizer counter
##                
##            # Synthesizer code
##            elif( pressed[x] == 0 and prev[x] == 0 ):
##                pcount = 0
            
            if notes[x] < 0: notes[x] = 0.0         # Clip notes. Minimum = 0
            if( angles[x] >= 0 ):               # If the wave angle is active:
                angles[x] = angles[x] + 1           # Linearly increase the angle
            if( notes[x] <= 0 ):                # If the note is not being played:
                angles[x] = -1                      # The wave angle isn't active (negative)

        # edit x and y based on notes[]
        x = ( notes[0] * sin( get_freq(0) * 2 * pi * angles[0] / RATE)
            + notes[1] * sin( get_freq(1) * 2 * pi * angles[1] / RATE)
            + notes[2] * sin( get_freq(2) * 2 * pi * angles[2] / RATE)
            + notes[3] * sin( get_freq(3) * 2 * pi * angles[3] / RATE)
            + notes[4] * sin( get_freq(4) * 2 * pi * angles[4] / RATE)
            + notes[5] * sin( get_freq(5) * 2 * pi * angles[5] / RATE)
            + notes[6] * sin( get_freq(6) * 2 * pi * angles[6] / RATE)
            + notes[7] * sin( get_freq(7) * 2 * pi * angles[7] / RATE)
            + notes[8] * sin( get_freq(8) * 2 * pi * angles[8] / RATE)
            + notes[9] * sin( get_freq(9) * 2 * pi * angles[9] / RATE)
            + notes[10] * sin( get_freq(10) * 2 * pi * angles[10] / RATE)
            + notes[11] * sin( get_freq(11) * 2 * pi * angles[11] / RATE) )

        x = clip16(x * gain)
        
        blocks[bcount] = x
        if bcount == BLOCKSIZE - 1:
            disp_press(pressed, 120)
            bcount = 0

##            # Plot code
##            if sum(blocks) > 0 or sum(blocks) < 0:
##                pdata = np.append(pdata, blocks)
                
            data = struct.pack('h' * BLOCKSIZE, *blocks)
            stream.write(data)
            pygame.display.update()
        else:
            bcount += 1
        
        pygame.event.pump()

##    # Plot code
##    if len(pdata) != samp_len:
##        pud = samp_len - len(pdata)
##        pdata = np.append(pdata, np.zeros(pud))
##        len(pdata)
##    line1.set_ydata(pdata)
##    fig1.canvas.draw()
##    fig1.canvas.flush_events()
##    plt.ioff()
##    plt.show()

    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':

    main()
