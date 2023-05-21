from flask import Blueprint, render_template

director_bp = Blueprint('director', __name__)

@director_bp.route('/')
def director():
    return render_template('director/director.html')