#Import all libraries
#Imports all variables from the global variables file
from global_variables import *
import pygame
import sys
import random

#Makes a master dictionary that contains every key. Every key has it's own dictionary containing values such as it's current pressed state, the key name, the sound etc.
keys_dict = {}
for i in range(len(keys)):
  keys_dict[keys[i]] = {'rect': keys_rects[i],'note': notes_list[i],'pressed': False,'channel': i,'sound': sounds[i]}
#Function to get a valid number
def get_valid_num(question, range):
  asking = True
  while asking:
#Gets valid number by checking if the input is within the proper range, returns the answer if it is valid
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
#Function to choose game mode
playing = True
def play_game(playing):
  while playing:
#Gets valid number, if 1, starts endless mode. If 2, starts preset song mode.
      which_mode = get_valid_num("Do you wish to play random mode or learn a new song? type '1' for random, '2' for new song or 3 to quit: ", 3)
      if which_mode == 1:
        chosen_lives = get_valid_num("How many lives do you wish to have? (min 1, max 10): ", 10)
        chosen_max = get_valid_num("What score do you wish to be the winning score? (10 is a little, 50 is a good amount, 100+ is insane. Type '0' for no limit.): ", None)
#If the user wants no score limit, pass in chosen_max as a None value.
        if not chosen_max:
          chosen_max == None
        playing = play_song('endless', chosen_lives = chosen_lives, chosen_max = chosen_max)
      elif which_mode == 2:
        playing = choose_preset_song()
#If user wants to quit, end the playing loop
      else:
        playing = False
#Function to choose a random key for endless mode
def get_random_key():
#Makes list of all keys
  x_list = [8, 108, 208, 308, 408, 508, 608, 708]
  x_sharp_list = [70, 170, 370, 470, 570]
#Chooses either sharp or natural key
  which_list = random.randint(1, 2)
#If sharp, choose from sharp list and set color / size values to sharp key values.
  if which_list == 2:
    x = random.choice(x_sharp_list)
    width = 35
    height = 200
    r = 6
    g = 22
    b = 43
#If natural, set color/size to natural key values
  else:
    x = random.choice(x_list)
    width = 88
    height = 200
    r = 226
    g = 218
    b = 227
#Return new key size, location and color. The key's location is an x-coordinate on the screen plane
  return x, width, height, r, g, b

#Function to play the note. Passes in multiple variables to be modified
def play_note(note_name, channel_number, note_file, mistake, good_note, total_mistake):
  #Plays the right sound based on the given channel number and sound file
  pygame.mixer.Channel(channel_number).play(pygame.mixer.Sound(f'{note_file}'))
  #If the user pressed the right note, return True hit 
  if note_name == good_note:
    hit = True
    return hit, mistake, total_mistake
  #If the user pressed the wrong note, return False hit and add 1 to all mistakes.
  elif note_name != good_note:
    mistake += 1
    total_mistake += 1
    hit = False
    return hit, mistake, total_mistake
#Function to make the preset songs
def make_preset_song(song):
#Sets empty lists
  song_notes = []
  song_octaves = []
  note_lengths = []
#If mii_channel, open the mii channel file and get all info from it. Set the title screen to 'mii channel theme'
  if song == 'mii_channel':
    with open('mii_song.txt') as mii_song_file:
      song_info = mii_song_file.readlines()
    mii_song_message = message_font.render("Mii Channel Theme", False, black)
#If mii maker song, open the right folder and read its contents.
  elif song == 'mii_maker':
    with open('mii_maker.txt') as mii_song_file:
      song_info = mii_song_file.readlines()
    mii_song_message = message_font.render("Mii Maker 3DS Theme", False, black)
#Loops through every line in the file, split by commas.
  for line_list in song_info:
    current_line = line_list.split(",")
#Removes whitespace
    current_line[-1] = current_line[-1].strip()
#Append different parts of the file line to the right lists. Repeat for all lines in the file.
    song_notes.append(current_line[0])
    song_octaves.append(current_line[1])
    note_lengths.append(current_line[-1])
#Removes '\n' from the info, multiplies all values by 2 effectively making the song 2x longer
  song_notes = (list(map(str.strip, song_notes))) * 2
  song_octaves = (list(map(str.strip, song_octaves))) * 2
#Sets all info to integers
  for note in range(len(song_notes)):
      song_notes[note] = int(song_notes[note])
#Makes a dictionary containing all song info
  song_info_dictionary = {
      'song_notes': song_notes,
      'song_octaves': song_octaves,
      'note_lengths': note_lengths
    }
#Runs play song function passing in the whole dictionary as well as the 'song' gamemode. 
  playing = play_song('song', song_info_dictionary, mii_song_message, note_speed = 10)
  return playing
#Function to choose preset song
def choose_preset_song():
#Gets valid number in range with the get_valid_num function, runs the make_song function with either mii channel or mii maker song passed in.
  print("\n\n----------\nYour song options are:\n1. Mii Channel Theme\n2. Mii Maker 3DS Theme")
  play_what_song = get_valid_num("Which song do you wish to play? Type the number beside the song.: ", 2)
  if play_what_song == 1:
    playing = make_preset_song('mii_channel')
  elif play_what_song == 2:
    playing = make_preset_song('mii_maker')
  return playing

