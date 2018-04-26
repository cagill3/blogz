from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import cgi
import flask

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:jumpman1@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    '''creates Blog table in DB'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(560))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Blog %r>' % self.title

class User(db.Model):
    '''creates User table in DB'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


#require user to be logged in to access blogs
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog_entry', 'logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            no_user = 'User does not exist. Signup!'
            return render_template('signup.html', error=no_user)

    if request.method == 'GET':
        return render_template('login.html', title='Blogz')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username == '':
            no_username = "You must enter a username"
            return render_template('signup.html', user_error=no_username)
        if password == '':
            no_password = "You must enter a password"
            return render_template('signup.html', pw_error=no_password)
        if verify == '':
            not_verified = "You must verify password"
            return render_template('signup.html', vfy_error=not_verified)
        if password != verify:
            no_match = "passwords don't match"
            return render_template('signup.html', match_error=no_match)


        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

        if existing_user:
            user_exists = 'Username already taken!'
            return render_template('signup.html', error=user_exists)

    if request.method == 'GET':
        return render_template('signup.html', title='Blogz')

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        return redirect('/blog')
    else:
        return redirect('/blog')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    posts = Blog.query.all()
    return render_template('index.html', title='Blogz', users=users, posts=posts)



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

        if request.method == 'GET':
            return render_template('new_posts.html', title='Blogz')

@app.route('/blogs')
def single_User():
    owner = request.args.get('user')
    print("*****************************************First"+str(owner)+"*************************************************")
    user = User.query.filter_by(username=owner).first()
    blogs = Blog.query.filter_by(owner=user).all()
    print("*****************************************Second"+str(blogs)+"*************************************************")
    return render_template('single_User.html', blogs=blogs, user=user)

@app.route('/blog', methods=['POST','GET'])
def blog_entry():

        if request.method == 'GET':
            post_id = request.args.get('id')
            print("******************************************************************************************")
            print("******************************************************************************************")
            print("******************************************************************************************")
            print("******************************************************************************************")

            if type(post_id) == str:
                posts = Blog.query.get(post_id)
                return render_template('view_post.html', posts=posts)
                if post_id in post_users:
                    posts = User.query.filter_by(username=post_id).first()
                    return render_template('single_User.html', posts=posts)
            #TODO need another if statement to render single_User.html template
            else:
                posts = Blog.query.all()
                print("******************************************************************************************")
                print("******************************************************************************************")
                print("******************************************************************************************")
                print("******************************************************************************************")
                return render_template('blog_entry.html', title='Blogz',
                                            posts=posts)

        if request.method == 'POST':
            post_title = request.form['post-title']
            post_body = request.form['post-body']
            owner = User.query.filter_by(username=session['username']).first()
            if post_title == '':
                title_error = 'Please fill in the title'
            else:
                title_error = ''
            if post_body == '':
                body_error = 'Please fill in the body'
            else:
                body_error = ''

            if title_error == '' and body_error == '':

                new_post = Blog(post_title, post_body, owner)
                db.session.add(new_post)
                db.session.commit()
                id= str(new_post.id)
                return redirect('/blog?id=' + id, )

            else:
                return render_template('new_posts.html', title='Blogz', title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()
