import os
from unittest import TestCase
import collections.abc
collections.Container = collections.abc.Container
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable
from models import db, Character


os.environ['DATABASE_URL'] = "postgresql:///comicbook_store"


from app import app

db.create_all()

app.config["WTF_CSRF_ENABLED"] = False

class UserViewTestCase(TestCase):
    """Test views for logged in users"""

    def setUp(self):
        """Create test client, add sample data."""

        Character.query.delete()
        
        self.client = app.test_client()

        # set up test comics in test db
        test_character = Character(id="7777", 
                                   name="test_character",
                                   real_name="real_test_character",
                                   deck='testdeck',
                                   first_appear_issue_id= '9999',
                                   first_appear_issue_num= '123456',
                                   first_appear_issue_name= 'test_issue',
                                   total_appearances= '78910',
                                   icon_image_url= 'test_icon_url',
                                   original_url= 'test_original_url',
                                   publisher_id= '8888',
                                   publisher_name='test_publisher'
                                  )


        db.session.add(test_character)
        db.session.commit()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_add_new_character(self):
        """Does the character model work?"""

        test_character1 = Character(id="6666", 
                           name="test_character1",
                           real_name="real_test_character1",
                           deck='testdeck1',
                           first_appear_issue_id= '999999',
                           first_appear_issue_num= '12345678',
                           first_appear_issue_name= 'test_issue1',
                           total_appearances= '789101112',
                           icon_image_url= 'test_icon_url1',
                           original_url= 'test_original_url1',
                           publisher_id= '888888',
                           publisher_name='test_publisher1'
                          )
        
        db.session.add(test_character1)
        db.session.commit()

        # is the comic added to the db?
        character = Character.query.get(6666)
        self.assertIsNotNone(character)

        test_character = Character.query.get(7777)
        self.assertNotEqual(test_character.id, character.id)

        # does the character have the correct information?
        self.assertEqual(character.id, 6666)
        self.assertEqual(character.name, 'test_character1')
        self.assertEqual(character.real_name, 'real_test_character1')
        self.assertEqual(character.deck, 'testdeck1')
        self.assertEqual(character.first_appear_issue_id, '999999')
        self.assertEqual(character.first_appear_issue_num, '12345678')
        self.assertEqual(character.first_appear_issue_name, 'test_issue1')
        self.assertEqual(character.total_appearances, '789101112')
        self.assertEqual(character.icon_image_url, 'test_icon_url1')
        self.assertEqual(character.original_url, 'test_original_url1')
        self.assertEqual(character.publisher_id, '888888')
        self.assertEqual(character.publisher_name, 'test_publisher1')