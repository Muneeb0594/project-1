from application import db, app, bcrypt 
from application.models import BlogPosts, User
from application.forms import LoginForm, RegisterForm
from flask import render_template, redirect, url_for

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


