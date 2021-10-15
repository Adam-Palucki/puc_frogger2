# Pythons Lessons - Trening 10 FROGGER - how we use classes, lists, basic game concepts
# PARALLEL UNIVERSE CODERS
# Adam Pałucki
# XII 2020

# ***** Libraries IMPORT section *****
from random import randint  # used to randomize integers
import sys  # used for operating system commands such as exit a game,
import shelve  # easy open and save objects to and from files
import os

import pgzrun
# this line can be deleted if you use MU editor, but is needed in other IDE's. This is import of pygame
# zero library

# ***** END of Libraries IMPORT section *****

# ***** VARIABLES AND CONSTANTS DECLARATIONS *****
WIDTH = 820  # width of the game window
HEIGHT = 800  # height of the game window
BACKGROUND = 'zaba'  # background file
ANCHOR = ('left', 'top')  # left top corner will be the anchor
ANCHOR_BOTTOM = ('middle', 'bottom')
BUTTON_BCKGRND = 'blue_button01'  # background for buttons
COLOR_TXT_BUTTON = (255, 255, 255)  # RGB - WHITE
COLOR_RANKING_TABLE = (66, 135, 245)  # RGB - LIGHT GREEN
KEYS_SENSITIVITY = 8  # bigger value -> keys less sensitive
CARS_FOLDER_NAME = 'cars'
difficulty_level = 'Easy'  # starting difficulty level - low letters because it can be changed during a game
DIFFICULTY_LEVEL_DICT = {'Easy': {
    'lives': 5,
    'frog_speed': 50,
    'cars_speed': 4,
    'car_space': 600
}, 'Normal': {
    'lives': 4,
    'frog_speed': 50,
    'cars_speed': 6,
    'car_space': 400
}, 'Hard': {
    'lives': 3,
    'frog_speed': 50,
    'cars_speed': 8,
    'car_space': 350
}}  # difficulty levels dict

# sound volume can be set between 0 and 1
SOUND_VOLUME = 0.5

# starting position of the Frog:
X_START = WIDTH // 2
Y_START = HEIGHT - 50

ROAD_TILE = 'road_tile'  # road tile to create highway as a background
UNSEEN = 200  # variable describes how far cars will go outside visible screen

