"""Tests for User Authentication"""
import unittest
import json
import ast

from werkzeug.wrappers.response import Response
from library.main import app, db
from library.models import PostModel
from config import app_config


class TestAuth(unittest.TestCase):
    """"Testcase for blueprint for authentication
    "" Will create a user in the db and drop it after test execution
    """

    def setUp(self):
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.client = self.app.test_client
        self.user_details = json.dumps({'password': 'testing_p@ssword',
                             'username': 'new_user'
                            })

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.close()
            db.drop_all()

    def getLoginToken(self):
        """"Method to get a login token
        """
        user_register = self.client().post('/signup', data=self.user_details, content_type="application/json")
        self.assertEqual(user_register.status_code, 201)
        user_login = self.client().post('/login', data=self.user_details, content_type="application/json")
        self.assertEqual(user_login.status_code, 201)
        token = ast.literal_eval(user_login.data.decode())
        return token['token']

    def test_register_user(self):
        """"Method to test a successful registration
        """
        user_register = self.client().post('/signup', data=self.user_details, content_type="application/json")
        
        result = json.loads(user_register.data)
        
        self.assertEqual(result['message'], "registered successfully")
        self.assertEqual(user_register.status_code, 201)

    def test_user_login(self):
        """"Method to test successful user login
        """
        user_register = self.client().post('/signup', data=self.user_details, content_type="application/json")
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post('/login', data=self.user_details, content_type="application/json")

        self.assertEqual(user_login.status_code, 201)


    def test_user_logged_in_user_can_get_posts(self):
        """"Method to test fetching posts with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        fetch_posts = self.client().get('/blog/posts', data=self.user_details, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 200)
        self.assertEqual(ast.literal_eval(response), {"posts":[]})


    def test_user_without_valid_token_cannot_get_posts(self):
        """Method to check errors with invalid login
        """
        headers = {
            'content-type': "application/json",
            'x-access-token': 'invalid-token'
        }
        fetch_posts = self.client().get('/blog/posts', data=self.user_details, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 401)
        self.assertEqual(ast.literal_eval(response)['message'], 'Invalid token!')

    def test_user_logged_in_can_add_posts(self):
        """Method to check adding posts with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        test_post = json.dumps({'title': 'test title', 'content': 'test content'})
        fetch_posts = self.client().post('/blog/create-post', data=test_post, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 200)
        self.assertEqual(ast.literal_eval(response), {"message":"new post created"})

    def test_user_without_valid_token_cannot_add_posts(self):
        """Method to check adding posts with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': 'invalid-token'
        }
        test_post = json.dumps({'title': 'test title', 'content': 'test content'})
        fetch_posts = self.client().post('/blog/create-post', data=test_post, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 401)
        self.assertEqual(ast.literal_eval(response)['message'], 'Invalid token!')

    def test_user_logged_in_cannot_add_posts_with_0_length(self):
        """Method to check adding posts with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        test_post_1 = json.dumps({'title': '', 'content': 'test content'})
        test_post_2 = json.dumps({'title': 'test title', 'content': ''})
        fetch_posts = self.client().post('/blog/create-post', data=test_post_1, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 422)
        self.assertEqual(ast.literal_eval(response), {"message": "post title length cannot be < 1"})
        fetch_posts = self.client().post('/blog/create-post', data=test_post_2, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 422)
        self.assertEqual(ast.literal_eval(response), {"message": "post content length cannot be < 1"})

    def test_user_logged_in_cannot_add_posts_exceeding_length_limit(self):
        """Method to check adding posts with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        title = ['a' for _ in range(201)]
        content = ['a' for _ in range(5001)]
        test_post_1 = json.dumps({'title': ''.join(title), 'content': 'test content'})
        test_post_2 = json.dumps({'title': 'test title', 'content': ''.join(content)})
        fetch_posts = self.client().post('/blog/create-post', data=test_post_1, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 413)
        self.assertEqual(ast.literal_eval(response), {"message": "post title length cannot exceed 200 character limit"})
        fetch_posts = self.client().post('/blog/create-post', data=test_post_2, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 413)
        self.assertEqual(ast.literal_eval(response), {"message": "post content length cannot exceed 5000 character limit"})

    def test_user_logged_in_user_can_get_specific_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        
        test_post = json.dumps({'title': 'test title', 'content': 'test content'})
        fetch_posts = self.client().post('/blog/create-post', data=test_post, content_type="application/json", headers=headers)
        post_id = 1
        fetch_posts = self.client().get(f'/blog/post/{post_id}', data=self.user_details, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 200)
        self.assertEqual(ast.literal_eval(response), {'content': 'test content', 'id': 1, 'owner': 'new_user', 'title': 'test title'})

    def test_user_logged_in_user_can_edit_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }

        test_post = json.dumps({'title': 'test title', 'content': 'test content'})
        fetch_posts = self.client().post('/blog/create-post', data=test_post, content_type="application/json", headers=headers)
        test_data = json.dumps({'post_id': 1,"title": "test update title","content": "test update content"})
        fetch_posts = self.client().post(f'/blog/edit-post', data=test_data, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 200)
        self.assertEqual(ast.literal_eval(response), {"message": "post updated"})

    def test_user_logged_in_user_cannot_edit_nonexistent_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        title = 'test title'
        content = 'test content'
        user_id = 'new_user'

        post = PostModel(title=title, content=content,user_id=user_id)
        with self.app.app_context():
            db.session.add(post)
            db.session.commit()
        test_data = json.dumps({'post_id': 2,"title": "test update title","content": "test update content"})
        fetch_posts = self.client().post(f'/blog/edit-post', data=test_data, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 404)
        self.assertEqual(ast.literal_eval(response), {'message': 'post does not exist'})

    def test_user_logged_in_user_cannot_edit_another_users_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }
        title = 'test title'
        content = 'test content'
        user_id = 'different_user'

        post = PostModel(title=title, content=content,user_id=user_id)
        with self.app.app_context():
            db.session.add(post)
            db.session.commit()
        test_data = json.dumps({'post_id': 1,"title": "test update title","content": "test update content"})
        fetch_posts = self.client().post(f'/blog/edit-post', data=test_data, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 403)
        self.assertEqual(ast.literal_eval(response), {'message': 'post does not belong to user'})

    def test_user_logged_in_user_can_delete_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }

        test_post = json.dumps({'title': 'test title', 'content': 'test content'})
        fetch_posts = self.client().post('/blog/create-post', data=test_post, content_type="application/json", headers=headers)

        post_id = 1
        fetch_posts = self.client().delete(f'/blog/delete-post/{post_id}', data=self.user_details, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 200)
        self.assertEqual(ast.literal_eval(response), {"message": "post deleted"})
        
    def test_user_logged_in_user_cannot_delete_another_users_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }

        title = 'test title'
        content = 'test content'
        user_id = 'different_user'

        post = PostModel(title=title, content=content,user_id=user_id)
        with self.app.app_context():
            db.session.add(post)
            db.session.commit()

        post_id = 1
        fetch_posts = self.client().delete(f'/blog/delete-post/{post_id}', data=self.user_details, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 403)
        self.assertEqual(ast.literal_eval(response), {'message': 'post does not belong to user'})

    def test_user_logged_in_user_cannot_delete_nonexistent_post(self):
        """"Method to test fetching specific post with logged in user
        """
        logintoken = self.getLoginToken()
        headers = {
            'content-type': "application/json",
            'x-access-token': logintoken
        }

        test_post = json.dumps({'title': 'test title', 'content': 'test content'})
        fetch_posts = self.client().post('/blog/create-post', data=test_post, content_type="application/json", headers=headers)

        post_id = 2
        fetch_posts = self.client().delete(f'/blog/delete-post/{post_id}', data=self.user_details, content_type="application/json", headers=headers)
        response = fetch_posts.data.decode()
        self.assertEqual(fetch_posts.status_code, 404)
        self.assertEqual(ast.literal_eval(response), {'message': 'post does not exist'})

if __name__ == '__main__':
    unittest.main()