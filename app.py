from flask import Flask, request, render_template
import sqlite3
app = Flask(__name__)


conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed INTEGER DEFAULT 0, description TEXT DEFAULT "")''')
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
    conn.close()

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
    conn.close()
    return render_template('index.html', tasks=tasks), 200
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    conn.commit()
    conn.close()
    alert_message = f'Task  has been deleted!'
    return render_template('index.html', tasks=tasks, alert_message=alert_message), 200

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    print(task_id)
    conn.commit()
    conn.close()
    return render_template('index.html', tasks=tasks), 200

@app.route('/task.html')
@app.route('/task/<int:task_id>')
@app.route('/delete/task.html')
@app.route('/complete/task.html')
@app.route('/save/<int:task_id>', methods=['POST'])
def task_page(task_id):

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = c.fetchall()
    if request.method == 'POST':
        description = request.form.get('descc')
        c.execute("UPDATE tasks SET description = ? WHERE id = ?", (description, task_id))

    c.execute("SELECT description, task FROM tasks WHERE id = ?", (task_id,))
    # c.execute("SELECT task FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    description = row[0]
    task = row[1]
    conn.commit()
    print(task)
    conn.close()
    return render_template('task.html', task=task, tasks=tasks, task_id=task_id, description=description), 200

#Uncomment this if developing
# with app.app_context():
#    app.run()
#
