# Flask templates

In this exercise, we will re-use the yesterday's application from the `01-SQLAlchemy-Recap` exercise:

```bash
cd ~/code/<user.github_nickname>/flask-with-sqlalchemy
```

Make sure your `git status` is clean (`add` and `commit` the WIP), and that your server can still be started:

```bash
FLASK_ENV=development pipenv run flask run
```

## Homepage

The goal of this exercise will be to replace the following action:

```python
@app.route('/')
def hello():
    return "Hello World!"
```

Instead of returning a plain text sentence, we want to actually build a nice HTML page.

We want you to build two pages:
- a `home` page with a grid of products (`/`)
- and a dynamic `detail` page with a given product (`/:id`)
When a user browses the home page, it should be able to easily go to a "show" page by clicking on a link.

First take some time to read the [Flask Templates](http://flask.pocoo.org/docs/1.0/tutorial/templates/) documentation. This is part of the `flask` package. Take also some time to read more about [Jinja](http://jinja.pocoo.org/docs/2.10/templates/), the templating language used by Flask.

```bash
mkdir templates
touch templates/base.html
```

Let's start with the [Bootstrap template](https://getbootstrap.com/docs/4.1/getting-started/introduction/) adapted to insert a Jinja **block**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">

    <title>Products</title>
  </head>
  <body>
    <div class="container">
      {% block content %}{% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
  </body>
</html>
```

In the controller (`wsgi.py`), you can instantiate:

```python
from flask import Flask, abort, request, render_template

# [...]

@app.route('/')
def home():
    products = db.session.query(Product).all()

    return render_template('home.html', products=products)
```

Try to navigate to the [`localhost:5000`](http://localhost:5000) on the Homepage. What error do you get? What should we do?

We need to create a new file `templates/home.html` and use the `products` variable from the `wsgi.py` to the `home.html` file thanks to the `render_template` arguments.

```bash
touch templates/home.html
```

```html
<!-- templates/home.html -->

{% extends 'base.html' %}

{% block content %}
  <h1>Products</h1>

  <ul class="list-unstyled">
    {% for product in products %}
      <li>{{ product.name }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```

The `list-unstyled` class is from [Bootstrap](https://getbootstrap.com/docs/4.1/content/typography/#unstyled).

The content within the `block content` is inserted back into the `base.html`.

## Product page

We now want to implement a **dynamic** product page display information about a single one. The idea is to change the `<li>` elements from the `home.html` and put **links** on them:

Before:

```html
<li>{{ product.name }}</li>
```

After (using [`url_for`](http://flask.pocoo.org/docs/1.0/api/#flask.url_for)):

```html
<li>
  <a href="{{ url_for('product_html', product_id=product.id) }}">{{ product.name }}</a>
</li>
```

First, we need to add a new route to the controller (`wsgi.py`):

```python
# [...]

@app.route('/<int:product_id>')
def product_html(product_id):
    product = db.session.query(Product).get(product_id)
    return render_template('product.html', product=product)
```

If you reload your `/` home page, you should be able to click on a link in the list. If you do so, you should get a `jinja2.exceptions.TemplateNotFound` once again, which tells you which file you are missing.

:point_right: Go ahead and **create** the missing template.

<details><summary markdown="span">View solution
</summary>

You need to run:

```bash
touch templates/product.html
```

</details>


Let's create the Product page with the `product` variable passed in the `render_template` call:

```html
<!-- templates/product.html -->

{% extends 'base.html' %}

{% block content %}
  <a href="{{ url_for('home') }}">← Back to list</a>

  <h1>{{ product.name }}</h1>

  <!-- What other columns do you have in the `products` table? Use them here! -->
{% endblock %}
```

Do not forget to commit and push your changes to your GitHub repository.

## I'm done!

Before you jump to the next exercise, let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 05-Front-end/01-Templates
touch DONE.md
git add DONE.md && git commit -m "05-Front-end/01-Templates done"
git push origin master
```
