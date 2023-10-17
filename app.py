from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello12345'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    # Convert the user ID to an integer
    user_id = int(user_id)
    
    # Find the user by ID in the users list
    user = next((user for user in users if user.id == user_id), None)
    
    return user

# Dummy data for blog posts (you can replace this with a database)
blog_posts = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the first blog post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'This is the second blog post.'}
]

# Dummy user data (for testing purposes)
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

users = [
    User(id=1, username='user1', email='user1@example.com', password=generate_password_hash('password123', method='sha256')),
    User(id=2, username='user2', email='user2@example.com', password=generate_password_hash('password456', method='sha256'))
]

# Home page
@app.route('/')
def home():
    form = RegistrationForm()  # Assuming RegistrationForm is defined in a separate file
    return render_template('home.html', form=form)


# Display a list of blog posts
@app.route('/posts')
def post_list():
    return render_template('post_list.html', posts=blog_posts)

# View an individual blog post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    # Find the post with the given post_id from the dummy data
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    
    if post:
        return render_template('view_post.html', post=post)
    else:
        return "Post not found", 404

# Add a new blog post (requires user authentication)
@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        # Process form submission for adding a new post
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Create a new blog post (you can save it to a database)
        new_post = {'id': len(blog_posts) + 1, 'title': title, 'content': content}
        blog_posts.append(new_post)
        
        return redirect(url_for('post_list'))
    
    return render_template('add_post.html')

# User registration page (simplified, no database integration)
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Assuming RegistrationForm is defined in a separate file
    if form.validate_on_submit():
        # Check if the user already exists (you can replace this with a database query)
        existing_user = next((user for user in users if user.email == form.email.data), None)
        if existing_user:
            flash('Email address is already registered.', 'danger')
            return redirect(url_for('register'))

        # Create a new user (you can replace this with database user creation)
        new_user = User(id=len(users) + 1,
                        username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data, method='sha256'))
        users.append(new_user)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists (you can replace this with a database query)
        user = next((user for user in users if user.email == form.email.data), None)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard or a protected route
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

if __name__ == '__main__':
    app.run()
