class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

# Dummy data for testing
users.append(User(id=1, username='user1', email='user1@example.com', password=generate_password_hash('password1', method='sha256')))
users.append(User(id=2, username='user2', email='user2@example.com', password=generate_password_hash('password2', method='sha256')))
users.append(User(id=3, username='user3', email='user3@example.com', password=generate_password_hash('password3', method='sha256')))
