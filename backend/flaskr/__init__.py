import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        return response

    # Helper function to paginate questions
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        items = [item.format() for item in selection]
        current_items = items[start:end]

        return current_items

    # An endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.all()
        categories = [category.format() for category in selection]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'categories': categories,
        }), 200

    '''
    An endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    two pages. Reference trivia.psql lines 126-145
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()

        questions = paginate_questions(request, selection)
        current_category = [question['category'] for question in questions]
        current_category = list(set(current_category))
        categories = [cat.format() for cat in Category.query.all()]

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'questions': questions,
            'total_questions': len(selection),
            'categories': categories,
            'current_category': current_category,
        }), 200

    '''
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if not question:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            }), 200

        except Exception as e:
            abort(404)

    '''
    An endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():

        try:
            data = request.json
            to_add = Question(data['question'],
                              data['answer'],
                              data['category'],
                              data['difficulty']
                              )
            to_add.insert()

            return jsonify({
                'success': True
            }), 200
        except Exception as e:
            abort(422)

    '''
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term is a substring of
    the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            search_term = request.json['searchTerm']

            selection = Question.query.filter(
                Question.question.ilike('%' + search_term + '%')).all()

            search_results = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': search_results,
                'total_questions': len(search_results),
                'current_category': None
            }), 200
        except Exception as e:
            abort(404)

    '''
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'questions': questions,
            'total_questions': len(selection),
            'current_category': category_id,
        })

    '''
    A POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():

        try:
            previous_questions = request.json['previous_questions']
            # Quiz category has 'type' and 'id' as keys
            category = request.json['quiz_category']

            if category['id'] == 0:
                questions = Question.query. \
                    filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query. \
                    filter_by(category=category['id']). \
                    filter(Question.id.notin_(previous_questions)).all()

            question_list = [(query.id, query.question, query.answer) for query
                             in questions]

            # Make sure we have questions else provide tuple of empty string
            if len(question_list) > 0:
                question = random.choice(question_list)
            else:
                question = ('', '', '')

            return jsonify({
                'id': question[0],
                'question': question[1],
                'answer': question[2]
            })
        except Exception as e:
            print(str(e))
            abort(404)

    '''
    Error handlers for all expected errors
    including 404 and 422.
    '''

    # reply with json for 404 error
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # reply with json for 500 error
    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    return app
