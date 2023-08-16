from flask import Flask, render_template, request, redirect, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from functools import wraps
import suggest
import pyrebase

app = Flask(__name__)

config = {
    
}

fb = pyrebase.initialize_app(config)
db = fb.database()

# Import the .env file 
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
app.secret_key = env.get("APP_SECRET_KEY")

# Connect the OAuth
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

##### Routes #####

# Create routes for home page when Generate Software or Insights is clicked
@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == 'POST':
        if 'form1' in request.form:
            prompt = request.form['softwareSection']
            software = suggest.generateSoftware(prompt)
            softwareList = software.replace('\n', '<br>')
        if 'form2' in request.form:
            prompt = request.form['insightsSection']
            insights = suggest.generateInsights(prompt)
            insightsList = insights.replace('\n', '<br>')
        if 'save1' in request.form:
            # Create a dictionary of all the software list data to be stored
            s = {
                "id_t": session['id_token'],
                "user_id": session['userinfo']['aud'],
                "email": session['userinfo']['email'],
                "recommendations": software.replace('\n', ' ')
            }
            db.push(s)
        if 'save2' in request.form:
            # Create a dictionary of all the insights list data to be stored
            i = {
                "id_t": session['id_token'],
                "user_id": session['userinfo']['aud'],
                "email": session['userinfo']['email'],
                "insights": insights.replace('\n', ' ')
            }
            db.push(i)
            
    return render_template('index.html', **locals(), session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

# Create the route for logging in using OAuth
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# Create the route for submitting the login using OAuth
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

# Create the route for logging out and returning the to home page using OAuth
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# Render the dashboard page to the /dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

# Render the about page to the /about route
@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
