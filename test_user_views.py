import os
from unittest import TestCase

from models import db, connect_db, User, Comic, Reading_List, Character, Character_List
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///comicbook_store"


from app import app, CURR_USER_KEY

db.create_all()

app.config["WTF_CSRF_ENABLED"] = False

class UserViewTestCase(TestCase):
    """Test views for logged in users"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Comic.query.delete()
        Character.query.delete()
        
        self.client = app.test_client()

        # test users
        self.testuser = User.signup(first_name="test",
                                    last_name="user",
                                    username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    )
        self.user1 = User.signup("test1", "user1", "testuser1", "test1@test.com", "testuser1")

        

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_create(self):
        """Are users being added to the users table?"""

        # fake login
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f'/users/{self.testuser.id}/account')
            # can we hit this route with a logged-in user?
            self.assertEqual(resp.status_code, 200)
            # is the user's first name being displayed?
            self.assertIn("test", str(resp.data))
    
    def setup_comics(self):
        # test comics
        test_comic = Comic(id="8888",
                            name="testcomic",
                            issue_number="8888",
                            deck="this is a test comic")

        comic1 = Comic(id="9999",
                        name="testcomic1",
                        issue_number="9999",
                        deck="this is another test comic")

        db.session.add_all([test_comic, comic1])
        db.session.commit()

            
    def test_add_to_reading_list(self):
        """Are comics being added to the reading_list table?"""

        self.setup_comics()

        comic = Comic.query.get(8888)
        self.assertIsNotNone(comic)
        comic1 = Comic.query.get(9999)
        self.assertIsNotNone(comic1)

         # fake login
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
            # post request for comic to add to reading list
            resp = c.post('/users/reading_list/8888', follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            
            reading = Reading_List.query.filter(Reading_List.comic_id==8888).all()
            
            self.assertEqual(len(reading), 1)
            
            self.assertEqual(reading[0].user_id, self.testuser.id)
        

    def test_remove_from_reading_list(self):
        """Are comics being removed from the user's reading list?"""
        
        self.setup_comics()

         # fake login
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
            # post request to add comic to reading list
            resp = c.post('/users/reading_list/8888', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            # post request to add another comic to reading list
            resp1 = c.post('/users/reading_list/9999', follow_redirects=True)
            self.assertEqual(resp1.status_code, 200)

            # check length of reading list to be 2
            reading = Reading_List.query.all()
            self.assertEqual(len(reading), 2)

            # post request to remove the comic from reading list
            resp2 = c.post(f'/users/8888/remove_comic', follow_redirects=True)
            self.assertEqual(resp2.status_code, 200)

            # check length of reading list to be 1
            reading1 = Reading_List.query.all()
            self.assertEqual(len(reading1), 1)


    def setup_characters(self):
        # test comics
        test_character = Character(id="7777", name="testcharacter")

        character1 = Character(id="6666", name="testcharacter1")

        db.session.add_all([test_character, character1])
        db.session.commit()


    def test_add_to_character_list(self):
        """Are characters being added to the characters table?"""

        self.setup_characters()

        character = Character.query.get(7777)
        self.assertIsNotNone(character)
        character1 = Character.query.get(6666)
        self.assertIsNotNone(character1)

         # fake login
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
            # post request for comic to add to reading list
            resp = c.post('/users/characters/7777', follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            
            characters = Character_List.query.filter(Character_List.character_id==7777).all()
            
            self.assertEqual(len(characters), 1)
            
            self.assertEqual(characters[0].user_id, self.testuser.id)

    def test_show_character_list(self):
        """"""

# finish this test