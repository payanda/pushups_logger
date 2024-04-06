from flask import Flask,Blueprint, render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, current_user
from . import db
from .models import Users, Workouts

# create a bluepring by then name of main
main = Blueprint("main", __name__)

# default page or route
@main.route("/")
def index():
    return render_template("index.html")

# route for seeing profile
@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

'''------------------------------- For CREATING the Workouts -------------------------------'''
# GET method
@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')
# POST method
@main.route("/new", methods=['POST'])
@login_required
def new_workout_post():
    pushup = request.form.get("pushup")
    comment = request.form.get("comment")
    workout = Workouts(pushup=pushup, comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()
    
    # show a message that workout has been added 
    flash("Your Workout added Successfully!")
    return redirect(url_for('main.user_workouts'))


'''------------------------------- For SHOWING The Workouts -------------------------------'''
@main.route("/all")
@login_required
def user_workouts():
    page = request.args.get('page', 1,type=int)
    user = Users.query.filter_by(email=current_user.email).first_or_404()
    # show 5 workout per page in website
    workouts = Workouts.query.filter_by(author=user).paginate(page=page, per_page=5)
    return render_template('all_workouts.html', workouts=workouts, user=user)


'''------------------------------- For UPDATING The Workouts -------------------------------'''
@main.route("/workout/<int:workout_id>/update", methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    # get the workout
    workout = Workouts.query.get_or_404(workout_id)
    
    # for POST method get information and update to the database
    if request.method == 'POST':
        workout.pushup = request.form.get('pushup')
        workout.comment = request.form.get('comment')
        db.session.commit()
        flash("Your workout Updated!")
        return redirect(url_for('main.user_workouts'))
    
    # for GET method just show the update form 
    return render_template('update_workout.html',workout_id=workout_id)


'''------------------------------- For DELETING The Workouts -------------------------------'''
@main.route("/workout/<int:workout_id>/delete")
@login_required
def delete_workout(workout_id):
    # get the workout
    workout = Workouts.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash("Your Workout has benn deleted!")
    return redirect(url_for('main.user_workouts'))