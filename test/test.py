from app import app
import unittest


class FlaskTest(unittest.TestCase):
    # check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/test")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # check if return type is application/Json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/test")
        self.assertEqual(response.content_type, "application/json")

    # check for data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/test")
        self.assertTrue(b'Response' in response.data)


if __name__ == "__main__":
    unittest.main()