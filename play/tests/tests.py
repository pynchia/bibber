from django.test import TestCase
from django.core.urlresolvers import reverse

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

    def test_homepage_game_on(self):
        """the game is on, just started, the home page must redirect to the
        play page
        """
        # let's set the session by going to the setup page
        self.client.post(reverse('play:setupgame'), {'num_players': 2})
        ut.get_page_redirects(self, 'home', 'play:playgame')

