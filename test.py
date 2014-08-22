from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue('Please login' in response.data)

    # Ensure login behaves correctly given the correct credentials
    def test_login_correct(self):
        tester = app.test_client(self)
        response = tester.post(
          '/login',
          data=dict(username='admin', password='admin'),
          follow_redirects=True
        )
        self.assertIn('You were just logged in, cool.', response.data)

    def test_login_incorrect(self):
        tester = app.test_client(self)
        response = tester.post(
          '/login',
          data=dict(username='joe', password='blow'),
          follow_redirects=True
        )
        self.assertIn('Invalid credentials, please try again.', response.data)

    # Ensure that logout works correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
          '/login',
          data=dict(username='admin', password='admin'),
          follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn('You were just logged out, bye.', response.data)

    # Ensure the main page needs a login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue('You need to login first.' in response.data)

    # Ensure the logout page requires a user to be logged in
    def test_logout_requires_login_first(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue('You need to login first.' in response.data)

    # Test that posts appear on our main page
    def test_posts_showing_up_on_main_page(self):
      tester = app.test_client(self)
      response = tester.post(
        '/login',
        data=dict(username='admin', password='admin'),
        follow_redirects=True
      )
      self.assertIn('Good', response.data)



if __name__ == '__main__':
    unittest.main()
