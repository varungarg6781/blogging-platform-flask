import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Blogging Platform', response.data)

    def test_posts_route(self):
        response = self.app.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the first blog post.', response.data)
        self.assertIn(b'This is the second blog post.', response.data)

    def test_user_login(self):
        response = self.app.post('/login', data=dict(
            email='user1@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect a redirect
        self.assertIn(b'user1@example.com', response.data)  # Expect the user's email in the response data

    # Adding some changes for PR to work
    # Adding some more changes for PR to work

    def test_user_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect a redirect
        self.assertNotIn(b'user1@example.com', response.data)  # Expect the user's email not to be in the response data


    def test_add_blog_post(self):
        with self.app:
            self.app.post('/login', data=dict(
                email='user1@example.com',
                password='password123'
            ))  # Log in the user (you can use your login test)
            response = self.app.post('/post/add', data=dict(
                title='New Post',
                content='This is a new blog post.'
            ))
            self.assertEqual(response.status_code, 302)  # Expect a redirect
            self.assertEqual(response.location, 'http://localhost/posts')  # Expect redirection to the posts page
            # Check if the new post is displayed on the posts page
            self.assertIn(b'New Post', self.app.get('/posts').data)

    
if __name__ == '__main__':
    unittest.main()
