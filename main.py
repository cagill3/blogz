from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import flask


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:jumpman1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(560))

    def __init__(self, title, body):
        self.title = title
        self.body = body




@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'GET':
        return render_template('new_posts.html', title='Add Blog Entry')

    if request.method == 'POST':
        post_title = request.form['post-title']
        post_body = request.form['post-body']
        if post_title == '':
            title_error = 'Please fill in the title'
            return render_template('new_posts.html', title='Add Blog Entry',
                                    title_error=title_error)
        if post_body == '':
            body_error = 'Please fill in the body'
            return render_template('new_posts.html', title='Add Blog Entry',
                                    body_error=body_error)
        else:
            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()

            posts = Blog.query.all()
            return render_template('blog_entry.html', posts=posts)


@app.route('/blog', methods=['POST','GET'])
def blog_entry():


    if request.method == 'GET':
        posts = Blog.query.all()
        return render_template('blog_entry.html', title='Build a Blog App',
                                posts=posts)


if __name__ == '__main__':
    app.run()
