# --- Utility functions for the tests ---

from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session


def get_page_200(testcase, pagename, kwargs=None):
    "Get a page and check the response is OK"
    response = testcase.client.get(reverse(pagename, kwargs=kwargs))
    # the page exists and is returned
    testcase.assertEqual(response.status_code, 200)
    return response


def get_page_redirects(testcase, pagename, targetname, kwargs=None):
    "Get a page and check it redirects to the given expected page"
    response = testcase.client.get(reverse(pagename, kwargs=kwargs))
    testcase.assertRedirects(response, reverse(targetname))
    return response

