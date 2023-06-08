from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')

with app.app_context():
    app.run()