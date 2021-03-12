import os
import unittest
from main import create_app, db


class TestWeeklyExpenseSource(unittest.TestCase):    


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







    def test_weeklyexpensesource_post(self):

        user1_weeklyexpensesource = {
            "amount": 132,
            "description": "Cleaning",
            "expense_type": "Ongoing",
            "week_end": "2014-06-07",
            "week_start": "2014-06-14"
        }

        response = self.client.post("/weeklyexpensesource/", json=user1_weeklyexpensesource, headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 200,
                         "post weeklyexpensesource")


    def test_weeklyexpensesource_get(self):

        user2_weeklyexpensesource = {
            "amount": 782,
            "description": "Petrol",
            "expense_type": "Ongoing",
            "week_end": "2020-10-07",
            "week_start": "2020-10-14"
        }

        response1 = self.client.post("/weeklyexpensesource/", json=user2_weeklyexpensesource, headers=self.user2_auth_header)

        response2 = self.client.get(f"/weeklyexpensesource/user/{self.user2_id}")

        self.assertEqual(response2.status_code, 200,
                         "valid weeklyexpensesource returns 200")



        response3 = self.client.get("weeklyexpensesource/user/2635242", json={}, headers=self.user2_auth_header)

        self.assertEqual(response3.status_code, 401,
                         "invalid user returns 401")


    def test_weeklyexpensesource_update(self):

        user3_weeklyexpensesource = {
            "amount": 364,
            "description": "Groceries",
            "expense_type": "Ongoing",
            "week_end": "2017-09-07",
            "week_start": "2017-09-14"
        }

        response3 = self.client.post("/weeklyexpensesource/", json=user3_weeklyexpensesource, headers=self.user3_auth_header)
        id = response3.get_json()["id"]

        print(id)


        user3_weeklyexpensesource_update = {
            "income_type": "One-off",
        }

        response4 = self.client.put(f"/weeklyexpensesource/{id}", json=user3_weeklyexpensesource_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 200,
                         "Update work history returns 200")

        # Try finding a weekly expense source with an id which does not exist
        
        very_large_id = 1320
        
        response4 = self.client.put(f"/weeklyexpensesource/{very_large_id}", json=user3_weeklyexpensesource_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no weeklyexpensesource has id of {id}")

        
    def test_weeklyexpensesource_delete(self):

        user4_weeklyexpensesource = {
            "amount": 450,
            "description": "Rent",
            "expense_type": "Ongoing",
            "week_end": "2016-11-11",
            "week_start": "2016-11-18"
        }

        response1 = self.client.post("/weeklyexpensesource/", json=user4_weeklyexpensesource, headers=self.user4_auth_header)
        id = response1.get_json()["id"]


        response2 = self.client.delete(f"/weeklyexpensesource/{id}", headers=self.user4_auth_header)

        self.assertEqual(response2.status_code, 200,
                         "Deleted weekly expense source")

        # I should not be able to delete the weekly expense source again since it should be deleted from the database.
        
        response4 = self.client.delete(f"/weeklyexpensesource/{id}", headers=self.user4_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't delete since no weeklyexpensesource has id of {id}")



    

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()