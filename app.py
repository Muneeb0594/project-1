from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = str(os.getenv('SECRET_KEY'))
db = SQLAlchemy(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Posts ' + str(self.id)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
	if request.method == 'POST':
		post_title = request.form['title']
		post_content = request.form['content']
		post_author = request.form['author']
		new_post = BlogPosts(title=post_title, content=post_content, author=post_author)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		all_posts = BlogPosts.query.order_by(BlogPosts.date_posted).all()
		return render_template('posts.html', posts=all_posts)

@app.route('/home/users/<string:name>/posts/<int:id>')
def home(name, id):
    return "Hello!!, " + name + ", your id is: " + str(id)

@app.route('/onlyget', methods=['GET'])
def get_req():
	return 'You Can Only Get This Webpage Fella!...'

@app.route('/posts/delete/<int:id>')
def delete(id):
	post = BlogPosts.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

	post = BlogPosts.query.get_or_404(id)

	if request.method == 'POST':
		post.title = request.form['title']
		post.author = request.form['author']
		post.content = request.form['content']
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('edit.html', post=post)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

class LoginForm(FlaskForm):
        email = StringField('Email: ',validators = [DataRequired(), Email()])
        password = PasswordField('Password: ',validators = [DataRequired()])
        submit = SubmitField('OK')

def validate_email(self, email):
    existing_users = User.query.filter_by(email=email.data).all()
    if not existing_users:
        raise ValidationError('User does not exist.')
    return render_template('login.html')

class PostForm(FlaskForm):
	title = StringField('Title: ', validators = [DataRequired()])
	content = PasswordField('Content: ', validators = [DataRequired()])
	submit = SubmitField('OK')

@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', form=form)

class RegisterForm(FlaskForm):
    email = StringField('Email: ', validators = [DataRequired(), Email()])
    password = PasswordField('Password: ', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('OK')

def validate_email(self, email):
    existing_users = User.query.filter_by(email=email.data).all()
    if existing_users:
        raise ValidationError('A user with that email is already registered.')
    return render_template ('register.html')

