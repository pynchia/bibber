from django.test import TestCase
from django.core.urlresolvers import reverse
from collections import Counter

from bibber.prj_constants import *
import utilities as ut


class MyTestCase(TestCase):
    # def setUpTestData(cls):
    #     pass
    #
    # fixtures = ['auth.json', 'app.json', ]
    #
    # def setUpClass(cls):
    #     super(MyTestCase, cls).setUpClass()     # Call parent
    #     pass
    #
    # def tearDownClass(cls):
    #     super(MyTestCase, cls).setUpClass()     # Call parent
    #     pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_homepage_game_off(self):
        """the game is off, the home page must redirect to the setup page
        """
        ut.get_page_redirects(self, 'home', 'play:setupgame')

    def test_homepage_game_started(self):
        """the game has just started, the home page must redirect to the
        play page
        """
        # let's set the session by posting to the setup page
        self.client.post(reverse('play:setupgame'), {'num_players': 2})
        # now the homepage must redirect to the play page
        return ut.get_page_redirects(self, 'home', 'play:playgame')

    def test_board_is_filled_correctly(self):
        self.test_homepage_game_started()
        board = self.client.session[KEY_BOARD]
        # for card in board:
        #     print card
        card_faces = [g.face for g in board]
        faces_count = Counter(card_faces)
        self.assertEqual(faces_count[CARD_ENTRANCE], 1)
        self.assertEqual(faces_count[CARD_PRISON_KEY], 2)
        self.assertEqual(faces_count[CARD_PRISON_CELL], 3)
        for ghost_type in CARD_GHOST_TYPES:
            self.assertEqual(faces_count[ghost_type], 6)

