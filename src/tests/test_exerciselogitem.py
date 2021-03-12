import os
import unittest
from main import create_app, db


class TestExerciseLogItem(unittest.TestCase):    


    @classmethod
    def create_user(cls, name, email):

        response = cls.client.post("/user/register", json={
            "email": f"{email}",
            "first_name": f"{name}",
            "last_name": "Rixon",
            "created_at": "2020-10-06 00:00:00",
            "dob": "1995-08-06",
            "gender": "Male",
            "mobile": "0424766201",
            "city": "Melbourne",
            "country": "Australia",
            "password": "123456"
        })

        print("email was " + email)
        print("name was " + name)
        print("json response was " + str(response.json))
        if response.status_code != 200:
            raise ValueError("Error when getting test user token.")
        
        user_id = response.json["id"]
        return user_id


    @classmethod
    def auth_user(cls, email):
        """Returns a user token for the test user as well
        as a header dictionary for authorization."""

        response = cls.client.post("/user/login", json={
            "email": f"{email}",
            "password": "123456"
        })

        print(response)

        if response.status_code != 200:
            raise ValueError("Error when getting user token.")

        token = response.json["token"]
        auth_header = {
            "Authorization": f"Bearer {token}"
        }

        return token, auth_header




    
    @classmethod
    def setUp(cls) -> None:
        os.environ["FLASK_ENV"] = "testing"
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.client = cls.app.test_client()

        cls.user1_id = cls.create_user("user1", "user1@gmail.com")
        cls.user2_id = cls.create_user("user2", "user2@gmail.com")
        cls.user3_id = cls.create_user("user3", "user3@gmail.com")
        cls.user4_id = cls.create_user("user4", "user4@gmail.com")


        cls.user1_auth_header = cls.auth_user("user1@gmail.com")[1]
        cls.user2_auth_header = cls.auth_user("user2@gmail.com")[1]
        cls.user3_auth_header = cls.auth_user("user3@gmail.com")[1]
        cls.user4_auth_header = cls.auth_user("user4@gmail.com")[1]







    def test_exerciselogitem_post(self):

        user1_exerciselogitem = {
            "description": "Treadmill in the gym",
            "date": "2020-07-10",
            "time_start": "2020-07-10 09:00:00",
            "time_end": "2020-07-10 10:00:00",
            "intensity": "High"
        }

        response = self.client.post("/exerciselogitem/", json=user1_exerciselogitem, headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 200,
                         "post exerciselogitem")


    def test_exerciselogitem_get(self):

        user2_exerciselogitem = {
            "description": "Push ups in the gym",
            "date": "2020-05-10",
            "time_start": "2020-09-10 11:00:00",
            "time_end": "2020-09-10 12:00:00",
            "intensity": "Medium"
        }

        response1 = self.client.post("/exerciselogitem/", json=user2_exerciselogitem, headers=self.user2_auth_header)

        response2 = self.client.get(f"/exerciselogitem/user/{self.user2_id}")

        self.assertEqual(response2.status_code, 200,
                         "valid exerciselogitem returns 200")



        response3 = self.client.get("exerciselogitem/user/2635242", json={}, headers=self.user2_auth_header)

        self.assertEqual(response3.status_code, 401,
                         "invalid user returns 401")


    def test_exerciselogitem_update(self):

        user3_exerciselogitem = {
            "description": "Walk in the park",
            "date": "2020-12-18",
            "time_start": "2020-12-18 16:00:00",
            "time_end": "2020-12-18 17:00:00",
            "intensity": "Low"
        }

        response3 = self.client.post("/exerciselogitem/", json=user3_exerciselogitem, headers=self.user3_auth_header)
        id = response3.get_json()["id"]

        print(id)


        user3_exerciselogitem_update = {
            "description": "Mood swings",
        }

        response4 = self.client.put(f"/exerciselogitem/{id}", json=user3_exerciselogitem_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 200,
                         "Updated exerciselogitem returns 200")

        # Try finding an exerciselogitem with an id which does not exist
        
        very_large_id = 1320
        
        response4 = self.client.put(f"/exerciselogitem/{very_large_id}", json=user3_exerciselogitem_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no exerciselogitem has id of {id}")

        
    def test_exerciselogitem_delete(self):

        user4_exerciselogitem = {
            "description": "Lunges",
            "date": "2020-12-05",
            "time_start": "2020-12-05 06:00:00",
            "time_end": "2020-12-05 07:00:00",
            "intensity": "Low"
        }

        response1 = self.client.post("/exerciselogitem/", json=user4_exerciselogitem, headers=self.user4_auth_header)
        id = response1.get_json()["id"]


        response2 = self.client.delete(f"/exerciselogitem/{id}", headers=self.user4_auth_header)

        self.assertEqual(response2.status_code, 200,
                         "Deleted exerciselogitem")

        # I should not be able to delete the exerciselogitem again since it should be deleted from the database.
        
        response4 = self.client.delete(f"/exerciselogitem/{id}", headers=self.user4_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't delete since no exerciselogitem has id of {id}")



    

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()