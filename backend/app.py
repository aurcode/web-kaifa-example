from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key in production
jwt = JWTManager(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@'
    f'{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Market(db.Model):
    __tablename__ = 'markets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(200))
    state = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=False)

    market = db.relationship('Market', backref=db.backref('reviews', lazy=True))

# User Registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# User Login (JWT Token Generation)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

# Endpoint to fetch markets
@app.route('/markets', methods=['GET'])
def get_markets():
    markets = Market.query.all()
    return jsonify([{
        'id': market.id,
        'name': market.name,
        'city': market.city,
        'state': market.state,
        'postal_code': market.postal_code,
        'latitude': market.latitude,
        'longitude': market.longitude
    } for market in markets]), 200

# Endpoint to fetch reviews of a specific market
@app.route('/markets/<int:market_id>/reviews', methods=['GET'])
def get_reviews(market_id):
    reviews = Review.query.filter_by(market_id=market_id).all()
    return jsonify([{
        'id': review.id,
        'username': review.username,
        'text': review.text,
        'score': review.score
    } for review in reviews]), 200

# Endpoint to create a review (requires JWT)
@app.route('/markets/<int:market_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(market_id):
    username = get_jwt_identity()
    data = request.get_json()
    score = data.get('score')
    text = data.get('text', '')

    if not isinstance(score, int) or not (1 <= score <= 5):
        return jsonify({'error': 'Score must be an integer between 1 and 5'}), 400

    new_review = Review(market_id=market_id, username=username, text=text, score=score)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({
        'message': 'Review submitted successfully',
        'data': {'username': username, 'score': score, 'text': text}
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
