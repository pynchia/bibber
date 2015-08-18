from django.test import TestCase
from django.core.urlresolvers import reverse

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
        ut.get_page_redirects(self, 'home', 'play:setupgame')

    def test_homepage_game_on(self):
        ut.get_page_redirects(self, 'home', 'play:playgame')

