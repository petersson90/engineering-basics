# Twitter API - 2

In this challenge we will continue with **Twitter API** exercise. In this exercise, the database was _mocked_ with a made-up `TweetRepository` class.

## Setup

We're going to continue with the correction from earlier:
:point_right: [github.com/ssaunier/twitter-api](https://github.com/ssaunier/twitter-api)

```bash
cd ~/code/<user.github_nickname>
git clone git@github.com:ssaunier/twitter-api.git twitter-api-database
cd twitter-api-database
git remote rm origin
```

Go to [github.com/new](https://github.com/new) and create a _public_ repository under your _personal_ account, name it `twitter-api-database`.

```bash
git remote add origin git@github.com:<user.github_nickname>/twitter-api-database.git
git push -u origin master
```

Now that you have the repo, you need to create the virtualenv and install the packages:

```bash
pipenv install --dev
```

Make sure that the tests are passing:

```bash
nosetests
```

Make sure that the web server can be run and show the Swagger documentation:

```bash
FLASK_ENV=development pipenv run flask run
```

:point_right: Go to [localhost:5000](http://localhost:5000/). Is everything fine?

## Setting up SQLAlchemy

Like in the previous exercise, we need to install some tools:

```bash
pipenv install psycopg2-binary gunicorn
pipenv install flask-sqlalchemy flask-migrate flask-script
```

We will need to configure the used Database from an environment variable, the easiest is to use the `python-dotenv` package with a `.env` file:

```bash
touch .env
echo ".env" >> .gitignore
```

And add the `DATABASE_URL` variable:

```bash
# .env
DATABASE_URL="postgresql://postgres:<password_if_necessary>@localhost/twitter_api_flask"

# On OSX:
# DATABASE_URL="postgresql://localhost/twitter_api_flask"
```

If you got a `sqlalchemy.exc.OperationalError` verify your `DATABASE_URL`. Your password shouldn't contains `<`, `>` symbols.

```bash
# Valid example
DATABASE_URL="postgresql://postgres:root@localhost/twitter_api_flask"

# Invalid example
DATABASE_URL="postgresql://postgres:<root>@localhost/twitter_api_flask"
```

We now need to create a config object to pass to the Flask application. This will link the env variables to the actual Flask / SQLAlchemy configuration:

```bash
touch config.py
```

```python
import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
```

Now let's instantiate an `SQLAlchemy` instance, but first let's kill the fake repositories:

```bash
rm app/db.py
rm app/repositories.py
rm tests/test_repositories.py
```

Open the `app/apis/tweets.py` and the `tests/apis/test_tweet_views.py` and remove the following line in both files:

```python
from app.db import tweet_repository
```

It's official, the tests are now broken :scream: But the `flask run` is still working :muscle: !
Let's continue bravely by instantiating our SQLAlchemy session we will use for all SQL queries (CRUD).

```python
# app/__init__.py
# pylint: disable=missing-docstring

# [...]
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    # [...]
```

### Model

Now it's time to **convert** our existing `Tweet` model to a proper SQLAlchemy model, and not just a regular class. Open the `app/models.py` file and update it:

```python
# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet #{self.id}>"
```

We can also get rid of the tests on the model as it's no longer a regular class. We trust SQLAlchemy with the column behavior, and as we have no instance method here, no need for unit testing:

```bash
rm tests/test_models.py
```

### Alembic setup

We need a local database for our application:

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask"
```

Then we need to isolate a utility file to run the commands without polluting the main `wsgi.py`. Here is how it goes:

```bash
touch manage.py
```

```python
# manage.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from wsgi import create_app
from app import db

application = create_app()

migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

Now we can use Alembic (run `pipenv graph` to see where it stands)!

```bash
pipenv run python manage.py db init
```

This command has created a `migrations` folder, with an empty `versions` in it. Time to run the first migration with the creation of the `tweets` table from the `app/models.py`'s `Tweet` class.

```bash
pipenv run python manage.py db migrate -m "Create tweets table"
```

Open the `migrations/versions` folder: can you see a first migration file? Go ahead, open it and read it! That's a file you **can** modify if you are not happy with what has been automatically generated. Actually that's something the tool tells you:

```bash
# ### commands auto generated by Alembic - please adjust! ###
```

When you are happy with the migration, time to run it against the local database:

```bash
pipenv run python manage.py db upgrade
```

And that's it! There is now a `tweets` table in the `twitter_api_flask` local database. It's empty for now, but it does exist!

## Adding a first tweet from a shell

We want to go the "manual testing route" to update the API controller code by adding manually a first Tweet in the database. It will validate that all our efforts to add SQLAlchemy are starting to pay off:

```bash
pipenv run flask shell
>>> from app import db
>>> from app.models import Tweet
>>> tweet = Tweet(text="Our first tweet!")
>>> db.session.add(tweet)
>>> db.session.commit()
# Did it work?
>>> db.session.query(Tweet).count()
>>> db.session.query(Tweet).all()
# Hooray!
```

## Updating the API controller code

Now that the models have been migrated from dumb Python class to SQLAlchemy proper models backed by a local Postgresql database, we want to update the code in `app/apis/tweets.py` so that it does not use the `tweet_repository` anymore.

We won't use the (outdated) tests to try to make our server _work again_. Run the server:

```bash
FLASK_ENV=development pipenv run flask run
```

:point_right: Go to [localhost:5000/tweets/1](http://localhost:5000/tweets/1). Let's make this work and return a JSON containing the first tweet we created in the `flask shell`.

Look at the error message in the terminal and try to fix the code _yourself_. There's only one line of code to add (an `import`) and another one to change. You can do it :muscle: !

<details><summary markdown='span'>View solution
</summary>

```python
# app/apis/tweets.py
# Add this at the beginning of the file:
from app import db

# Then in the `TweetResource#get` replace this line:
#   tweet = tweet_repository.get(tweet_id))
# with:
tweet = db.session.query(Tweet).get(tweet_id)
```

Congrats! [localhost:5000/tweets/1](http://localhost:5000/tweets/1) is now working!

</details>

Let's leave only the `GET /tweets/:id` route working, not touching the ones, and try to fix the tests first before going back to it.

## Updating the tests

Open the `tests/apis/test_tweet_views.py`. Before we dive into replacing the `tweet_repository` with some `db.session` in here, let's pause and think about what we are doing.

What happens if you run the following in one of your test method?

```python
tweet = Tweet(text="A test tweet")
db.session.add(tweet)
db.session.commit()
```

That's right! It will **create a record** on the database. Which means that if you run the tests 10 times, it will create 10 records! Way to pollute your development environment :disappointed_relieved:

The solution is to:

- Run the test against _another_ database schema
- Clean up the schema (deleting all tables/recreating them) between every test run (every method even!)

Here is how we are going to achieve this goal. First we need to create a new database locally:

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask_test"
```

And then we can update our `TestTweetViews` class with:

```python
# tests/apis/test_tweet_views.py

from flask_testing import TestCase
from app import create_app, db  # Don't forget to take the db import
from app.models import Tweet

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # [...]
```

Now go ahead and update the four tests replacing the `tweet_repository` former logic with some `db.session`. Once you are done, go back to the `app/apis/tweets.py` to fix the API code as well! You can do it :muscle: !

To check if you are making some progress, run the tests:

```bash
nosetests
```

<details><summary markdown='span'>View solution
</summary>

Here is the updated code for the `TestTweetViews` test case:

```python
    # tests/apis/test_tweet_views.py
    # [...]

    def test_tweet_show(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_create(self):
        response = self.client.post("/tweets", json={'text': 'New tweet!'})
        created_tweet = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_tweet["id"], 1)
        self.assertEqual(created_tweet["text"], "New tweet!")

    def test_tweet_update(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.patch("/tweets/1", json={'text': 'New text'})
        updated_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_tweet["id"], 1)
        self.assertEqual(updated_tweet["text"], "New text")

    def test_tweet_delete(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        self.client.delete("/tweets/1")
        self.assertIsNone(db.session.query(Tweet).get(1))
```

And here is the code for `app/apis/tweets.py` where we need to update occurrences of `tweet_repository`:

```python
# [...]

class TweetResource(Resource):
    @api.marshal_with(json_tweet)
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            return tweet

    @api.marshal_with(json_tweet, code=200)
    @api.expect(json_new_tweet, validate=True)
    def patch(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            tweet.text = api.payload["text"]
            db.session.commit()
            return tweet

    def delete(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            db.session.delete(tweet)
            db.session.commit()
            return None

@api.route('')
@api.response(422, 'Invalid tweet')
class TweetsResource(Resource):
    @api.marshal_with(json_tweet, code=201)
    @api.expect(json_new_tweet, validate=True)
    def post(self):
        text = api.payload["text"]
        if len(text) > 0:
            tweet = Tweet(text=text)
            db.session.add(tweet)
            db.session.commit()
            return tweet, 201
        else:
            return abort(422, "Tweet text can't be empty")
```

</details>

## Setting up Travis

Setting up Travis for a project where you have a real PostgreSQL database is not as trivial as for a project without. Let's see how we can iterate on the **Travis setup** already covered:

```bash
touch .travis.yml
```

```yml
# .travis.yml

language: python
python: 3.8
cache: pip
dist: xenial
addons:
  postgresql: 10
install:
  - pip install pipenv
  - pipenv install --dev
before_script:
  - psql -c 'CREATE DATABASE twitter_api_flask_test;' -U postgres
env:
  - DATABASE_URL="postgresql://localhost/twitter_api_flask"
script:
  - pipenv run nosetests
```

Commit & push this change. Then go to [github.com/marketplace/travis-ci](https://github.com/marketplace/travis-ci) to add this `<github-nickname>/twitter-api-database` to your free Travis plan if it's not the case yet.

## Going further

### Tweet list

Let's add another endpoint to our API to retrieve **all tweets**:

```bash
GET /tweets
```

Go ahead, you can TDD it!

## I'm done!

Let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 04-Database/02-Twitter
touch DONE.md
git add DONE.md && git commit -m "04-Database/02-Twitter done"
git push origin master
```
