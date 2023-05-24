import pygame
from pygame import mixer
import sys
import random
pygame.init()
mixer.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
mixer.music.set_volume(1)
pygame.mixer.set_num_channels(13)
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
keys_rects = [c1_key, cs_key, d_key, ds_key, e_key, f_key, fs_key, g_key, gs_key, a_key, as_key, b_key, c2_key]
keys = [pygame.K_a, pygame.K_w,
pygame.K_s,
pygame.K_e,
pygame.K_d,
pygame.K_f,
pygame.K_t,
pygame.K_g,
pygame.K_y,
pygame.K_h,
pygame.K_u,
pygame.K_j,
pygame.K_k,
]
notes_list = ['C1', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C2']
sounds = ['c', 'c-', 'd', 'd-', 'e', 'f', 'f-', 'g', 'g-', 'a', 'a-', 'b', 'c']
keys_dict = {}
for i in range(len(keys)):
  keys_dict[keys[i]] = {'rect': keys_rects[i],'note': notes_list[i],'pressed': False,'channel': i,'sound': sounds[i]}


def get_valid_num(question, range):
  asking = True
  while asking:
    try:
      answer = int(input(question))
      if answer < 1 or answer > range:
        print("Answer not in proper range.")
      else:
        asking = False
    except:
      print("Not an integer answer.")
  return answer


playing = True
def play_game(playing):
  while playing:
      which_mode = get_valid_num("Do you wish to play endless mode or learn a new song? type '1' for endless, '2' for new song.", 2)
      if which_mode == 1:
        print("sdgfsdgsdg")
        playing = play_song('endless')
      elif which_mode == 2:
        playing = choose_preset_song()



def get_random_key():
  x_list = [8, 108, 208, 308, 408, 508, 608, 708]
  x_sharp_list = [70, 170, 370, 470, 570]
  which_list = random.randint(1,2)
  if which_list == 2:
    x = random.choice(x_sharp_list)
    width = 35
    height = 200
    r = 6
    g = 22
    b = 43
  else:
    x = random.choice(x_list)
    width = 88
    height = 200
    r = 226
    g = 218
    b = 227
  return x, width, height, r, g, b










win_img = pygame.image.load("win_screen.png")
win_img = pygame.transform.scale(win_img,(screen_width, screen_height))
lose_img = pygame.image.load("lose_screen.png")
lose_img = pygame.transform.scale(lose_img,(screen_width, screen_height))
learn_img = pygame.image.load("learn.png")
learn_img = pygame.transform.scale(learn_img,(screen_width, screen_height))



def play_note(note_name, channel_number, note_file, mistake, good_note):

  pygame.mixer.Channel(channel_number).play(pygame.mixer.Sound(f'{note_file}'))
  if note_name == good_note:
    print("Good Note Hit")
    hit = True
    return hit, mistake
  elif note_name != good_note:
    print("Wrong note!")
    mistake += 1
    print(f"Mistake. Now at {mistake} mistake(s)")
    hit = False
    return hit, mistake


def make_preset_song(song):


  if song == 'mii_channel':
    song_notes = [
      370,
      508,
      70,
      508,
      370,
      108,
      108,
      108,
      8,
      108,
      370,
      508,
      708,
      508,
    ]
    playing = play_song('song', song_notes, note_speed = 10)



def choose_preset_song():
  print("\n\n----------\nYour song options are:\n1. Mii Channel Theme\n")
  play_what_song = get_valid_num("Which song do you wish to play? Type the number beside the song.: ", 1)
  if play_what_song == 1:
    playing = make_preset_song('mii_channel')










def play_song(mode, song_notes = '', note_speed = 0):
  if mode == 'endless':
    x, width, height, r, g, b = get_random_key()
    score = 0
    tiles_fallen = 0
    velocity_increase = 0
    lives = 5
  hit = False
  mistake = 0
  y = 200
  note_count = 0
  score = 0
  velocity = 10
  octave = 4
  playing_notes = True
  key_is_falling = True

  while playing_notes:
    print("added note count")
    while key_is_falling:
      if mode == 'endless':
        if score == 10 or lives == 0:
          if score == 10:
            game_verdict = 'win'
          elif lives == 0:
            game_verdict = 'lose'
          key_is_falling = False
          playing_notes = False


        if (tiles_fallen % 5) == 0 and tiles_fallen != 0:
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

      else:
        if y >= 430:
          y = 100
          print("Failed Note Hit")
          note_count += 1
        if note_count > (len(song_notes) - 1):
          print("Song ended.")
          key_is_falling = False
          playing_notes = False
        else:
          x = song_notes[note_count]
          screen.fill((189, 151, 30))
          pygame.time.delay(100)
          y += note_speed
          pygame.draw.rect(screen, (255,255,255), (x, y, 60, 140))
      
        


      j = -1
      for key, value in keys_dict.items():
        j += 1
        if value['pressed'] == True:
          down_key = value['rect']
          pygame.draw.rect(screen, (128,128,128), down_key)
          
        else:
          rectangle = value['rect']
          if rectangle != cs_key and rectangle != ds_key and rectangle != fs_key and rectangle != gs_key and rectangle != as_key:
            pygame.draw.rect(screen, (255,255,255), rectangle)
          else:
            pygame.draw.rect(screen, (0,0,0), rectangle)
      pygame.display.flip()

      if x == 8:
        good_note = 'C1'
      elif x == 108:
        good_note = 'D'
      elif x == 208:
        good_note = 'E'
      elif x == 308:
        good_note = 'F'
      elif x == 408:
        good_note = 'G'
      elif x == 508:
        good_note = 'A'
      elif x == 608:
        good_note = 'B'
      elif x == 708:
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
          if event.key == pygame.K_LSHIFT:
            octave = 5
            print(octave, 'octave')
          elif event.key == pygame.K_LCTRL:
            octave = 3
            print(octave, 'octave')
          elif event.key in keys_dict:
            keys_dict[event.key]['pressed'] = True
            if event.key == pygame.K_k:
              high_c = octave + 1
              hit, mistake = play_note("C2", 12, f'./Octave {octave} Notes/c{high_c}.mp3', mistake, good_note)
            else:
              sound_file = keys_dict[event.key]['sound']
              hit, mistake = play_note(keys_dict[event.key]['note'], keys_dict[event.key]['channel'], f'./Octave {octave} Notes/{sound_file}{octave}.mp3',mistake, good_note)
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LCTRL or event.key == pygame.K_LSHIFT:
            octave = 4
          if event.key in keys_dict:
            keys_dict[event.key]['pressed'] = False



      if hit:
          if mode == 'endless':
            score += 1
            tiles_fallen += 1
            print(score, 'score')
            print("next key...")
            x, width, height, r, g, b = get_random_key()
            y = 100
          else:
            y = 100
            note_count += 1

          hit = False
      if mode == 'endless':
        if mistake == 3:
            print("3 mistakes. Lost a life.")
            lives -= 1
            print("Lives are now", lives)
            mistake = 0

      
    if mode == 'endless':
      if game_verdict == 'lose':
        screen.blit(lose_img, (0, 0))
        pygame.display.flip()
      elif game_verdict == 'win':
        screen.blit(win_img, (0, 0))
        pygame.display.flip()
      play_again_loop = True
    else:
      screen.blit(learn_img, (0, 0))
      pygame.display.flip()
      play_again_loop = True

  while play_again_loop:
    play_again = input("Do you want to play again? ('y' or 'n'): ")
    if play_again == 'y':
      play_again_loop = False
      playing_notes = False
    elif play_again == 'n':
      print("Goodbye!")
      play_again_loop = False
      playing_notes = False
      return False
    else:
      print("Invalid answer")

play_game(playing)
print("All loops ended")
