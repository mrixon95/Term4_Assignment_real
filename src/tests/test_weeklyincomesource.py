import os
import unittest
from main import create_app, db


class TestWeeklyIncomeSource(unittest.TestCase):    


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







    def test_weeklyincomesource_post(self):

        user1_weeklyincomesource = {
            "amount": 247,
            "description": "Uber driving",
            "income_type": "Ongoing",
            "week_end": "2010-06-07",
            "week_start": "2010-06-14"
        }

        response = self.client.post("/weeklyincomesource/", json=user1_weeklyincomesource, headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 200,
                         "post weeklyincomesource")


    def test_weeklyincomesource_get(self):

        user2_weeklyincomesource= {
            "amount": 582,
            "description": "Coles shift",
            "income_type": "Ongoing",
            "week_end": "2020-08-07",
            "week_start": "2020-08-14"
        }

        response1 = self.client.post("/weeklyincomesource/", json=user2_weeklyincomesource, headers=self.user2_auth_header)

        response2 = self.client.get(f"/weeklyincomesource/user/{self.user2_id}")

        self.assertEqual(response2.status_code, 200,
                         "valid weeklyincomesource returns 200")



        response3 = self.client.get("weeklyincomesource/user/2635242", json={}, headers=self.user2_auth_header)

        self.assertEqual(response3.status_code, 401,
                         "invalid user returns 401")


    def test_weeklyincomesource_update(self):

        user3_weeklyincomesource = {
            "amount": 894,
            "description": "Software engineering job",
            "income_type": "Ongoing",
            "week_end": "2010-06-07",
            "week_start": "2010-06-14"
        }

        response3 = self.client.post("/weeklyincomesource/", json=user3_weeklyincomesource, headers=self.user3_auth_header)
        id = response3.get_json()["id"]

        print(id)


        user3_weeklyincomesource_update = {
            "income_type": "One-off",
        }

        response4 = self.client.put(f"/weeklyincomesource/{id}", json=user3_weeklyincomesource_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 200,
                         "Update work history returns 200")

        # Try finding a weekly income source with an id which does not exist
        
        very_large_id = 1320
        
        response4 = self.client.put(f"/weeklyincomesource/{very_large_id}", json=user3_weeklyincomesource_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no weeklyincomesource has id of {id}")

        
    def test_weeklyincomesource_delete(self):

        user4_weeklyincomesource = {
            "amount": 152,
            "description": "Cleaning",
            "income_type": "Ongoing",
            "week_end": "2010-06-07",
            "week_start": "2010-06-14"
        }

        response1 = self.client.post("/weeklyincomesource/", json=user4_weeklyincomesource, headers=self.user4_auth_header)
        id = response1.get_json()["id"]


        response2 = self.client.delete(f"/weeklyincomesource/{id}", headers=self.user4_auth_header)

        self.assertEqual(response2.status_code, 200,
                         "Deleted weekly income source")

        # I should not be able to delete the weekly income source again since it should be deleted from the database.
        
        response4 = self.client.delete(f"/weeklyincomesource/{id}", headers=self.user4_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't delete since no weeklyincomesource has id of {id}")



    

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()