# ***** default starting flags and variables *****
name_input_active = False  # if change player name input box is active?
PLAYER_NAME_INPUT_BOX = Rect((WIDTH // 2 - 150, HEIGHT // 4 + 50), (300, 50))

GAME_TIME = 60  # how much time do You have to cross the highway
game_time = GAME_TIME
player_score = 0  # set starting value
game_stage = 'start_game'  # starting stage of the game - welcome screen

# MU searching for images in 'images' folder by default but os path is different (os = operating system)
cars_image_os_folder = './images/' + CARS_FOLDER_NAME + '/'
cars_image_mu_folder = './' + CARS_FOLDER_NAME + '/'
# ***** END OF VARIABLES AND CONSTANTS DECLARATIONS *****

# ***** CLASSES DECLARATIONS *****
# buttons and screens:
class Button(Actor):  # we are using pygame zero Actor class - are You remember first lessons?
    writing = ''

    def __init__(self, button_picture, pos, writing):  # special method to start instance of the class
        super().__init__(button_picture, center=pos)  # special method calling to 'activate' parent class'
        self.pos = pos  # button position
        self.writing = writing  # what do you want to be written on the button?


class Screen:
    background = ''
    title = ''

    def __init__(self, background, title=''):
        self.background = background
        self.title = title

    def show(self):
        screen.clear()
        background = Actor(self.background)
        background.draw()
        screen.draw.text(self.title, midtop=(WIDTH // 2, HEIGHT // 8), fontsize=40,
                         color=COLOR_TXT_BUTTON)  # drawing title

    def show_button_play(self):
        PLAY_BTN.draw()
        screen.draw.text(PLAY_BTN.writing, midtop=(PLAY_BTN.x, PLAY_BTN.y - 16), fontsize=40, color=COLOR_TXT_BUTTON)

    def show_button_ranking(self):
        RANKING_BTN.draw()
        screen.draw.text(RANKING_BTN.writing, midtop=(RANKING_BTN.x, RANKING_BTN.y - 16), fontsize=40,
                         color=COLOR_TXT_BUTTON)

    def show_button_change_name(self):
        CHANGE_NAME_BTN.draw()
        screen.draw.text(CHANGE_NAME_BTN.writing, midtop=(CHANGE_NAME_BTN.x, CHANGE_NAME_BTN.y - 10), fontsize=30,
                         color=COLOR_TXT_BUTTON)

    def show_button_set_level(self):
        SET_LVL_BTN.draw()
        screen.draw.text(SET_LVL_BTN.writing, midtop=(SET_LVL_BTN.x, SET_LVL_BTN.y - 16), fontsize=40,
                         color=COLOR_TXT_BUTTON)

    def show_button_quit(self):
        QUIT_BTN.draw()
        screen.draw.text(QUIT_BTN.writing, midtop=(QUIT_BTN.x, QUIT_BTN.y - 16), fontsize=40, color=COLOR_TXT_BUTTON)

    def show_button_play_again(self):
        PLAY_AGAIN_BTN.draw()
        screen.draw.text(PLAY_AGAIN_BTN.writing, midtop=(PLAY_AGAIN_BTN.x, PLAY_AGAIN_BTN.y - 16), fontsize=40,
                         color=COLOR_TXT_BUTTON)

    def show_button_back(self):
        BACK_BTN.draw()
        screen.draw.text(BACK_BTN.writing, midtop=(BACK_BTN.x, BACK_BTN.y - 16), fontsize=40, color=COLOR_TXT_BUTTON)

    def show_button_save(self):
        SAVE_BTN.draw()
        screen.draw.text(SAVE_BTN.writing, midtop=(SAVE_BTN.x, SAVE_BTN.y - 16), fontsize=44, color=COLOR_TXT_BUTTON)

    def show_button_easy(self):
        EASY_BTN.draw()
        screen.draw.text(EASY_BTN.writing, midtop=(EASY_BTN.x, EASY_BTN.y - 16), fontsize=44, color=COLOR_TXT_BUTTON)

    def show_button_normal(self):
        NORMAL_BTN.draw()
        screen.draw.text(NORMAL_BTN.writing, midtop=(NORMAL_BTN.x, NORMAL_BTN.y - 16), fontsize=44,
                         color=COLOR_TXT_BUTTON)

    def show_button_hard(self):
        HARD_BTN.draw()
        screen.draw.text(HARD_BTN.writing, midtop=(HARD_BTN.x, HARD_BTN.y - 16), fontsize=44, color=COLOR_TXT_BUTTON)


# Player - The Frog
class Frog(Actor):
    def __init__(self, picture, pos):  # special method which is always run while creating avery object of this class
        super().__init__(picture, center=pos, anchor=ANCHOR)  # calling __init__ of the parent
        self.image = picture
        self.pos = pos
        self.speed = DIFFICULTY_LEVEL_DICT[difficulty_level]['frog_speed']
        self.lives = DIFFICULTY_LEVEL_DICT[difficulty_level]['lives']
        self.rect = Rect(self.pos, self.size)  # collision rectangle
        self.name = 'Player 1'
        self.score = 0
        self.cool_time = 0  #

    def update(self):  # update of the Frog
        self.rect = Rect(self.pos, self.size)  # collision rectangle

# the Car class
class Car(Actor):
    def __init__(self, picture, pos):   # special method which is always run while creating avery object of this class
        super().__init__(picture, center=pos, anchor=ANCHOR_BOTTOM)    # calling __init__ of the parent
        self.image = picture
        self.pos = pos
        self.speed = 3
        new_position = [self.x - (self.width // 2), self.y - self.height]
        self.rect = Rect(new_position, self.size)  # collision rectangle

    def update(self):
        new_position = [self.x - (self.width // 2), self.y - self.height]
        self.rect = Rect(new_position, self.size)  # colission rectangle
# ***** END OF CLASSES DECLARATIONS *****

# ***** CREATING ACTORS AND OBJECTS  INITIALISATIONS *****
# Buttons
pos1 = (WIDTH // 2, 100 + HEIGHT // 8)
PLAY_BTN = Button(BUTTON_BCKGRND, pos1, 'PLAY')
pos3 = (WIDTH // 2, 150 + HEIGHT // 8)
RANKING_BTN = Button(BUTTON_BCKGRND, pos3, 'Ranking')
pos4 = (WIDTH // 2, 200 + HEIGHT // 8)
CHANGE_NAME_BTN = Button(BUTTON_BCKGRND, pos4, 'Player rename')
pos5 = (WIDTH // 2, 250 + HEIGHT // 8)
SET_LVL_BTN = Button(BUTTON_BCKGRND, pos5, 'SET LEVEL')
pos6 = (WIDTH // 2, 300 + HEIGHT // 8)
QUIT_BTN = Button(BUTTON_BCKGRND, pos6, 'QUIT')
pos7 = (WIDTH // 2, 350 + HEIGHT // 8)
pos8 = (WIDTH // 2, 400 + HEIGHT // 8)
BACK_BTN = Button(BUTTON_BCKGRND, pos7, 'BACK')
SAVE_BTN = Button(BUTTON_BCKGRND, pos7, 'SAVE')
PLAY_AGAIN_BTN = Button(BUTTON_BCKGRND, pos8, 'PLAY again')
EASY_BTN = Button(BUTTON_BCKGRND, pos1, 'Easy')
NORMAL_BTN = Button(BUTTON_BCKGRND, pos3, 'Normal')
HARD_BTN = Button(BUTTON_BCKGRND, pos4, 'Hard')
# Screens
START_SCREEN = Screen(BACKGROUND, 'Welcome in our FROGGER game!')
GAME_SCREEN = Screen(BACKGROUND)
END_SCREEN = Screen(BACKGROUND, 'Game Over')
RANKING_SCREEN = Screen(BACKGROUND, 'HALL OF FAME:')
SET_LEVEL_SCREEN = Screen(BACKGROUND, 'Set level of game difficulty')
RENAME_SCREEN = Screen(BACKGROUND, 'Rename player')

# import car file list

cars_left_images_list = os.listdir('./images/cars_left/')
cars_right_images_list = os.listdir('./images/cars_right/')

if '.DS_Store' in cars_left_images_list:  # in case You have Mac
    cars_left_images_list.remove('.DS_Store')
if '.DS_Store' in cars_right_images_list:
    cars_right_images_list.remove('.DS_Store')

# initialisation of the Frog
frog = Frog('frog', pos=[X_START, Y_START])


# ***** Additional functions *****
def randomize_car(x, y, speed, direction):
    global cars_image_mu_folder
    global cars_left_images_list
    global cars_right_images_list

    if direction == 'left':
        car = Car(
            './cars_' + direction + '/' + cars_left_images_list[randint(1, len(cars_left_images_list) - 1)],
            pos=[x, y])
    else:
        car = Car(
            './cars_' + direction + '/' + cars_right_images_list[randint(1, len(cars_right_images_list) - 1)],
            pos=[x, y])
    car.speed = speed
    return car


def randomize_space_x():
    global DIFFICULTY_LEVEL_DICT
    global difficulty_level

    return randint(1, DIFFICULTY_LEVEL_DICT[difficulty_level]['car_space'])


# creating list of cars going left
def traffic_lane_left(y, speed):
    global UNSEEN

    x = - UNSEEN
    traffic_lane = []
    while x <= WIDTH + UNSEEN:
        car = randomize_car(x, y, speed, direction='left')
        traffic_lane.append(car)
        x += car.width
        x += randomize_space_x()
    return traffic_lane


def traffic_lane_right(y, speed):
    global UNSEEN

    x = WIDTH + UNSEEN
    traffic_lane = []
    while x >= 0 - UNSEEN:
        car = randomize_car(x, y, speed, direction='right')
        traffic_lane.append(car)
        x -= car.width
        x -= randomize_space_x()
    return traffic_lane


# initialisation of traffic lanes; inner traffic lanes are faster
# it will be list of lists
traffic_lanes_right = []
traffic_lanes_left = []
traffic_lanes_right.append(traffic_lane_right(175, 3))
traffic_lanes_right.append(traffic_lane_right(225, 4))
traffic_lanes_right.append(traffic_lane_right(275, 5))
traffic_lanes_right.append(traffic_lane_right(325, 6))
traffic_lanes_right.append(traffic_lane_right(375, 7))
traffic_lanes_right.append(traffic_lane_right(425, 8))
traffic_lanes_left.append(traffic_lane_left(475, 8))
traffic_lanes_left.append(traffic_lane_left(525, 7))
traffic_lanes_left.append(traffic_lane_left(575, 6))
traffic_lanes_left.append(traffic_lane_left(625, 5))
traffic_lanes_left.append(traffic_lane_left(675, 4))
traffic_lanes_left.append(traffic_lane_left(725, 3))
# ***** END OF CREATING ACTORS AND OBJECTS INITIALISATIONS *****

# ***** PLAYING MUSIC FUNCTIONS *****
def play_start_end_game_music():
    music.stop()
    music.play('start_end')
    music.set_volume(SOUND_VOLUME)


play_start_end_game_music()  # music start and end screens


def play_running_game_music():  # change of the music when go to play screen
    music.stop()
    music.play('play_music')
    music.set_volume(SOUND_VOLUME)
# ***** END OF PLAYING MUSIC FUNCTIONS *****

# ***** HUD, RANKING, SUMMARY, RENAME PLAYER FUNCTIONS *****
# get ranking
def get_rank():
    data = shelve.open('hof_frogger.db')
    rank = data.get('rank')
    data.close()
    return rank

# add result to Hall of Fame
def add_rank(frog):
    data = shelve.open('hof_frogger.db')

    rank = data.get('rank')
    if not rank:
        rank = []
    rank.append(
        {
            'player_name': frog.name,
            'player_score': round(frog.score),
            'difficulty': difficulty_level
        }
    )
    rank = sorted(rank, key=lambda i: i['player_score'], reverse=True)

    if len(rank) > 10:
        rank.pop()

    data['rank'] = rank
    data.close()

# show input box for change player name
def input_box():
    global name_input_active
    global frog
    global PLAYER_NAME_INPUT_BOX

    screen.draw.text(
        f"Enter new name", midtop=(WIDTH // 2, HEIGHT // 5),
        fontsize=72, color=(50, 242, 50)
    )

    if name_input_active:
        screen.draw.rect(PLAYER_NAME_INPUT_BOX, (50, 242, 50))
    else:
        screen.draw.rect(PLAYER_NAME_INPUT_BOX, (150, 142, 150))

    screen.draw.text(
        f"{frog.name}", midtop=(PLAYER_NAME_INPUT_BOX.midtop[0], PLAYER_NAME_INPUT_BOX.midtop[1] + 7),
        fontsize=48
    )


def show_selected_difficulty_level():  # showing which difficulty level is chosen
    screen.draw.text(
        f"Actual difficulty level: {difficulty_level}", midtop=(WIDTH // 2, 500),
        fontsize=42, color=COLOR_TXT_BUTTON
    )


def show_score():  # wyswietla podsumowanie wyniku po zakonczonej rozgrywce
    global score_summary
    global COLOR_TXT_BUTTON
    screen.draw.text(
        f'Player:{score_summary[0]}\nFinal Score:{score_summary[1]}\nTime left:{round(score_summary[2])}\nLevel:{score_summary[3]}',
        topleft=(WIDTH // 6, 100),
        fontsize=32,
        color=COLOR_TXT_BUTTON
    )


# Show Hud - how many lives left and time left
def update_hud():
    global frog
    global game_time

    screen.draw.text(
        f"Game time: {round(game_time)} s", topright=(WIDTH - 10, 10),
        fontsize=42, color=(50, 242, 50)
    )
    screen.draw.text(
        f" Score: {round(frog.score)}", topleft=(20, 10),
        fontsize=56, color=(50, 242, 50)
    )

    w = 10
    for i in range(frog.lives):
        w += 50
        heart = Actor('heart', (w, 70))
        heart.draw()
# ***** END OF HUD, RANKING, SUMMARY, RENAME PLAYER FUNCTIONS *****

# ***** EVENT HANDLING *****
# Event: Key pressed
# Here we take control of pressing ESC kay and input new player name
def on_key_down(key, unicode):
    global game_stage
    global frog

    if key == keys.ESCAPE:
        quit(0)

    if game_stage == 'rename':
        if name_input_active:
            if key == keys.BACKSPACE:  # this key deletes last letter
                frog.name = frog.name[:-1]
            else:
                frog.name += unicode


# Event: mouse button pressed
def on_mouse_down(pos, button):
    global game_stage
    global PLAYER_NAME_INPUT_BOX
    global name_input_active
    global PLAY_AGAIN_BTN
    global PLAY_BTN
    global RANKING_BTN
    global SAVE_BTN
    global BACK_BTN
    global CHANGE_NAME_BTN
    global SET_LVL_BTN
    global EASY_BTN
    global NORMAL_BTN
    global HARD_BTN
    global difficulty_level

    if (game_stage == 'start_game') | (game_stage == 'summary'):
        if PLAY_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed PLAY button
            game_stage = 'playing'
            play_running_game_music()
        if RANKING_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed RANKING button
            game_stage = 'ranking'
        if CHANGE_NAME_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed RENAME button
            game_stage = 'rename'
        if RANKING_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed RANKING button
            game_stage = 'ranking'
        if SET_LVL_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed SET LEVEL button
            game_stage = 'set_level'
        if QUIT_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed QUIT button
            game_stage = 'end_game'
        if BACK_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed BACK button
            game_stage = 'start_game'
        if PLAY_AGAIN_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed PLAY AGAIN button
            game_stage = 'playing'
            play_running_game_music()
    if (game_stage == 'ranking'):
        if BACK_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed BACK button
            game_stage = 'start_game'
    if (game_stage == 'rename'):
        if PLAYER_NAME_INPUT_BOX.collidepoint(pos) & (button == mouse.LEFT):
            name_input_active = True
        else:
            name_input_active = False
        if SAVE_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed SAVE button
            game_stage = 'start_game'
    if game_stage == 'set_level':
        if EASY_BTN.collidepoint(pos) & (button == mouse.LEFT):
            difficulty_level = 'Easy'
        if NORMAL_BTN.collidepoint(pos) & (button == mouse.LEFT):
            difficulty_level = 'Normal'
        if HARD_BTN.collidepoint(pos) & (button == mouse.LEFT):
            difficulty_level = 'Hard'
        if BACK_BTN.collidepoint(pos) & (button == mouse.LEFT):  # if pressed BACK button
            game_stage = 'start_game'
# ***** END OF EVENT HANDLING *****

# ***** SPECIAL PYGAME ZERO FUNCTION UPDATE ***** we updating game objects:
def update(
        delta_time, SUCCEDED_Y=None):  # delta_time visible only in this function - measures time of previous execution of this function
    global game_stage
    global player_score
    global game_time
    global DIFFICULTY_LEVEL_DICT
    global frog
    global traffic_lanes_left
    global traffic_lenes_right
    global score_summary
    global difficulty_level
    SUCCEDED_Y = 140

    if game_stage == 'playing':
        if (keyboard.right) & (frog.x < WIDTH - 10):
            if frog.cool_time == 0:
                frog.x += frog.speed
                frog.cool_time = KEYS_SENSITIVITY
        if (keyboard.left) & (frog.x > 10):
            if frog.cool_time == 0:
                frog.x -= frog.speed
                frog.cool_time = KEYS_SENSITIVITY
        if (keyboard.down) & (frog.y <= HEIGHT - 40):
            if frog.cool_time == 0:
                frog.y += frog.speed
                frog.cool_time = KEYS_SENSITIVITY
        if (keyboard.up) & (frog.y > 15):
            if frog.cool_time == 0:
                frog.y -= frog.speed
                frog.cool_time = KEYS_SENSITIVITY

        # change position of every car
        for traffic_lane in traffic_lanes_left:
            for car in traffic_lane:
                car.x -= car.speed
                if car.x <= -UNSEEN:
                    car.x = WIDTH + UNSEEN
        for traffic_lane in traffic_lanes_right:
            for car in traffic_lane:
                car.x += car.speed
                if car.x >= WIDTH + UNSEEN:
                    car.x = -UNSEEN

        # frog update by her method
        frog.update()

        # ***** Collisions *****
        # collisions of the frog with cars
        for traffic_lane in traffic_lanes_left:
            for car in traffic_lane:
                car.update()
                if car.rect.colliderect(frog.rect):  # is collision?
                    frog.lives -= 1  # frog lost 1 live
                    frog.pos = [X_START, Y_START]
                    sounds.torpedo_explosion.play()  # explosion sound
        for traffic_lane in traffic_lanes_right:
            for car in traffic_lane:
                car.update()
            if car.rect.colliderect(frog.rect):  # is collision?
                frog.lives -= 1  # frog lost one live
                frog.pos = [X_START, Y_START]
                sounds.torpedo_explosion.play()  # explosion sound
        # ***** end of collisions *****
        if frog.y < SUCCEDED_Y:  # if frog position y is less then 140 then she succeeded
            frog.score += round(game_time)
            frog.pos = [X_START, Y_START]
            game_time = GAME_TIME
        if (game_time == 0):  # end of time, very sorry
            frog.lives -= 1
            frog.pos = [X_START, Y_START]
            game_time = GAME_TIME
        if (frog.lives <= 0):  # if end of lives
            # end game
            game_stage = 'summary'
            play_start_end_game_music()  # change music
            # save player score
            # all left time is added to the score
            frog.score += round(game_time)
            add_rank(frog)
            score_summary = [frog.name, frog.score, game_time, difficulty_level]
            # reset variables to create new game
            frog.lives = DIFFICULTY_LEVEL_DICT[difficulty_level]['lives']
            frog.pos = [X_START, Y_START]
            game_time = GAME_TIME
            frog.score = 0
        # keys sensitivity
        if frog.cool_time > 0:
            frog.cool_time -= 1
        # update clock on the screen
        game_time -= delta_time
# ***** END OF UPDATE *****

# ***** SPECIAL PYGAME ZERO FUNCTION DRAW ***** here we draw everything
def draw():
    global game_stage
    global frog
    global GAME_SCREEN
    global END_SCREEN
    global START_SCREEN
    global traffic_lanes_left
    global traffic_lenes_right

    if game_stage == 'start_game':
        START_SCREEN.show()
        START_SCREEN.show_button_play()
        START_SCREEN.show_button_ranking()
        START_SCREEN.show_button_set_level()
        START_SCREEN.show_button_change_name()
        START_SCREEN.show_button_quit()
    if game_stage == 'playing':
        GAME_SCREEN.show()
        screen.clear()

        # create background; 4x4 tiles
        for variable_y in range(0, 4):
            for variable_x in range(0, 4):
                road_tile = Actor(ROAD_TILE, [variable_x * 205, variable_y * 150 + 140], ANCHOR)
                road_tile.draw()
        frog.draw()
        for traffic_lane in traffic_lanes_left:
            for car in traffic_lane:
                car.draw()
        for traffic_lane in traffic_lanes_right:
            for car in traffic_lane:
                car.draw()

        update_hud()  # updating lives and time on hud
    if game_stage == 'summary':
        END_SCREEN.show()
        show_score()
        END_SCREEN.show_button_play_again()
        END_SCREEN.show_button_quit()
        END_SCREEN.show_button_back()
    if game_stage == 'ranking':
        RANKING_SCREEN.show()
        ranking = get_rank()
        if ranking != None:
            start_height = HEIGHT // 6 + 40
            start_width = WIDTH - round(WIDTH * 0.35)
            rect = Rect((start_width, start_height), (300, 40 + 40 * 10))  # rectangle for ranking
            screen.draw.filled_rect(rect, COLOR_RANKING_TABLE)

            for idx, record in enumerate(ranking):
                start_height += 40
                screen.draw.text(
                    f"{idx + 1}. {record.get('player_name')} : {record.get('player_score')} : {record.get('difficulty', 332)}",
                    midleft=(start_width + 5, start_height - 20),
                    fontsize=32, color=(50, 242, 50)
                )
        RANKING_SCREEN.show_button_back()
    if game_stage == 'rename':
        RENAME_SCREEN.show()
        input_box()
        RENAME_SCREEN.show_button_save()
    if game_stage == 'set_level':
        SET_LEVEL_SCREEN.show()
        show_selected_difficulty_level()
        SET_LEVEL_SCREEN.show_button_easy()
        SET_LEVEL_SCREEN.show_button_normal()
        SET_LEVEL_SCREEN.show_button_hard()
        SET_LEVEL_SCREEN.show_button_back()
    if game_stage == 'end_game':
        sys.exit(0)
# ***** END OF DRAW *****

pgzrun.go()  # This line is not needed in MU Editor, but if you use other IDE do not change it.
