import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for 
    expected errors.
    """

    def test_get_categories(self):
        response = self.client().get('/categories')

        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', json.loads(response.data))

    def test_get_questions(self):
        response = self.client().get('/questions')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reply['questions']), 10)

        self.assertIn('total_questions', reply)
        self.assertIn('categories', reply)
        self.assertIn('current_category', reply)

    def test_404_get_questions(self):
        response = self.client().get('/questions?page=900000')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(reply['success'], False)
        self.assertEqual(reply['error'], 404)
        self.assertEqual(reply['message'], 'resource not found')

    def test_delete_questions(self):
        response = self.client().get('/questions')

        questions = json.loads(response.data)
        question_id = questions['questions'][0]['id']

        response = self.client().delete('/questions/' + str(question_id))

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reply['success'], True)
        self.assertEqual(reply['deleted'], question_id)

    def test_404_delete_questions(self):
        response = self.client().delete('/questions/99999999')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(reply['success'], False)
        self.assertEqual(reply['error'], 404)
        self.assertEqual(reply['message'], 'resource not found')

    def test_post_questions(self):
        question = {
            'question': 'What is 1 + 2?',
            'answer': 3,
            'category': 1,
            'difficulty': 1
        }
        response = self.client().post('/questions', json=question)

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reply['success'], True)

    def test_422_post_questions(self):
        response = self.client().post('/questions')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(reply['success'], False)
        self.assertEqual(reply['error'], 422)
        self.assertEqual(reply['message'], 'Unprocessable')

    def test_post_search_questions(self):
        search = {
            'searchTerm': 'title'
        }
        response = self.client().post('/questions/search', json=search)

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reply['success'], True)

        self.assertIn('questions', reply)
        self.assertIn('total_questions', reply)
        self.assertIn('current_category', reply)

    def test_404_post_search_questions(self):
        response = self.client().post('/questions/search')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(reply['success'], False)
        self.assertEqual(reply['error'], 404)
        self.assertEqual(reply['message'], 'resource not found')

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIn('questions', reply)
        self.assertIn('total_questions', reply)
        self.assertIn('current_category', reply)

    def test_404_get_questions_by_category(self):
        response = self.client().get('/categories/9999999999999/questions')

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(reply['success'], False)
        self.assertEqual(reply['error'], 404)
        self.assertEqual(reply['message'], 'resource not found')

    def test_post_quiz_question(self):
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        response = self.client().post('/quizzes', json=quiz)

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIn('id', reply)
        self.assertIn('question', reply)
        self.assertIn('answer', reply)

    def test_404_post_quiz_question(self):
        response = self.client().post('/quizzes', json={})

        reply = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(reply['success'], False)
        self.assertEqual(reply['error'], 404)
        self.assertEqual(reply['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
