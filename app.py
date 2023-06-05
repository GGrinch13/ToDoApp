from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')

with app.app_context():
    db.create_all()
    app.run()