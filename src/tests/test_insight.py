import os
import unittest
from main import create_app, db


class TestInsight(unittest.TestCase):    


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







    def test_insight_post(self):

        user1_insight = {
            "date": "2020-08-10",
            "insight_type": "Mental",
            "health_type": "Mental",
            "description": "Sleeping less",
            "graph_type": "Scatter plot",
            "value": "3",
            "unit": "hours",
            "degree_good_bad": "Very bad"
        }

        response = self.client.post("/insight/", json=user1_insight, headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 200,
                         "post insight")


    def test_insight_get(self):

        user2_insight = {
            "date": "2019-08-10",
            "insight_type": "Physical",
            "health_type": "Physical",
            "description": "Weight gain",
            "graph_type": "Scatter plot",
            "value": "3",
            "unit": "hours",
            "degree_good_bad": "Bad"
        }

        response1 = self.client.post("/insight/", json=user2_insight, headers=self.user2_auth_header)

        response2 = self.client.get(f"/insight/user/{self.user2_id}")

        self.assertEqual(response2.status_code, 200,
                         "valid insight returns 200")



        response3 = self.client.get("insight/user/2635242", json={}, headers=self.user2_auth_header)

        self.assertEqual(response3.status_code, 401,
                         "invalid user returns 401")


    def test_insight_update(self):

        user3_insight = {
            "date": "2017-08-10",
            "insight_type": "Mental",
            "health_type": "Mental",
            "description": "Depression",
            "graph_type": "Bar Chart",
            "value": "3",
            "unit": "weeks",
            "degree_good_bad": "Bad"
        }

        response3 = self.client.post("/insight/", json=user3_insight, headers=self.user3_auth_header)
        id = response3.get_json()["id"]

        print(id)


        user3_insight_update = {
            "description": "Mood swings",
        }

        response4 = self.client.put(f"/insight/{id}", json=user3_insight_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 200,
                         "Updated insight returns 200")

        # Try finding an insight with an id which does not exist
        
        very_large_id = 1320
        
        response4 = self.client.put(f"/insight/{very_large_id}", json=user3_insight_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no insight has id of {id}")

        
    def test_insight_delete(self):

        user4_insight = {
            "date": "2014-08-10",
            "insight_type": "Financial",
            "health_type": "Financial",
            "description": "Debt",
            "graph_type": "Pie chart",
            "value": "50",
            "unit": "dollars",
            "degree_good_bad": "Bad"
        }

        response1 = self.client.post("/insight/", json=user4_insight, headers=self.user4_auth_header)
        id = response1.get_json()["id"]


        response2 = self.client.delete(f"/insight/{id}", headers=self.user4_auth_header)

        self.assertEqual(response2.status_code, 200,
                         "Deleted insight")

        # I should not be able to delete the insight again since it should be deleted from the database.
        
        response4 = self.client.delete(f"/insight/{id}", headers=self.user4_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't delete since no insight has id of {id}")



    

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()