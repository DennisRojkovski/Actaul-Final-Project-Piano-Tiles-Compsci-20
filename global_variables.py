import pygame
from pygame import mixer
#File for all variables.
pygame.init()
mixer.init()
#Makes screen size
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
#sets colors black and white to their RGB code
black = (0,0,0)
white = (255, 255, 255)
#Opens and reads highscore file as the highscore
with open("highscore.txt", 'r+') as highscore_file:
  highscore = highscore_file.read()
#Sets different fonts to the same font with different sizes
keys_font = pygame.font.SysFont('Verdana',  30)
message_font = pygame.font.SysFont('Verdana', 20)
tips_font = pygame.font.SysFont('Verdana', 14)
#Sets different letters to be rendered as the key names
letter_1 = keys_font.render("A", False, black, white)
letter_2 = keys_font.render("S", False, black, white)
letter_3 = keys_font.render("D", False, black, white)
letter_4 = keys_font.render("F", False, black, white)
letter_5 = keys_font.render("G", False, black, white)
letter_6 = keys_font.render("H", False, black, white)
letter_7 = keys_font.render("J", False, black, white)
letter_8 = keys_font.render("K", False, black, white)
letter_9 = keys_font.render("W", False, white, black)
letter_10 = keys_font.render("E", False, white, black)
letter_11 = keys_font.render("T", False, white, black)
letter_12 = keys_font.render("Y", False, white, black)
letter_13 = keys_font.render("U", False, white, black)
#Loads all images from their files, transforms them to fit the entire screen
win_img = pygame.image.load("win_screen.png")
win_img = pygame.transform.scale(win_img,(screen_width, screen_height))
lose_img = pygame.image.load("lose_screen.png")
lose_img = pygame.transform.scale(lose_img,(screen_width, screen_height))
learn_img = pygame.image.load("learn.png")
learn_img = pygame.transform.scale(learn_img,(screen_width, screen_height))

#Sets messages to be displayed during the game
start_message = message_font.render("Press the right key to begin.", False, black)
record_message = message_font.render(f"All-time record: {highscore}", False, black)
help_message_1 = tips_font.render("When the background turns RED, hold LSHIFT.", False, black)
help_message_2 = tips_font.render("When the background turns YELLOW, let go.", False, black)
key_names = [letter_1, letter_2, letter_3, letter_4, letter_5, letter_6, letter_7, letter_8]
sharp_names = [letter_9, letter_10, letter_11, letter_12, letter_13]
#Sets music channels and volume
mixer.music.set_volume(1)
pygame.mixer.set_num_channels(13)
#Creates rectangles in the right position and the right size
c1_key = pygame.Rect(8, 600, 88, 300)
d_key = pygame.Rect(108, 600, 88, 300)
e_key = pygame.Rect(208, 600, 88, 300)
f_key = pygame.Rect(308, 600, 88, 300)
g_key = pygame.Rect(408, 600, 88, 300)
a_key = pygame.Rect(508, 600, 88, 300)
b_key = pygame.Rect(608, 600, 88, 300)
c2_key = pygame.Rect(708, 600, 88, 300)
cs_key = pygame.Rect(70, 600, 70, 150)
ds_key = pygame.Rect(170, 600, 70, 150)
fs_key = pygame.Rect(370, 600, 70, 150)
gs_key = pygame.Rect(470, 600, 70, 150)
as_key = pygame.Rect(570, 600, 70, 150)
#Makes a list of all keys
keys_rects = [c1_key, cs_key, d_key, ds_key, e_key, f_key, fs_key, g_key, gs_key, a_key, as_key, b_key, c2_key]
#Makes a list of all pygame keydown functions
keys = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_d, pygame.K_f, pygame.K_t, pygame.K_g, pygame.K_y, pygame.K_h, pygame.K_u, pygame.K_j, pygame.K_k]
#Makes list of all note names
notes_list = ['C1', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C2']
#Makes list of all sound names
sounds = ['c', 'c-', 'd', 'd-', 'e', 'f', 'f-', 'g', 'g-', 'a', 'a-', 'b', 'c']