# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks (Completed)

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference
### Endpoints
GET '/categories'
- Acquires a dictionary of categories. The Key:value pair are integer ids and
 string values for the category name respectively.
- Request arguments: None
- Error Codes: 404
- Returns an object with key:value pairings ie:
    ```javascript
    {
     '1': "Science",
     '2': "Art",
     ...
    }
    ```
 
GET '/questions'
- Acquires a JSON object with the keys:
 - 'questions': an object with key: value pairing.
    - Keys below are in format 'data type':keys  
        - string: 'answer', 'question'
        - integer: 'category', 'id' and 'difficulty' 
 - 'total_questions' integer representing total question available
 - 'categories' list/array of objects with key:value pairings
    example:
    ```javascript
    "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    },
    ... 
    ]
    ```
 - 'current_category' None
 - Error Codes: 404
 
GET '/categories/<integer: category_id>/questions'
- Acquire questions base on category_id value
- Request argument: integer value for category_id value
- Error Codes: 404
- Returns all questions for the requested category_id in the format
    ```javascript
     {
      "current_category": 1, 
      "questions": [
        {
          "answer": "The Liver", 
          "category": 1, 
          "difficulty": 4, 
          "id": 20, 
          "question": "What is the heaviest organ in the human body?"
        }, 
        {
          "answer": "Alexander Fleming", 
          "category": 1, 
          "difficulty": 3, 
          "id": 21, 
          "question": "Who discovered penicillin?"
        }
      ], 
      "total_questions": 3
    }
    ```

POST '/questions'
- Adds a new question to the database
- Request argument: a JSON object with the format:
    ```javascript
      {
          'question': 'What is 1 + 1?',
          'answer': '2',
          'category': '1',
          'difficulty': '3'
      }   
    ```
 - Error Codes: 422
 - Returns: JSON object with the format:
    ```javascript
    {
        'success': True
    }
    ```

POST '/questions/search'
- Acquires questions based on a search term
- Request Arguments: JSON object with format:
    ```javascript
      {
          "searchTerm":"title"
      }
    ```
- Error Codes: 404
- Returns: Questions matching the search term in format:
    ```javascript
    {
      "current_category": null, 
      "questions": [
        {
          "answer": "Blood", 
          "category": 1, 
          "difficulty": 4, 
          "id": 22, 
          "question": "Hematology is a branch of medicine involving the study of what?"
        }
      ], 
      "success": true, 
      "total_questions": 1
    }
    ``` 
POST '/quizzes'
- Acquires questions to play the quiz
- Request Argument: list of previous questions ids and a category for questions
    - previous_questions: List of questions ids from answered questions
        ```javascript
          [1,2,3,4]
        ```
    - category: type and id of selected questions category in the form
    ```javascript
      {
          'type': 'Science',
          'id': '1'
      }   
    ``` 
- Error Codes: 404
- Returns JSON object of format below where id is the question id
    ```javascript
      {
          'id': '1',
          'question': 'What is 1 + 1?',
          'answer': '2'
      }   
     ```
DELETE '/questions/<integer: question_id>'
- Deletes a question based on a given question id integer
- Request Arguement: Question id via URI
- Error Codes: 404
- Returns JSON object of the format
    ```javascript
      {
          'success': True,
          'deleted': question_id
      }   
    ```

## Testing
To run the tests, run
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
