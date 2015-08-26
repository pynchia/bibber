# --- the session keys

# the number of players in the game
KEY_NUM_PLAYERS = 'numplayers'
# the current turn
KEY_CUR_PLAYER = 'curplayer'
# players
KEY_PLAYERS = 'players'
# the die
KEY_DIE = 'die'
# the clock
KEY_CLOCK = 'clock'

# --- game progress
KEY_GAME_STATUS = 'status'
STATUS_OFF  = 0
STATUS_PLAY = 1
STATUS_MOVE = 2

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

# the values of the die
DIE_VALUES = (0, 1, 1, 2, 2, 3)

