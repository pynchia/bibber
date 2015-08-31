# --- the session keys

# the number of players in the game
KEY_NUM_PLAYERS = 'numplayers'
# the current turn
KEY_CUR_PLAYER = 'curplayer'
# the clock
KEY_CLOCK = 'clock'
# the game status
KEY_GAME_IS_ON = 'gameison'
# players
KEY_PLAYERS = 'players'
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

# the types of ghosts on the board
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
DIE_VALUES = (0, 1, 1, 2, 2, 3)

SOUND_MAX_GHOSTS = 24
SOUND_PRISON_KEY = 'prison_key'
SOUND_PRISON_FREE = 'prison_free'
SOUND_CAPTURED = 'captured'
SOUND_WIN = 'win'
SOUND_GAME_OVER = 'gameover'
