import pygame
from pygame import mixer
import sys
import time
import random
pygame.init()
mixer.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
mixer.music.set_volume(1)
pygame.mixer.set_num_channels(13)
octave = 4
playing_notes = True
c1_key = pygame.Rect(4, 600, 96, 300)
d_key = pygame.Rect(104, 600, 96, 300)
e_key = pygame.Rect(204, 600, 96, 300)
f_key = pygame.Rect(304, 600, 96, 300)
g_key = pygame.Rect(404, 600, 96, 300)
a_key = pygame.Rect(504, 600, 96, 300)
b_key = pygame.Rect(604, 600, 96, 300)
c2_key = pygame.Rect(704, 600, 96, 300)
cs_key = pygame.Rect(70, 600, 70, 150)
ds_key = pygame.Rect(170, 600, 70, 150)
fs_key = pygame.Rect(370, 600, 70, 150)
gs_key = pygame.Rect(470, 600, 70, 150)
as_key = pygame.Rect(570, 600, 70, 150)
keys = [c1_key, d_key, e_key, f_key, g_key, a_key, b_key, c2_key, cs_key, ds_key, fs_key, gs_key, as_key]
key_colors = {'C1':False, 'D': False, 'E': False, 'F':False, 'G':False, 'A':False, 'B':False, 'C2':False, 'C#':False, 'D#':False, 'F#':False, 'G#':False, 'A#':False}

def get_random_key():
  x_list = [4, 104, 204, 304, 404, 504, 604, 704]
  x_sharp_list = [70, 170, 370, 470, 570]
  which_list = random.randint(1,2)
  if which_list == 2:
    x = random.choice(x_sharp_list)
    width = 70
    height = 200
    r = 6
    g = 22
    b = 43
  else:
    x = random.choice(x_list)
    width = 96
    height = 200
    r = 226
    g = 218
    b = 227
  return x, width, height, r, g, b
x, width, height, r, g, b = get_random_key()
y = 200
score = 0
velocity = 10
tiles_fallen = 0
velocity_increase = 0
lives = 5

win_img = pygame.image.load("win_screen.png")
win_img = pygame.transform.scale(win_img,(screen_width, screen_height))
lose_img = pygame.image.load("lose_screen.png")
lose_img = pygame.transform.scale(lose_img,(screen_width, screen_height))



def play_note(note_name, channel_number, note_file, lives, key_colors):
  key_colors[f'{note_name}'] = True

  pygame.mixer.Channel(channel_number).play(pygame.mixer.Sound(f'{note_file}'))
  if note_name == good_note:
    print("Good Note Hit")
    hit = True
    return hit, lives
  elif note_name != good_note:
    print("Wrong note!")
    lives = lives - 1
    print("Lost a life. Lives are now ", lives)
    hit = False
    return hit, lives
  

key_is_falling = True
hit = False

while playing_notes:

  while key_is_falling:

    if score == 101131111 or lives ==-1111111141110:
      if score == 10:
        game_verdict = 'win'
      elif lives == 0:
        game_verdict = 'lose'
      key_is_falling = False
      playing_notes = False


    if (tiles_fallen % 8) == 0 and tiles_fallen != 0:
      velocity_increase += 1.5
      velocity += velocity_increase
      tiles_fallen += 1

    if y >= 400:
      print("Failed Note Hit")
      lives = lives - 1
      velocity = 10
      print("New lives:", lives)
      x, width, height, r, g, b = get_random_key()
      y = 100
    else:

      screen.fill((189, 151, 30))
      pygame.time.delay(100)
      y += velocity
      pygame.draw.rect(screen, (r, g, b), (x, y, width, height))
      pygame.display.flip()

      for key, value in key_colors.items():
        if value
          pygame.draw.rect(screen, (255,255,255), i)
        else:
          pygame.draw.rect(screen, (0,0,0), i)
      pygame.display.flip()

      if x == 4:
        good_note = 'C1'
      elif x == 104:
        good_note = 'D'
      elif x == 204:
        good_note = 'E'
      elif x == 304:
        good_note = 'F'
      elif x == 404:
        good_note = 'G'
      elif x == 504:
        good_note = 'A'
      elif x == 604:
        good_note = 'B'
      elif x == 704:
        good_note = 'C2'
      elif x == 70:
        good_note = 'C#'
      elif x == 170:
        good_note = 'D#'
      elif x == 370:
        good_note = 'F#'
      elif x == 470:
        good_note = 'G#'
      elif x == 570:
        good_note = 'A#'  

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_z:
            if octave == 3:
              print("The piano doesn't have any lower keys!")
            else:
              octave = octave - 1
              print(f"Now in octave {octave}")
          if event.key == pygame.K_x:
            if octave == 5:
              print("The piano doesn't have any higher keys!")
            else:
              octave = octave + 1
              print(f"Now in octave {octave}")
              
          if event.key == pygame.K_a:
            hit, lives = play_note("C1", 0, f'./Octave {octave} Notes/c{octave}.mp3', lives, key_colors)

          if event.key == pygame.K_w:
            hit, lives = play_note("C#", 1, f'./Octave {octave} Notes/c-{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_s:
            hit, lives = play_note("D", 2, f'./Octave {octave} Notes/d{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_e:
            hit, lives = play_note("D#", 3, f'./Octave {octave} Notes/d-{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_d:
            hit, lives = play_note("E", 4, f'./Octave {octave} Notes/e{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_f:
            hit, lives = play_note("F", 5, f'./Octave {octave} Notes/f{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_t:
            hit, lives = play_note("F#", 6, f'./Octave {octave} Notes/f-{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_g:
            hit, lives = play_note("G", 7, f'./Octave {octave} Notes/g{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_y:
            hit, lives = play_note("G#", 8, f'./Octave {octave} Notes/g-{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_h:
            hit, lives = play_note("A", 9, f'./Octave {octave} Notes/a{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_u:
            hit, lives = play_note("A#", 10, f'./Octave {octave} Notes/a-{octave}.mp3', lives, key_colors)
          
          if event.key == pygame.K_j:
            hit, lives = play_note("B", 12, f'./Octave {octave} Notes/b{octave}.mp3', lives, key_colors)
            
          if event.key == pygame.K_k:
            high_c = octave + 1
            hit, lives = play_note("C2", 12, f'./Octave {octave} Notes/c{high_c}.mp3', lives, key_colors)
      if hit:
        score += 1
        tiles_fallen += 1
        print(score, 'score')
        print("next key...")
        x, width, height, r, g, b = get_random_key()
        y = 100
        hit = False

  if game_verdict == 'lose':
    screen.blit(lose_img, (0, 0))
    pygame.display.flip()
  elif game_verdict == 'win':
    screen.blit(win_img, (0, 0))
    pygame.display.flip()

  play_again_loop = True
  while play_again_loop:
    play_again = input("Do you want to play again? ('y' or 'n'): ")
    if play_again == 'y':
      print("Refresh the page lmao")
      play_again_loop = False
      playing_notes = False
    elif play_again == 'n':
      print("Goodbye!")
      play_again_loop = False
      playing_notes = False
    else:
      print("Invalid answer")
print("All loops ended")
