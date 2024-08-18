from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_usernames.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TwitterUsername(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_username():
    username = request.form.get('username')
    if TwitterUsername.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already followed'}), 400
    new_username = TwitterUsername(username=username)
    db.session.add(new_username)
    db.session.commit()
    return jsonify({'message': 'Followed successfully'}), 200

if __name__ == '__main__':
    with app.app_context():  # Ensure the application context is available
        db.create_all()  # Create database tables
    app.run(debug=True)
