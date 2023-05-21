from flask import Flask, redirect
from .DatabaseManager.databaseManager import databaseManager_bp
from .Login.login import login_bp
from .Director.director import director_bp
from .Audience.audience import audience_bp
from .config import Config

app = Flask(__name__)
app.secret_key = Config.API_KEY
# Register blueprints
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(databaseManager_bp, url_prefix='/databaseManager')
app.register_blueprint(audience_bp, url_prefix='/audience')
app.register_blueprint(director_bp, url_prefix='/director')

# Redirect root URL to '/login'
@app.route('/')
def root():
    return redirect('/login')

if __name__ == '__main__':
    app.run()