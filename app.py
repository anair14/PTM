import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                group_name TEXT
             )''')
conn.commit()
conn.close()

@app.route('/')
def index():
    # Fetch tasks and groups from the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = c.fetchall()
    c.execute('SELECT DISTINCT group_name FROM tasks')
    groups = [row[0] for row in c.fetchall() if row[0] is not None]
    conn.close()
    return render_template('index.html', tasks=tasks, groups=groups)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    group_name = request.form['group_name']
    # Insert the task into the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task_name, group_name) VALUES (?, ?)', (task_name, group_name))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    # Delete the task from the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
