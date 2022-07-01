import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()  # Loads the environment variables from the .env file

app = Flask(__name__)  # Initializes a Flask app

os.getenv("API_KEY")  # Obtains the value of the .env variable containing the Google Maps API key


# configure database
if os.getenv("TESTING") == 'true':
    print("Running in testing mode")
    db = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    print("Running in development mode")
    db = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=3306
        )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

db.connect()
db.create_tables([TimelinePost])

# Route for the landing page
@app.route('/')
def index():
    """
    Serves the landing page.
    """
    return render_template('index.html', title="Juan Escalada", url=os.getenv("URL"))

# Route for the profile page
@app.route('/profile/<name>')
def profile(name):
    """
    Loads profile dynamically from the JSON file and serves profile page.
    
    If profile could not be found, redirects to the landing page.
    """
    data = load_profiles_from_json('data.json')
    if name in data:
        info = data[name]
        return render_template('profile.html', name=name, info=info, url=os.getenv("URL"), API_KEY=os.getenv("API_KEY"))
    else:
        return index()


@app.route('/timeline')
def timeline():
    posts = [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
    return render_template('timeline.html', title='Timeline', posts=posts)


@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    # get valid name or abort
    try:
        name = request.form['name']
        if len(name) == 0:
            return "Invalid name. Name cannot be empty", 400
    except:
        return "Invalid request. Request missing the field 'name'", 400
    # get valid email or abort
    try:
        email = request.form['email']
        if len(email) == 0:
            return "Invalid email. Email cannot be empty", 400
    except:
        return "Invalid request. Request missing the field 'email'", 400
    # get valid content ot abort
    try:
        content = request.form['content']
        if len(content) == 0:
            return "Invalid content. Content cannot be empty", 400
    except:
        return "Invalid request. Request missing the field 'content'", 400
    
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }

# Route for handling 404 errors
@app.errorhandler(404)
def not_found(e):
    """
    Redirects any invalid URL to the landing page.
    """
    return render_template("index.html")


def load_profiles_from_json(filename) -> dict:
    """
    Loads profile data by parsing the JSON file provided.

    :param: The JSON file to parse
    :return: A dict containing all the JSON info parsed
    """
    # Get the relative path for the JSON data
    path = f'{os.getcwd()}/{filename}'
    # Open the file and return its parsed contents
    # UTF-8 encoding is used to parse apostrophes correctly
    with open(path, "r", encoding='utf8') as file:
        return json.load(file)
