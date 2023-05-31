
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
keys_font = pygame.font.SysFont('Verdana',  30)
message_font = pygame.font.SysFont('Verdana', 20)
tips_font = pygame.font.SysFont('Verdana', 14)
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
keys = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_d, pygame.K_f, pygame.K_t, pygame.K_g, pygame.K_y, pygame.K_h, pygame.K_u, pygame.K_j, pygame.K_k]
notes_list = ['C1', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C2']
sounds = ['c', 'c-', 'd', 'd-', 'e', 'f', 'f-', 'g', 'g-', 'a', 'a-', 'b', 'c']
keys_dict = {}
for i in range(len(keys)):
  keys_dict[keys[i]] = {'rect': keys_rects[i],'note': notes_list[i],'pressed': False,'channel': i,'sound': sounds[i]}

with open("highscore.txt", 'r+') as highscore_file:
  highscore = highscore_file.read()

def get_valid_num(question, range):
  asking = True
  while asking:
    try:
      answer = int(input(question))
      if range != None:
        if answer < 1 or answer > range:
          print("Answer not in proper range.")
        else:
          asking = False
      else:
        if answer < 0:
          print("Answer not in proper range.")
        else:
          asking = False
    except:
      print("Not an integer answer.")
  return answer


playing = True
def play_game(playing):
  while playing:
      which_mode = get_valid_num("Do you wish to play random mode or learn a new song? type '1' for random, '2' for new song or 3 to quit: ", 3)
      if which_mode == 1:
        chosen_lives = get_valid_num("How many lives do you wish to have? (min 1, max 10): ", 10)
        chosen_max = get_valid_num("What score do you wish to be the winning score? (10 is a little, 50 is a good amount, 100+ is insane. Type '0' for no limit.): ", None)
        if not chosen_max:
          chosen_max == None
        playing = play_song('endless', chosen_lives = chosen_lives, chosen_max = chosen_max)
      elif which_mode == 2:
        playing = choose_preset_song()
      else:
        playing = False

def get_random_key():
  x_list = [8, 108, 208, 308, 408, 508, 608, 708]
  x_sharp_list = [70, 170, 370, 470, 570]
  which_list = random.randint(1, 2)
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

black = (0,0,0)
white = (255, 255, 255)

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
start_message = message_font.render("Press the right key to begin.", False, black)
record_message = message_font.render(f"All-time record: {highscore}", False, black)
help_message_1 = tips_font.render("When the background turns RED, hold LSHIFT.", False, black)
help_message_2 = tips_font.render("When the background turns YELLOW, let go.", False, black)

key_names = [letter_1, letter_2, letter_3, letter_4, letter_5, letter_6, letter_7, letter_8]
sharp_names = [letter_9, letter_10, letter_11, letter_12, letter_13]

def play_note(note_name, channel_number, note_file, mistake, good_note, total_mistake):

  pygame.mixer.Channel(channel_number).play(pygame.mixer.Sound(f'{note_file}'))
  if note_name == good_note:
    hit = True
    return hit, mistake, total_mistake
  elif note_name != good_note:
    mistake += 1
    total_mistake += 1
    hit = False
    return hit, mistake, total_mistake


def make_preset_song(song):
  if song == 'mii_channel':
    song_notes = []
    song_octaves = []
    with open('mii_song.txt') as mii_song_file:
      song_info = mii_song_file.readlines()
  j = 0
  for info in song_info:
    j += 1
    if (j % 2) == 1:
      song_notes.append(info)
    else:
      song_octaves.append(info)
  song_notes = (list(map(str.strip, song_notes))) * 2
  song_octaves = (list(map(str.strip, song_octaves))) * 2
  for note in range(len(song_notes)):
    song_notes[note] = int(song_notes[note])
  mii_song_message = message_font.render("Mii Channel Theme", False, black)
  playing = play_song('song', song_notes, mii_song_message, song_octaves, note_speed = 10)



def choose_preset_song():
  print("\n\n----------\nYour song options are:\n1. Mii Channel Theme\n")
  play_what_song = get_valid_num("Which song do you wish to play? Type the number beside the song.: ", 1)
  if play_what_song == 1:
    playing = make_preset_song('mii_channel')


def play_song(mode, song_notes = '', song_message = '', song_octaves = None, note_speed = 0, chosen_lives = 10, chosen_max = None):
  with open("highscore.txt") as highscore_file:
    highscore = int(highscore_file.read())
  if mode == 'endless':
    x, width, height, r, g, b = get_random_key()
    score = 0
    velocity_increase = 0
    lives = chosen_lives
  tiles_fallen = 0
  hit = False
  total_mistake = 0
  mistake = 0
  y = 200
  accuracy_percent = 100
  note_count = 0
  score = 0
  velocity = 10
  octave = 4
  playing_notes = True
  key_is_falling = True
  while playing_notes:
    while key_is_falling:

      if tiles_fallen == 0:
        accuracy_percent = '100'
      else:
        accuracy_percent = round((((tiles_fallen)/(tiles_fallen + total_mistake)) * 100), 1)
      record_message = message_font.render(f"All-time record: {highscore}", False, black)
      mistake_message = message_font.render(f"{mistake} mistake(s)", False, black)
      score_message = message_font.render(f"score: {score}", False, black)
      accuracy_message = message_font.render(f"Accuracy: {accuracy_percent}%", False, black)
      if mode == 'endless':
        if lives > 1:
          lives_message = message_font.render(f"{lives} lives", False, black)
        else:
          lives_message = message_font.render("1 life", False, black)
        if chosen_max != 0:
          if score == chosen_max:
            game_verdict = 'win'
            key_is_falling = False
            playing_notes = False
        elif lives == 0:
          game_verdict = 'lose'
          key_is_falling = False
          playing_notes = False


        if (tiles_fallen % 5) == 0 and tiles_fallen != 0:
          velocity_increase += 1.25
          velocity += velocity_increase
          tiles_fallen += 1

        if y >= 400:
          lives = lives - 1
          total_mistake += 1
          velocity = 10
          x, width, height, r, g, b = get_random_key()
          y = 100
        else:
          if tiles_fallen == 0:
            screen.fill((189, 151, 30))
            screen.blit(start_message, (180,570))
            y = y
          else:
            screen.fill((189, 151, 30))
            pygame.time.delay(100)
            y += velocity
          pygame.draw.rect(screen, (r, g, b), (x, y, width, height))
      else:
        if song_octaves[tiles_fallen] == '2':
          screen.fill((230, 97, 45))
        elif song_octaves[tiles_fallen] == '0':
          screen.fill((80,100,240))
        else:
          screen.fill((189, 151, 30))

        if y >= 430:
          y = 100
          total_mistake += 1
          note_count += 1
        if note_count > (len(song_notes) - 1):
          key_is_falling = False
          playing_notes = False
        else:
          x = song_notes[note_count]
          pygame.time.delay(100)
          if tiles_fallen == 0:
            screen.blit(start_message, (180,570))
          else:
            y += note_speed
          if x != 70 and x != 170 and x != 370 and x != 470 and x != 570:
            pygame.draw.rect(screen, (255,255,255), (x, y, 88, 200))
          else:
            pygame.draw.rect(screen, (0,0,0), (x, y, 35, 200))
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
        key_location = 40
      for key_name in key_names:
        screen.blit(key_name, (key_location, 760))
        key_location += 100
      key_location = 75
      key_counter = 0
      for key_name in sharp_names:
        screen.blit(key_name, (key_location, 700))
        key_counter += 1
        if key_counter == 2:
          key_location += 202
        else:
          key_location += 101
      if mode == 'endless':
        screen.blit(mistake_message, (20, 35))
        screen.blit(lives_message, (20, 60))
        screen.blit(score_message, (300, 50))
        if score > highscore:
          highscore = score
        screen.blit(record_message, (550, 10))
      else:
        screen.blit(song_message, (230, 30))
        screen.blit(help_message_1, (450, 60))
        screen.blit(help_message_2, (450, 80))


      screen.blit(accuracy_message, (20, 85))
        
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
          elif event.key == pygame.K_LCTRL:
            octave = 3
          elif event.key in keys_dict:
            keys_dict[event.key]['pressed'] = True
            if event.key == pygame.K_k:
              high_c = octave + 1
              hit, mistake, total_mistake = play_note("C2", 12, f'./Octave {octave} Notes/c{high_c}.mp3', mistake, good_note, total_mistake)
            else:
              sound_file = keys_dict[event.key]['sound']
              hit, mistake, total_mistake = play_note(keys_dict[event.key]['note'], keys_dict[event.key]['channel'], f'./Octave {octave} Notes/{sound_file}{octave}.mp3',mistake, good_note, total_mistake)
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LCTRL or event.key == pygame.K_LSHIFT:
            octave = 4
          if event.key in keys_dict:
            keys_dict[event.key]['pressed'] = False

      if hit:
          if mode == 'endless':
            score += 1
            tiles_fallen += 1
            x, width, height, r, g, b = get_random_key()
            y = 100
          else:
            y = 100
            note_count += 1
            tiles_fallen += 1
          hit = False

      if mode == 'endless':
        if mistake == 3:
            lives -= 1
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
  with open('highscore.txt', 'w') as highscore_file:
    highscore_file.write(str(highscore))
  while play_again_loop:
    play_again = input("Do you want to play again? ('y' or 'n'): ").lower()
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
