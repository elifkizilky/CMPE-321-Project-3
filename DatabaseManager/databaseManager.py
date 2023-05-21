from flask import Blueprint, render_template

databaseManager_bp = Blueprint('databaseManager', __name__)

@databaseManager_bp.route('/')
def databaseManager():
    return render_template('databaseManager/databaseManager.html')