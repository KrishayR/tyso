
from flask import Flask, flash, jsonify, make_response, render_template, Response, session, abort, redirect, request
from flask import url_for
import numpy as np
import mediapipe as mp
import os
import pathlib
from google_auth_oauthlib.flow import Flow 
import requests
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import datetime, timedelta
import json
import sqlite3
from descope import DescopeClient
from functools import wraps


try:
    descope_client = DescopeClient(project_id="replace") # initialize the descope client
except Exception as error:
    print ("failed to initialize. Error:")
    print (error)


app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'something'
app.secret_key = "something"
app.config['SESSION_TYPE'] = 'sqlalchemy'
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'

# Create a connection to the database
conn = sqlite3.connect('workouts.db', check_same_thread=False)




# Initialize the Session object with the Flask app instance
Session(app)



GOOGLE_CLIENT_ID = "something.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # Remove in Production, domain needs https

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Google_Session(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.String())
    expiry = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, session_id, data, expiry):
        self.session_id = session_id
        self.data = json.dumps(data)
        self.expiry = expiry


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm Password"}, validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class ResetRequestForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})

    submit = SubmitField('Reset Password')




# def generate():
#     global counter, stage, prev_left_shoulder, prev_right_shoulder, shoulder_moving
#     # Change confidence to be tighter on user's form
#     with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.6) as pose:
#         while cap.isOpened():
#             ret, frame = cap.read()

#             # Recolor to RGB
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False # Improves Performance

#             # Detection
#             results = pose.process(image)

#             # Recolor back to BGR
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Improves Performance

#             # Extract Landmarks
#             try:
#                 landmarks = results.pose_landmarks.landmark

#                 # Shoulder Movement
#                 left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                 right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
#                 if prev_left_shoulder is not None and prev_right_shoulder is not None:
#                     left_dx = left_shoulder[0] - prev_left_shoulder[0]
#                     left_dy = left_shoulder[1] - prev_left_shoulder[1]
#                     right_dx = right_shoulder[0] - prev_right_shoulder[0]
#                     right_dy = right_shoulder[1] - prev_right_shoulder[1]
#                     if abs(left_dx) > 0.05 or abs(left_dy) > 0.05 or abs(right_dx) > 0.05 or abs(right_dy) > 0.05:
#                         shoulder_moving = True
                        
#                 prev_left_shoulder = left_shoulder
#                 prev_right_shoulder = right_shoulder

#                 # Bicep Curl
#                 left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                 left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#                 left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
#                 left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
#                 left_distance = np.sqrt((left_elbow[0] - left_hip[0])**2 + (left_elbow[1] - left_hip[1])**2)
#                 angle_left = calculate_angles(left_shoulder, left_elbow, left_wrist)
#                 cv2.putText(image, str(round(angle_left)), tuple(np.multiply(left_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

#                 right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
#                 right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
#                 right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
#                 right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
#                 right_distance = np.sqrt((right_elbow[0] - right_hip[0])**2 + (right_elbow[1] - right_hip[1])**2)
#                 angle_right = calculate_angles(right_shoulder, right_elbow, right_wrist)
#                 cv2.putText(image, str(round(angle_right)), tuple(np.multiply(right_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#                 # cv2.putText(image, str(right_distance), tuple(np.multiply(right_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

#                 # Curling logic
#                 if not shoulder_moving:
#                     if left_distance < 0.3 and right_distance < 0.3:
#                         if angle_left > 165 and angle_right > 165:
#                             stage = "extended"
#                         elif angle_left < 165 and angle_right < 165 and stage == "compressed":
#                             cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
#                             text = "Extend your arms fully, making sure your elbows are almost straight."
#                             cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 2, cv2.LINE_AA)

#                         if (angle_left < 25 and stage == "extended") and (angle_right < 25 and stage == "extended"):
#                             stage = "compressed"
#                             counter += 1
#                         elif angle_left > 25 and angle_right > 25 and stage == "extended":
#                             cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
#                             text = "Contract your arms fully, so that the dumbell almost touches your shoulder."
#                             cv2.putText(image, text, (40, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 2, cv2.LINE_AA)
#                     else:
#                         cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
#                         text = "Form Tip: Your elbows should be tucked in when performing the bicep curl."
#                         cv2.putText(image, text, (40, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#                 else:
#                     shoulder_moving = False

#             except Exception as err:
#                 pass


#             # Counter text
#             cv2.rectangle(image, (0, 0), (225, 73), (51, 68, 255), -1)
#             cv2.putText(image, "REPS: ", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#             cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

#             # Rendering connections
#             mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                 mp_drawing.DrawingSpec(color=(56, 55, 54), thickness=2, circle_radius=2),
#                 mp_drawing.DrawingSpec(color=(51, 68, 255), thickness=2, circle_radius=2)
#             )

#             # Convert to JPEG
#             ret, jpeg = cv2.imencode('.jpg', image)

#             # Generate response
#             yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')








@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    elif 'name' in session:
        return redirect(url_for('protected_area'))
    else:
        return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dash():
    return render_template('dashboard.html')


# @app.route('/workout')
# def workout():
#     return render_template('workout.html')




@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy-policy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')


# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         print(session)
#         if ("session_id" in session) or (current_user.is_authenticated):
#             return function()
#         else:
#             print("User is logged in, proceeding to protected area")
#             return abort(401)

