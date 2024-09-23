# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Configure the database URI for MySQL using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@'
    f'{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}'
)

# Disable track modifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define the Score model representing the 'scores' table in the database
class Score(db.Model):
    __tablename__ = 'scores'  # Name of the database table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    username = db.Column(db.String(50), nullable=False)  # Username column
    score = db.Column(db.Float, nullable=False)  # Score column

# Create all database tables within the application context
with app.app_context():
    db.create_all()  # Create the tables defined in the models

# Define a route to submit a new score
@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()  # Get the JSON data from the request
    # Check if 'username' and 'score' are in the data
    if 'username' not in data or 'score' not in data:
        return jsonify({'error': 'Missing username or score'}), 400  # Return an error if missing

    username = data['username']  # Extract username from data
    score = data['score']  # Extract score from data

    # Validate that the score is a number (integer or float)
    if not isinstance(score, (int, float)):
        return jsonify({'error': 'Score must be a number'}), 400  # Return an error if score is invalid

    # Create a new Score instance
    new_score = Score(username=username, score=score)
    db.session.add(new_score)  # Add the new score to the session
    db.session.commit()  # Commit the session to save the score in the database

    # Return a success message and the submitted score
    return jsonify({'message': 'Score submitted successfully', 'data': {'username': username, 'score': score}}), 201

# Define a route to retrieve all submitted scores
@app.route('/scores', methods=['GET'])
def get_scores():
    scores = Score.query.all()  # Query all scores from the database
    # Return a JSON response containing all scores
    return jsonify([{'username': score.username, 'score': score.score} for score in scores]), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available IP addresses at port 5000