#Main body function, passes in all necessary info.
def play_song(mode, song_info_dictionary = None, song_message = '', note_speed = 0, chosen_lives = 10, chosen_max = None):
#Reads highscore file and stores it
  with open("highscore.txt") as highscore_file:
    highscore = int(highscore_file.read())
#If endless mode, get a random key location and set different variables to the right values
  if mode == 'endless':
    x, width, height, r, g, b = get_random_key()
    score = 0
    velocity_increase = 0
    lives = chosen_lives
    velocity_increase = 1.25
#Set general variables
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
#while playing, run the following loops.
  while playing_notes:
    while key_is_falling:
#If no tiles have fallen, accuracy is 100%.
      if tiles_fallen == 0:
        accuracy_percent = '100'
#Else get accuracy with total tiles fallen compared to total + mistake logic. Round to 1 decimal point
      else:
        accuracy_percent = round((((tiles_fallen)/(tiles_fallen + total_mistake)) * 100), 1)
#Sets messages to be changed during the game, displaying high score, mistakes, score and accuracy
      record_message = message_font.render(f"All-time record: {highscore}", False, black)
      mistake_message = message_font.render(f"{mistake} mistake(s)", False, black)
      score_message = message_font.render(f"score: {score}", False, black)
      accuracy_message = message_font.render(f"Accuracy: {accuracy_percent}%", False, black)

#If endless, run the following body code.
      if mode == 'endless':
#Displays lives
        if lives > 1:
          lives_message = message_font.render(f"{lives} lives", False, black)
        else:
          lives_message = message_font.render("1 life", False, black)
#If chosen max is not 0, check if the player has won. If yes, end game. If no, continue.
        if chosen_max != 0:
          if score == chosen_max:
            game_verdict = 'win'
            key_is_falling = False
            playing_notes = False
#If ever lives are 0, game over, game verdict is lose.
        elif lives == 0:
          game_verdict = 'lose'
          key_is_falling = False
          playing_notes = False
#Every five tiles fallen, increase the velocity of the tiles by the set amount. Add 1 to tiles fallen.
        if (tiles_fallen % 5) == 0 and tiles_fallen != 0:
          velocity += velocity_increase
          tiles_fallen += 1
#The tiles work on a coordinate system of x and y values. If the y value is greater than 400, the key has touched the bottom.
# Add 1 to mistakes, remove a life and get a new random key.
        if y >= 400:
          lives = lives - 1
          total_mistake += 1
          velocity = 10
          x, width, height, r, g, b = get_random_key()
          y = 100
#If the game has not started, tell the user to press the right keys. Keep the current key in place until it is pressed.
        else:
          if tiles_fallen == 0:
            screen.fill((189, 151, 30))
            screen.blit(start_message, (180,570))
            y = y
#If the key is just falling, move the key down by the given velocity every so often using pygame delays.
          else:
            screen.fill((189, 151, 30))
            pygame.time.delay(100)
            y += velocity
          pygame.draw.rect(screen, (r, g, b), (x, y, width, height))

#Elif gamemode is set song mode, run the following body code.
      else:
#If hit, reset the y-value of the key, add 1 to mistakes.
        if y >= 430:
          y = 100
          total_mistake += 1
          note_count += 1
#If the song is over, end the game.
        if note_count > (len(song_info_dictionary['song_notes']) - 1):
          key_is_falling = False
          playing_notes = False
#Checks song octave value from dictionary. If 2, change color to red. If 0, change to blue. Else change to yellow.
        else:
          if song_info_dictionary['song_octaves'][tiles_fallen] == '2':
            screen.fill((230, 97, 45))
          elif song_info_dictionary['song_octaves'][tiles_fallen] == '0':
            screen.fill((80,100,240))
          else:
            screen.fill((189, 151, 30))
#New note value is the x-value from the dictionary, in the place of the current note count.
          x = song_info_dictionary['song_notes'][note_count]
          pygame.time.delay(100)
#If game not started, blit start message.
          if tiles_fallen == 0:
            screen.blit(start_message, (180,570))
#While game is running, make tile fall by given value. Depending on if the key is sharp or natural,
#draw the key black or white, and with a different size respectively.
          else:
            y += note_speed
          if x != 70 and x != 170 and x != 370 and x != 470 and x != 570:
            pygame.draw.rect(screen, (255,255,255), (x, y, 88, 200))
          else:
            pygame.draw.rect(screen, (0,0,0), (x, y, 35, 200))

#In all game modes, run the following code. Draws all aspects of the game.
      for key, value in keys_dict.items():
#Colors pressed keys gray.
        if value['pressed'] == True:
          down_key = value['rect']
          pygame.draw.rect(screen, (128,128,128), down_key)
