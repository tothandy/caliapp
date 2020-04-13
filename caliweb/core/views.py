from caliweb.models import Workout
from flask import render_template, request, Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    own_workouts = Workout.query.order_by(Workout.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', own_workouts=own_workouts)

@core.route('/info')
def info():
    return render_template('info.html')