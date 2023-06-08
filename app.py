from flask import Flask, request, render_template
import sqlite3
app = Flask(__name__)


conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
conn.commit()
conn.close()
@app.route('/')
def index_page():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/submit', methods=['POST'])
def submit():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    task = request.form.get('task-input')
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    print(tasks)
    return render_template('index.html', tasks=tasks)

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
    return render_template('index.html', tasks=tasks)


with app.app_context():
    app.run()