#Depending on what rectangle is being drawn, draw it as a sharp or natural key.
        else:
          rectangle = value['rect']
          if rectangle != cs_key and rectangle != ds_key and rectangle != fs_key and rectangle != gs_key and rectangle != as_key:
            pygame.draw.rect(screen, (255,255,255), rectangle)
          else:
            pygame.draw.rect(screen, (0,0,0), rectangle)
#For every key letter name, draw the letter. Add 100 to the x-distance, and draw the next. Evenly draws all keys on the screen.
      key_location = 40
      for key_name in key_names:
        screen.blit(key_name, (key_location, 760))
        key_location += 100
#Once all natural keys have been drawn, repeat the process for sharps. Since there is a gap in the sharp keys, once the program
#gets to that gap, skip over one more value and continue drawing
      key_location = 75
      key_counter = 0
      for key_name in sharp_names:
        screen.blit(key_name, (key_location, 700))
        key_counter += 1
        if key_counter == 2:
          key_location += 202
        else:
          key_location += 101
#If endless mode, draw all endless mode messages. If the user gets a new highscore, set highscore to their score.
      if mode == 'endless':
        screen.blit(mistake_message, (20, 35))
        screen.blit(lives_message, (20, 60))
        screen.blit(score_message, (300, 50))
        screen.blit(record_message, (550, 10))
        if score > highscore:
          highscore = score
#If set mode, draw all helpful messages.
      else:
        screen.blit(song_message, (230, 30))
        screen.blit(help_message_1, (450, 60))
        screen.blit(help_message_2, (450, 80))
      screen.blit(accuracy_message, (20, 85))

#Once everything has been drawn, refresh the page.
      pygame.display.flip()

#Depending on the x-value of the current key, set the right note to its respective position
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
#Gets user inputs from pygame event function
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
#If key down, run the following.
        if event.type == pygame.KEYDOWN:
#If shift or control are pressed, change the octave value to 5 or 3 respectively
          if event.key == pygame.K_LSHIFT:
            octave = 5
          elif event.key == pygame.K_LCTRL:
            octave = 3
#If any keys in the keys dictionary have been pressed, run the following
          elif event.key in keys_dict:
#Set that key's pressed value to true.
            keys_dict[event.key]['pressed'] = True
#Special case - If K is pressed, add 1 to the octave count. This is the high C note and has to be played an octave higher.
            if event.key == pygame.K_k:
              high_c = octave + 1
              hit, mistake, total_mistake = play_note("C2", 12, f'./Octave {octave} Notes/c{high_c}.mp3', mistake, good_note, total_mistake)
#In all other cases, set sound file to the right sound. Run the play note function passing in all proper values including the note name, the octave, sound, mistakes, etc.
            else:
              sound_file = keys_dict[event.key]['sound']
              hit, mistake, total_mistake = play_note(keys_dict[event.key]['note'], keys_dict[event.key]['channel'], f'./Octave {octave} Notes/{sound_file}{octave}.mp3',mistake, good_note, total_mistake)
#Once the key has been lifted, if key is CTRL or SHIFT, change octave back to 4.
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LCTRL or event.key == pygame.K_LSHIFT:
            octave = 4
#Else change the 'pressed' value of the right key back to false.
          if event.key in keys_dict:
            keys_dict[event.key]['pressed'] = False
#If succeeded to press the key, run the following
      if hit:
#If endless mode, add 1 to score, get new random key location. 
          if mode == 'endless':
            score += 1
            tiles_fallen += 1
            x, width, height, r, g, b = get_random_key()
            y = 100
#Else reset key and add 1 to total tiles fallen count.
          else:
            y = 100
            note_count += 1
            tiles_fallen += 1
          hit = False
#Forever check for 3 mistakes. If 3, take away one life and reset mistakes to 0.
      if mode == 'endless':
        if mistake == 3:
            lives -= 1
            mistake = 0
#Once the game is over, if endless mode, depending on game verdict, display win or lose screen.
    if mode == 'endless':
      if game_verdict == 'lose':
        screen.blit(lose_img, (0, 0))
        pygame.display.flip()
      elif game_verdict == 'win':
        screen.blit(win_img, (0, 0))
        pygame.display.flip()
      play_again_loop = True
#Else once the song is over, display 'you learned something new' screen
    else:
      screen.blit(learn_img, (0, 0))
      pygame.display.flip()
      play_again_loop = True
#Opens the high score file and appends, even if the user did not set a new high score
  with open('highscore.txt', 'w') as highscore_file:
    highscore_file.write(str(highscore))
#Sets a play again loop, asks if the user wants to play again.
  while play_again_loop:
    play_again = input("Do you want to play again? ('y' or 'n'): ").lower()
#If play again, reset all variables. If no, end the game.
    if play_again == 'y':
      play_again_loop = False
      playing_notes = False
      return True
    elif play_again == 'n':
      print("Goodbye!")
      play_again_loop = False
      playing_notes = False
      return False
#If invalid, ask again.
    else:
      print("Invalid answer")
#Starts game
play_game(playing)