#     wrapper.__name__ = function.__name__
#     return wrapper

@app.route('/weight')
def weight():
    return render_template('weight.html')

@app.route('/workout')
def workout():
    ret = render_template('workout.html')
    return ret

@app.route('/startworkout')
def startworkout():
    ret = render_template('startworkout.html')
    return ret

@app.route('/finish')
def workoutsummary():
    ret = render_template('workoutsummary.html')
    return ret


@app.route('/bicepcurls')
def bicepcurls():
    ret = render_template('bicepcurls.html')
    return ret

@app.route('/deadlifts')
def deadlifts():
    ret = render_template('deadlifts.html')
    return ret

@app.route('/frontraises')
def front():
    ret = render_template('frontraises.html')
    return ret

@app.route('/lateralraises')
def lats():
    ret = render_template('lateralraises.html')
    return ret

@app.route('/pushups')
def pushup():
    ret = render_template('pushups.html')
    return ret

@app.route('/shoulderpress')
def shoulderpress():
    ret = render_template('shoulderpress.html')
    return ret

@app.route('/squats')
def squats():
    ret = render_template('squats.html')
    return ret

@app.route('/tricepextensions')
def triceps():
    ret = render_template('tricepextensions.html')
    return ret

@app.route('/blog')
def blog():
    ret = render_template('blog.html')
    return ret

@app.route('/how-to-gain-weight-and-muscle-as-a-skinny-teen')
def post1():
    ret = render_template('post1.html')
    return ret

@app.route('/finish')
def finish():
    ret = render_template('finish.html')
    return ret

@app.route('/rocket')
def rocket():
    ret = render_template('tysorocket.html')
    return ret


@app.route('/progress')
def progress():
    global conn
    conncursor = conn.cursor()
    if 'name' in session:  # User is logged in through Google auth
        username = session['name']
    elif current_user.is_authenticated:  # User is logged in through Flask-Login
        print(current_user.is_authenticated)
        username = current_user.username
    else:  # User is not logged in
        username = None
    conncursor.execute('SELECT * FROM workouts WHERE username=?', (username,))
    workouts = conncursor.fetchall()
    return render_template('progress.html', current_user=current_user, workouts=workouts)










# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     error = False
#     form = ResetRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             flash("Reset Request Sent. Check your mail.")
#         else:
#             error = True

#     return render_template("pwdreset.html", form=form, error=error)


def token_required(f): # auth decorator
    @wraps(f)
    def decorator(*args, **kwargs):
        # print(request.headers['Authorization'])
        session_token = None
        if 'Authorization' in request.headers: # check if token in request
            auth_request = request.headers['Authorization']
            session_token = auth_request.replace('Bearer ', '')
        if not session_token: # throw error
            return make_response(jsonify({"error": "❌ invalid session token in the request!"}), 401)

        try: # validate token
            jwt_response = descope_client.validate_session(session_token=session_token)
        except:
            return make_response(jsonify({"error": "❌ invalid session token!"}), 401)

        print(jwt_response)

        return f(jwt_response, *args, **kwargs)

    return decorator


@app.route('/login', methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        auth_request = request.headers['Authorization']
        session_token = auth_request.replace('Bearer ', '') # get the session token

        try:
            jwt_response = descope_client.validate_session(session_token=session_token)
            print(jwt_response)
            return { "status": jwt_response }
        except Exception as error:
            print ("Could not validate user session. Error:")
            print (error)
            return { "error": error }

    return render_template("login.html")


@app.route('/get_secret_message', methods=["GET"])
@token_required
def get_secret_message(jwt_response):
    print(jwt_response)
    return {"secret_msg": "This is the secret message. Congrats!"}

# @app.errorhandler(Exception)
# def not_found(e):
#     return render_template('404.html')

@app.route('/getworkoutdata', methods=['GET', 'POST'])
def get_workout_data():
    global conn
    data = request.get_json()
    workout_info = data['workoutInfo']
    comment = data['comment']
     # Determine the username based on the authentication system being used
    if 'name' in session:  # User is logged in through Google auth
        username = session['name']
    elif current_user.is_authenticated:  # User is logged in through Flask-Login
        print(current_user.is_authenticated)
        username = current_user.username
    else:  # User is not logged in
        username = None
    

    # Store the data in the database
    if username is not None:
        print(username)
        print(workout_info)
        print(comment)

        # Store the data in the database
        print("h1")
        try:
            conncursor = conn.cursor()
            print("h2")
            conncursor.execute('INSERT INTO workouts (username, workout_info, comment) VALUES (?, ?, ?)',  (username, workout_info, comment))
            print('hfiuiue')
            conn.commit()
        except Exception as e:
            print(f"error was {e}")

        
    return 'Data received'


@app.route('/signup', methods=["GET", "POST"])
def signup(): 
    if request.method == "POST":
        auth_request = request.headers['Authorization']
        session_token = auth_request.replace('Bearer ', '') # get the session token

        try:
            jwt_response = descope_client.validate_session(session_token=session_token)
            print(jwt_response)
            return { "status": jwt_response }
        except Exception as error:
            print ("Could not validate user session. Error:")
            print (error)
            return { "error": error }

    return render_template("signup.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

