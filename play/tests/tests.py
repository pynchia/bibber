from django.test import TestCase
from django.core.urlresolvers import reverse

import test_utilities as ut
from play.models import Game


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

    def homepage_game_off(self):
        ut.get_page_200(self, 'play:home')

