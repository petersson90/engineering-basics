# Flask Admin

If you want to easily add a back-office to your application, the [`flask-admin`](https://flask-admin.readthedocs.io/en/latest/) package might help you. The main idea of this package is to build a simple CRUD app from a few python lines.

Once again, we can use our product app to test the `flask-admin` package:

```bash
cd ~/code/<user.github_nickname>/flask-with-sqlalchemy
```

Make sure your `git status` is clean and don't forget to work in a branch!

```bash
git checkout -b flask-admin
```

Let's install the `flask-admin` package with:

```bash
pipenv install flask-admin
```

Open your `wsgi.py` and add the following import at the top of the file, just after `import Flask`:

```python
from flask_admin import Admin
```

In the `wsgi.py`, before the first `@app.route`, initialize your new `Admin` object with:

```python
# [...]
admin = Admin(app, template_mode='bootstrap3')
# [...]
```

If you haven't done it yet, start your flask server:

```bash
FLASK_ENV=development pipenv run flask run
```

And now navigate to [`localhost:5000/admin`](http://localhost:5000/admin). You should see an empty Admin Home page. It's now time to populate it!

In the `wsgi.py` file, set up the models you want to add to this `/admin`:

```python
# This goes at the top of your file, after the `from flask_admin...` for instance
from flask_admin.contrib.sqla import ModelView

# This goes after `admin =` & the import of models:
admin.add_view(ModelView(Product, db.session))
```

Reload the [`localhost:5000/admin`](http://localhost:5000/admin) page. Isn't it lovely?

To be able to use all the CRUD features, you need to make sure that your app has a [**secret**](https://flask.pocoo.org/docs/1.0/quickstart/?highlight=secret#sessions). To do so, open the `config.py` and add another line to your `Config` object:

```python
SECRET_KEY = os.environ['SECRET_KEY']
```

You also need to add new environment variable `SECRET_KEY` to your `.env`. To generate a random secret key, you can use the following technique:

```bash
python -c 'import secrets; print(secrets.token_urlsafe(16))'
```

:rocket: Go ahead, try create, update and delete products with this new admin panel!

Don't forget to commit and push your branch.

## Going further

You might worry that you users get access to this admin panel, and you should! Flask-admin's documentation has [a section about this](https://flask-admin.readthedocs.io/en/latest/introduction/#authorization-permissions).

## I'm done!

Before you jump to the next exercise, let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 05-Front-end/02-Flask-Admin
touch DONE.md
git add DONE.md && git commit -m "05-Front-end/02-Flask-Admin done"
git push origin master
```
