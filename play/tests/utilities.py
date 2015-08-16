# --- Utility functions for the tests ---

from django.core.urlresolvers import reverse

def get_page_200(testobj, pagename, kwargs=None):
    "Get a page and check the response is OK"
    response = testobj.client.get(reverse(pagename, kwargs=kwargs))
    # the page exists and is returned
    testobj.assertEqual(response.status_code, 200)
    return response

def get_page_redirects(testobj, pagename, redirpagename, kwargs=None):
    "Get a page and check it redirects to the given expected page"
    response = testobj.client.get(reverse(pagename, kwargs=kwargs))
    testobj.assertRedirects(response, reverse(redirpagename))
    return response

