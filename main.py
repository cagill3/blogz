from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import flask

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:jumpman1@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(560))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user

    def __repr__(self):
        return '<Blog %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()

            return redirect('/newpost')

        else:
            return "<h1>Duplicate User</h1>"

    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            #TODO remember user has logged in
            return redirect('/newpost')
        else:
            #TODO why login failed
            return '<h1>Error!</h2>'

    if request.method == 'GET':
        return render_template('login.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/logout', methods=['POST'])
def logout():
    return redirect('/blog')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('new_posts.html', title='Add Blog Entry')

    if request.method == 'POST':
        return render_template('new_posts.html', title='Add Blog Entry')


@app.route('/blog', methods=['POST','GET'])
def blog_entry():

    if request.method == 'GET':
        post_id = request.args.get('id')

        if type(post_id) == str:
            posts = Blog.query.get(post_id)
            return render_template('view_post.html', title='Blog post #'+ str(post_id),
                                    posts=posts)
        else:
            posts = Blog.query.all()
            return render_template('blog_entry.html', title='Build a Blog App',
                                        posts=posts)

    if request.method == 'POST':
        post_title = request.form['post-title']
        post_body = request.form['post-body']

        if post_title == '':
            title_error = title_error = 'Please fill in the title'
        else:
            title_error = ''
        if post_body == '':
            body_error = 'Please fill in the body'
        else:
            body_error = ''

        if title_error == '' and body_error == '':

            new_post = Blog(post_title, post_body, user)
            db.session.add(new_post)
            db.session.commit()
            id= str(new_post.id)
            return redirect('/blog?id=' + id)

        else:
            return render_template('new_posts.html', title_error=title_error, body_error=body_error)


if __name__ == '__main__':
    app.run()
