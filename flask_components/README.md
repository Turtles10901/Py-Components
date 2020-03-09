# Flask-Components

Flask-Components is a Flask extension to create reuseable 'Components' that render themselves as HTML.

### Usage

in initialization
```python
from flask import Flask
from flask_components import FlaskComponents

#config goes here

app = Flask(__name__)
components = FlaskComponents(app)
```

in views
```python
@app.route('/')
def index():
    return render_template("index.html",components=components)
```