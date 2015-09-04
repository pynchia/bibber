from django.conf import settings
# --- the session keys and API JSON keys

# the number of players in the game
KEY_NUM_PLAYERS = 'num_players'
# the current turn
KEY_CUR_PLAYER = 'cur_player'
# the clock
KEY_CLOCK = 'clock'
# the die
KEY_DIE = 'die'
# the game status
KEY_GAME_IS_ON = 'game_is_on'
# is the game is won
KEY_WIN = 'game_won'
# players
KEY_PLAYERS = 'players'
# the possible destinations for the move
KEY_POSSIB_DEST = 'possib_dest'
# the sound to be played
KEY_SOUND = 'sound'

# the dest POST parameter
KEY_DEST = 'dest'

# --- the board
KEY_BOARD = 'board'

# number of rows
NUM_ROWS = 4
# how many cards for each row on the board
CARDS_PER_ROW = 6
# the number of cards on the board
NUM_CARDS = NUM_ROWS * CARDS_PER_ROW
# the number of cards with ghosts
NUM_GHOST_CARDS = NUM_CARDS - 6

# the types of cards on the board
CARD_GHOST_TYPES = ['ghost1', 'ghost2', 'ghost3']
NUM_GHOST_TYPES = len(CARD_GHOST_TYPES)
# the key to the prison
CARD_PRISON_KEY = 'key'
# the prison cell
CARD_PRISON_CELL = 'cell'
# the starting point
CARD_ENTRANCE = 'entrance'

DISALLOWED_DESTINATIONS = (0, 5, 18, 23)

# the values of the die
DIE_VALUES = (0, 1, 1, 2, 2, 3, 3)

SOUND_MAX_GHOSTS = 24
SOUND_PATH = settings.STATIC_URL+'sound/'

SOUND_CLOCK = SOUND_PATH+'bell.mp3'
SOUND_CLOCK12 = SOUND_PATH+'bell12.mp3'
SOUND_PRISON_KEY = SOUND_PATH+'prison_key.mp3'
SOUND_PRISON_FREE = SOUND_PATH+'prison_free.mp3'
SOUND_CAPTURED = SOUND_PATH+'captured.mp3'
SOUND_WIN = SOUND_PATH+'win.mp3'
SOUND_GAME_OVER = SOUND_PATH+'gameover.mp3'

#--- Error messages

