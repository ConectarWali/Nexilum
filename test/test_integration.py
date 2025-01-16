import unittest
from http import HTTPMethod
from integration.integration import Integration
from exception.integration_error import Integration_error

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.api = Integration(
            base_url="https://jsonplaceholder.typicode.com",
            headers={"Content-Type": "application/json"}
        )

    def test_get_posts(self):
        response = self.api.request(method=HTTPMethod.GET, endpoint="posts")
        self.assertIsInstance(response, list)  # Should return a list of posts
        self.assertGreater(len(response), 0)  # Ensure the list is not empty

    def test_get_specific_post(self):
        response = self.api.request(method=HTTPMethod.GET, endpoint="posts/1")
        self.assertIsInstance(response, dict)  # Should return a single post
        self.assertEqual(response["id"], 1)  # The ID should match the request

    def test_create_post(self):
        new_post = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        response = self.api.request(
            method=HTTPMethod.POST,
            endpoint="posts",
            data=new_post
        )
        self.assertIsInstance(response, dict)
        self.assertEqual(response["title"], "foo")
        self.assertEqual(response["body"], "bar")
        self.assertEqual(response["userId"], 1)

    def test_update_post(self):
        updated_post = {
            "id": 1,
            "title": "foo updated",
            "body": "bar updated",
            "userId": 1
        }
        response = self.api.request(
            method=HTTPMethod.PUT,
            endpoint="posts/1",
            data=updated_post
        )
        self.assertIsInstance(response, dict)
        self.assertEqual(response["title"], "foo updated")

    def test_delete_post(self):
        response = self.api.request(
            method=HTTPMethod.DELETE,
            endpoint="posts/1"
        )
        self.assertIsNone(response)  # DELETE requests typically return no content or empty response

    def test_handle_error(self):
        with self.assertRaises(Integration_error):
            self.api.request(method=HTTPMethod.GET, endpoint="invalid-endpoint")

    def tearDown(self):
        del self.api
