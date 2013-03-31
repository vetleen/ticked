from django.test import TestCase
from django.contrib.auth.models import User
     
class TestTheUrls(TestCase):
    """
    Test that URLs yield expected response
    """
    def setUp(self):
        """
        CONFIGURATION FOR URLS TESTING
        """
        ## Set the conditions for URL-testing
        self.urls_to_test = ['/frontpage/', '/todos/view/', '/todos/view/1/', '/todos/add/', '/todos/tick/1/', '/todos/untick/1/', '/todos/view/ticked/', '/todos/delete/1/', '/todos/edit/1/', '/user/logout/', '/user/new/', '/user/create/', '/user/edit/', '/user/delete/']     #the test will try all these urls
        self.acceptable_url_statuses = [200, 302]    #the test will accept these statuses

        ## Create testusers
            #you may add "user": "password" to dict to increas number of testusers
            #You should disable one of the accounbts when you figure out how to test every path troughh your code
        self.test_users = {"testuser@testuser.com": "testuserpassword", "another@username.no": "passsssssssssss10202"}        
            #creates the users
        for username, password in self.test_users.iteritems():
            new_user = User.objects.create_user(username=username, password=password)
            #tests that users exist
        for counter in range(len(self.test_users)):
            user_id=counter+1
            user_to_test = User.objects.get(id=user_id)
            error_message = "User with username %s, is not an instance of the User class" % (user_to_test.username)
            self.assertIsInstance(user_to_test, User, error_message)
    def test_url_status(self):
        """
        TEST URL STATUS
        """
        #test views that don't have their own tests
        for url in self.urls_to_test:
            response = self.client.get(url, follow=True)
            error_message = "Unexpected status %s from URL: %s" % (response.status_code, url)
            self.assertIn(response.status_code, self.acceptable_url_statuses, error_message)

        #test URLS for loginview. NOTE: This only tests the status code of the view - not anything else
        self.test_users.update({"notauser@test.com": "sksjskskks"}) #add a user that doesn't exist
        for username, password in self.test_users.iteritems():
            url_to_test = '/user/login/'
            response = self.client.post(url_to_test, {'username': username, 'password': password}, follow=True)
            error_message = "Unexpected status %s from URL: %s" % (response.status_code, url_to_test)
            self.assertIn(response.status_code, self.acceptable_url_statuses)



















