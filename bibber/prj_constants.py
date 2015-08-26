# the following are the names of the values stored in the session

# the number of players in the game
KEY_NUM_PLAYERS = 'numplayers'
# the current turn
KEY_CUR_PLAYER = 'curplayer'
# player 1
KEY_PLAYER1 = 'p1'
# player 2
KEY_PLAYER2 = 'p2'
# player 3
KEY_PLAYER3 = 'p3'
# the die
KEY_DIE = 'die'

# game progress
KEY_GAME_STATUS = 'status'
STATUS_OFF  = 0
STATUS_PLAY = 1
STATUS_MOVE = 2

# the board
KEY_BOARD = 'board'

# number of rows
NUM_ROWS = 4
# how many cards for each row on the board
CARDS_PER_ROW = 6
# the number of cards on the board
NUM_CARDS = NUM_ROWS * CARDS_PER_ROW
# the number of cards with ghosts
NUM_GHOST_CARDS = NUM_CARDS - 6

# ------ types of cards ------
# the types of ghosts on the board
CARD_GHOST_TYPES = ['lady', 'kid', 'man']
NUM_GHOST_TYPES = len(CARD_GHOST_TYPES)

# the key to the prison
CARD_PRISON_KEY = 'key'
# the prison cell
CARD_PRISON_CELL = 'cell'
# the starting point
CARD_ENTRANCE = 'entrance'

