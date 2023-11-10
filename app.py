from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    
def init_db():
    with app.app_context():
        db.create_all()  # Create the database
        # Add 5 random users to the database
        for i in range(5):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = 'password'
            # Check if the username or email already exists
            if User.query.filter_by(username=username).first() is None and \
               User.query.filter_by(email=email).first() is None:
                user = User(username=username, email=email, password=password)
                db.session.add(user)
        db.session.commit()

@app.route('/')
def index():
    with app.app_context():
        username = request.args.get('username')
        users = []
        if username:
            connection = db.engine.connect()
            # Ceci est vulnérable aux injections SQL
            statement = text(f"SELECT * FROM user WHERE username = '{username}'")
            # ' UNION SELECT id, email, password, NULL FROM user --
            # -> Enter this to output all users with passwords
            result = connection.execute(statement)
            users = result.fetchall()
            connection.close()
        return render_template('index.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        init_db()
        app.run(debug=True, host='0.0.0.0', port=5001)