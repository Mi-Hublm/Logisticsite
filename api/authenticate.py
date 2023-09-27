from flask import Flask, request, jsonify, current_app, render_template
import secrets
from flask_argon2 import Argon2
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import pyotp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/my_database'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email_address'
app.config['MAIL_PASSWORD'] = 'your_email_password'

argon2 = Argon2(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
mail = Mail(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)
ma = Marshmallow(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Set up logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    login_attempts = db.Column(db.Integer, default=0)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    backup_codes = db.relationship('BackupCode', backref='user', lazy=True)

    def set_password(self, password):
        self.password = argon2.generate_password_hash(password)

    def check_password(self, password):
        return argon2.check_password_hash(self.password, password)

class BackupCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    code = db.Column(db.String(16), nullable=False, unique=True)

class TwoFactorSecret(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    secret = db.Column(db.String(255), nullable=False)

db.create_all()

# Set up custom error handlers

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"message": "Bad Request"}), 400

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"message": "Forbidden"}), 403

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"message": "Not Found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"message": "Internal Server Error"}), 500

@app.route("/api/authenticate", methods=["POST"])
@limiter.limit("5 per minute")
def authenticate():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        if not user.email_verified:
            logger.warning(f"Authentication failed: Email address not verified for user {username}")
            return abort(403, "Email address not verified")

        if user.two_factor_enabled:
            # Get the user's 2FA secret
            two_factor_secret = TwoFactorSecret.query.filter_by(user_id=user.id).first()

            # Verify the user's 2FA code with a longer time step (e.g., 60 seconds)
            totp = pyotp.TOTP(two_factor_secret.secret, interval=60)
            if not totp.verify(data.get("2fa_code")):
                logger.warning(f"Authentication failed: Invalid 2FA code for user {username}")
                return abort(401, "Invalid 2FA code")

        access_token = create_access_token(identity=username)
        logger.info(f"Authentication successful for user {username}")
        return jsonify({"message": "Authentication successful", "access_token": access_token}), 200
    logger.warning(f"Authentication failed: Invalid credentials for user {username}")
    return abort(401, "Invalid credentials")

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # Check if the username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        logger.warning(f"Registration failed: Username or email already in use for user {username}")
        return abort(400, "Username or email already in use")

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Send email verification
    verification_token = generate_email_verification_token()
    send_verification_email(email, verification_token)

    logger.info(f"Registration successful for user {username}")
    return jsonify({"message": "Registration successful. Check your email for verification instructions."}), 201


def generate_email_verification_token():
    # Generate a random and secure token
    token = secrets.token_hex(token_length)
    return token

def send_verification_email(email, token):
    msg = Message("Verify your email", sender="your_email_address", recipients=[email])
    msg.body = f"Click the following link to verify your email: http://yourwebsite.com/verify?token={token}"
    mail.send(msg)

if __name__ == "__main__":
    app.run(debug=True)
