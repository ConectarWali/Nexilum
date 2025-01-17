import unittest
from nexilum.connect_to import connect_to
from http import HTTPMethod

@connect_to(
    base_url="https://jsonplaceholder.typicode.com",
    headers={"Content-Type": "application/json"}
)
class JSONPlaceholder:
    def get_posts(self, method=HTTPMethod.GET, endpoint="posts", **data):
        pass

    def get_post(self, method=HTTPMethod.GET, endpoint="posts/{post_id}", **data):
        pass

    def get_post_comments(self, method=HTTPMethod.GET, endpoint="posts/{post_id}/comments", **data):
        pass

    def create_post(self, method=HTTPMethod.POST, endpoint="posts", **data):
        pass

    def update_post(self, method=HTTPMethod.PUT, endpoint="posts/{post_id}", **data):
        pass

    def delete_post(self, method=HTTPMethod.DELETE, endpoint="posts/{post_id}", **data):
        pass

    def get_users(self, method=HTTPMethod.GET, endpoint="users", **data):
        pass

    def get_user(self, endpoint:str, method=HTTPMethod.GET, **data):
        pass

    def get_user_posts(self, method=HTTPMethod.GET, endpoint="users/{user_id}/posts", **data):
        pass

    def get_user_todos(self, method=HTTPMethod.GET, endpoint="users/{user_id}/todos", **data):
        pass

    
class TestJSONPlaceholder(unittest.TestCase):
    def setUp(self):
        self.api = JSONPlaceholder()

    def test_get_posts(self):
        response = self.api.get_posts()
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)

    def test_get_specific_post(self):
        response = self.api.get_post(endpoint="posts/1")
        self.assertIsInstance(response, dict)
        self.assertEqual(response["id"], 1)

    def test_create_post(self):
        new_post = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        response = self.api.create_post(data=new_post)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["title"], "foo")

    def test_update_post(self):
        updated_post = {
            "id": 1,
            "title": "foo updated",
            "body": "bar updated",
            "userId": 1
        }
        response = self.api.update_post(
            endpoint="posts/1",
            data=updated_post
        )
        self.assertIsInstance(response, dict)
        self.assertEqual(response["title"], "foo updated")

    def tearDown(self):
        del self.api
