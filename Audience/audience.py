from flask import Blueprint, render_template

audience_bp = Blueprint('audience', __name__)

@audience_bp.route('/')
def audience():
    return render_template('audience/audience.html')