# --- Utility functions for the tests ---

from django.core.urlresolvers import reverse

def get_page_200(testobj, pagename, kwargs=None):
    "Utility function to get a page and check the response is OK"
    response = testobj.client.get(reverse(pagename, kwargs=kwargs))
    # the page exists and is returned
    testobj.assertEqual(response.status_code, 200)
    return response

