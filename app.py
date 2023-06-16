from flask import Flask, request, render_template
import sqlite3
app = Flask(__name__)


conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed INTEGER DEFAULT 0)''')
conn.commit()
conn.close()

@app.route('/')
@app.route('/complete/index.html')
@app.route('/delete/index.html')
@app.route('/index.html')
def index_page():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    return render_template('index.html', tasks=tasks), 200


@app.route('/about')
@app.route('/complete/about.html')
@app.route('/delete/about.html')
@app.route('/about.html')
def about_page():
    return render_template('about.html')


@app.route('/submit', methods=['POST'])
def submit():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    task = request.form.get('task-input')
    if not task.strip():
        return 'Fill in the task field!', 400
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    return render_template('index.html', tasks=tasks), 200

#
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', tasks=tasks), 200

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    conn.commit()
    tasks = c.fetchall()

    conn.close()

    return render_template('index.html', tasks=tasks), 200

@app.route('/task.html')
@app.route('/delete/task.html')
@app.route('/complete/task.html')
def task_page():
    return render_template('task.html')

#Uncomment this if developing
# with app.app_context():
#     app.run()