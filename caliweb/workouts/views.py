from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from caliweb import db
from caliweb.models import Workout
from caliweb.workouts.forms import WorkoutForm

own_workouts = Blueprint('own_workouts', __name__)

# CREATE
@own_workouts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = WorkoutForm()

    if form.validate_on_submit():
        own_workout = Workout(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id
                            )

        db.session.add(own_workout)
        db.session.commit()
        flash('Workout created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)



# WORKOUT (VIEW)
@own_workouts.route('/<int:own_workout_id>')
def own_workout(own_workout_id):
    own_workout = Workout.query.get_or_404(own_workout_id)
    return render_template('own_workout.html', title=own_workout.title,
                            date=own_workout.date, post=own_workout)

# UPDATE
@own_workouts.route('/<int:own_workout_id>/update', methods=['GET', 'POST'])
@login_required
def update(own_workout_id):
    own_workout = Workout.query.get_or_404(own_workout_id)
    if own_workout.author != current_user:
        #Forbidden access
        abort(403)

    form = WorkoutForm()
    if form.validate_on_submit():
        own_workout.title = form.title.data
        own_workout.text = form.text.data
        db.session.commit()
        flash('Workout Updated')
        return redirect(url_for('own_workouts.own_workout', own_workout_id=own_workout.id))
    # Pass back the old workout information so they can start again with the old text and title
    elif request.method =='GET':
        form.title.data = own_workout.title
        form.text.data = own_workout.text
    return render_template('create_post.html', title='Update', form=form)


# DELETE
@own_workouts.route('/<int:own_workout_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(own_workout_id):
    own_workout = Workout.query.get_or_404(own_workout_id)
    if own_workout.author != current_user:
        #Forbidden access
        abort(403)
    
    db.session.delete(own_workout)
    db.session.commit()
    flash('Workout deleted')
    return redirect(url_for('core.index'))