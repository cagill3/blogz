from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:jumpman1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(560))

    def __init__(self, name):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.name



@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['post-title']
        post_body = request.form['post-body']
        new_post = Blog(new_post)
        db.session.add(new_post_title, new_post_body)
        db.session.commit()

        return render_template('blog_entry.html', post_title=post_title, post_body=post_body)

    if request.method == 'GET':
        return render_template('new_posts.html')


@app.route('/blog', methods=['POST','GET'])
def blog_entry():


    if request.method == 'POST':
        post_title = request.form['post-title']
        post_body = request.form['post-body']
        return render_template('blog_entry.html', post_title=post_title, post_body=post_body)

    if request.method == 'GET':
        post = Blog.query.all()
        return render_template('blog_entry.html', post=post)



if __name__ == '__main__':
    app.run()
