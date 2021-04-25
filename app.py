from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_data_from_db(sqlCommand, many = 1):
    conn = get_db_connection()
    if many == 1:
        data = conn.execute(sqlCommand).fetchall()
    else:
        data = conn.execute(sqlCommand).fetchone()
    conn.close()
    return data

def execute_comm(command, values):
    conn = get_db_connection()
    data = conn.execute(command, values)
    conn.commit()
    conn.close()
    return data

def get_post(postId):
    post = get_data_from_db('SELECT * FROM posts WHERE id = ' + str(postId), 0)
    if post is None:
        abort(404)
    return post

def validatePost(post):
    valid = 1
    if not post['title']:
        valid = 0
        flash('Title is required')
    elif not post['content']:
        valid = 0
        flash('Content is required')
    return valid


@app.route('/')
def index():
    return render_template('index.html', posts=get_data_from_db('SELECT * FROM posts'))

@app.route('/about')
def about():
    return render_template(
        'pages/about.html',
        pageInfo=get_data_from_db("SELECT * FROM pagesInfo WHERE pageName = 'about'", 0)
    )

@app.route('/post/<int:postId>')
def post(postId):
    return render_template('pages/post.html', post = get_post(postId))

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def postEdit(id):
    post = get_post(id)
    valid = request.method == 'POST' and validatePost(request.form)
    if valid:
        title = request.form['title']
        content = request.form['content']
        execute_comm('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        return redirect(url_for('index'))
    else:
        return render_template('pages/edit.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    valid = request.method == 'POST' and validatePost(request.form)
    if valid:
        title = request.form['title']
        content = request.form['content']
        execute_comm('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        return redirect(url_for('index'))
    else:
        return render_template('pages/create.html')

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    post = get_post(id)
    execute_comm('DELETE FROM posts WHERE id = ?', (id,))
    flash('"{}" Successfully deleted'.format(post['title']))
    return redirect(url_for('index'))