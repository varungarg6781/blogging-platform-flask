from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Dummy data for blog posts (you can replace this with a database)
blog_posts = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the first blog post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'This is the second blog post.'}
]

# Home page
@app.route('/')
def home():
    return render_template('home.html')

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
    if request.method == 'POST':
        # Process user registration form submission
        username = request.form.get('username')
        password = request.form.get('password')
        
        # You can add user registration logic here (e.g., store in a database)
        
        return redirect(url_for('login'))  # Redirect to the login page after successful registration
    
    return render_template('register.html')

# Login page (placeholder, you can implement authentication)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form submission
        # You can implement user authentication logic here
        
        return redirect(url_for('post_list'))  # Redirect to the post list page after successful login
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
