from django.test import TestCase, Client
from django.urls import reverse
from . import util

# Create your tests here.


class EncyclopediaTestCase(TestCase):

    def SetUp(self):

        pass

    def test_new_page(self):
        #create a test client
        client = Client()

        # Make a POST request to create a new page with valid data
        response = client.post(reverse('new_page'), {'title': 'Test Page', 'content': 'Test Content'})

        # Check if the page was successfully created and user was redirected
        self.assertEqual(response.status_code, 200)  # 302 is the status code for redirection

        # Check if the new entry was saved
        self.assertTrue(util.get_entry('Test Page'))

        # Make a POST request with empty title to trigger error
        response = client.post(reverse('new_page'), {'title': '', 'content': 'Test Content'})
        self.assertEqual(response.status_code, 200)  # Check for 200 Bad Request

        # Make a POST request with empty content to trigger error
        response = client.post(reverse('new_page'), {'title': 'Test Page 2', 'content': ''})
        self.assertEqual(response.status_code, 200)  # Check for 400 Bad Request

        # Make a POST request with existing title to trigger error
        existing_entry = util.list_entries()[0]
        response = client.post(reverse('new_page'), {'title': existing_entry, 'content': 'Test Content'})
        self.assertEqual(response.status_code, 200)  # Check if the page is rendered again
        self.assertContains(response, 'An encyclopedia entry with this title already exists.')  # Check for error message

    

    def test_entry_view(self):
        # Create a test client
        client = Client()

        # Test accessing an existing entry page
        existing_entry = util.list_entries()[0]
        response = client.get(reverse('entry', args=[existing_entry]))
        self.assertEqual(response.status_code, 200)  # Check if the page loads successfully

        # Test accessing a non-existing entry page
        response = client.get(reverse('entry', args=['Nonexistent_Entry']))
        self.assertEqual(response.status_code, 404)  # Check if the page returns a 404 error

    def test_search_results_view(self):
        # Create a test client
        client = Client()

        # Test searching for an existing entry
        existing_entry = util.list_entries()[0]
        response = client.get(reverse('search_results') + '?q=' + existing_entry)
        self.assertEqual(response.status_code, 200)  # Check if the search results page loads successfully

        # Test searching for a non-existing entry
        response = client.get(reverse('search_results') + '?q=Nonexistent')
        self.assertEqual(response.status_code, 200)  # Check if the search results page loads successfully

    def test_edit_page_view(self):
        # Create a test client
        client = Client()

        # Test accessing the edit page for an existing entry
        existing_entry = util.list_entries()[0]
        response = client.get(reverse('edit_page', args=[existing_entry]))
        self.assertEqual(response.status_code, 200)  # Check if the edit page loads successfully

        # Test accessing the edit page for a non-existing entry
        response = client.get(reverse('edit_page', args=['Nonexistent_Entry']))
        self.assertEqual(response.status_code, 404)  # Check if the page returns a 404 error

        # Test editing an entry with valid data
        response = client.post(reverse('edit_page', args=[existing_entry]), {'content': 'Updated content'})
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after saving

    def test_random_page_view(self):
        # Create a test client
        client = Client()

        # Test accessing a random page
        response = client.get(reverse('random_page'))
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected

