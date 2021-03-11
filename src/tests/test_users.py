import os
import unittest
from main import create_app, db


class TestUsers(unittest.TestCase):    
    
    @classmethod
    def setUp(cls) -> None:
        os.environ["FLASK_ENV"] = "testing"
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.client = cls.app.test_client()

        cls.reg_response = cls.client.post(
            "/user/register", json= {
            "email": "mrixon95@gmail.com",
            "first_name": "Michael",
            "last_name": "Rixon",
            "created_at": "2020-10-06 00:00:00",
            "dob": "1995-08-06",
            "gender": "Male",
            "mobile": "0424766201",
            "city": "Melbourne",
            "country": "Australia",
            "password": "password"
            }
        )


    def test_user_register(self):
        self.assertEqual(self.reg_response.status_code, 200,
                         "valid register returns 200")

        status_code = self.reg_response.status_code
        self.assertEqual(status_code, 200)

        json_received = self.reg_response.get_json()

        self.assertEqual(json_received["email"], "mrixon95@gmail.com",
                         "should receive json with email mrixon95@gmail.com")

        

    def test_user_login(self): 
        response = self.client.post("/user/login", json={
            "email": "unknown@test.com",
            "password": "unknown"
        })

        self.assertEqual(response.status_code, 401,
                         "unauthorized")



        response2 = self.client.post("/user/login", json={
            "email": "mrixon95@gmail.com",
            "password": "password"
        })

        self.assertEqual(response2.status_code, 200,
                         "successfully logged in")
        
        data2 = response2.get_json()
        print("Login response json is ")
        print(data2)
        self.assertIn("token", data2)
        self.assertIsInstance(data2["token"], str)

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()