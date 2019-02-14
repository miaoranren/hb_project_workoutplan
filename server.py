from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Exercise, Image, Equipment, Category, Weight_Unit, Rep_Unit, Workout, User, Workout
# from helper import get_equipment_code

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/register', methods=['GET'])
def register_form():

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register_process():
    username = request.form["username"]
    password = request.form["password"]
    age = int(request.form["age"])
    gender = request.form["gender"]
    
    new_user = User(username=username, password=password, age=age, gender=gender)
    db.session.add(new_user)
    db.session.commit()

    flash(f"User {username} added.")
    return redirect('/')

@app.route('/login', methods=['GET'])
def login_form():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_process():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user.")
        return redirect("/register")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session['user_id'] = user.user_id
    workout_schedule = Workout.query.filter(Workout.user_id == user.user_id).all()

    # print(session['user_id'])
    # print(workout_schedule)

    flash("Logged In")
    return render_template("workout_schedule.html", workout_schedule=workout_schedule, user=user)
    #list

@app.route('/logout')
def logout():
    del session["user_id"] 
    flash("Logged Out.")
    return redirect('/')

@app.route('/create_workout', methods=['POST'])
def add_workout():
    new_workout = Workout(user_id=int(session['user_id']))
    db.session.add(new_workout)
    db.session.commit()
    session['workout_id'] = new_workout.workout_id
    print(new_workout.workout_id)
    return render_template("Searchpage.html")

@app.route('/', methods=['POST'])    

@app.route('/search', methods=['GET']) 
def search():
    equipment_inputs = request.args.getlist("equipment")
    exercises_1 = []
    for equipment_input in equipment_inputs:
        exercises_1 += Exercise.query.filter(Exercise.equipments.any(Equipment.equipment_name == equipment_input)).all()

    exercises_1 = list(set(exercises_1)) # remove duplication

    category_inputs = request.args.getlist("category")
    exercises_2 = []
    for category_input in category_inputs:
        print('input', category_input)
        category_id = Category.query.filter(Category.category_name == category_input).one().category_id
        exercises_2 += Exercise.query.filter(Exercise.category_id == category_id).all()

    exercises_2 = list(set(exercises_2))

    exercises = exercises_1 + exercises_2

    return render_template("exercise_results.html", exercises=exercises)

@app.route('/search/<int:exercise_id>')
def adddetails(exercise_id):
    return render_template("add_detail.html", exercise_id=exercise_id)

@app.route('/addexercises/<int:exercise_id>', methods=['POST'])
def addexercises(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    daysofweek = request.form.get("daysofweek") #later
    numberofsets = request.form.get("numberofsets")
    reps = request.form.get("reps")
    repunit = request.form.get("repunit")
    weights = request.form.get("weights")
    weightunit = request.form.get("weightunit")

    weight_unit_id = Weight_Unit.query.filter(Weight_Unit.weight_unit_name == weightunit).one().weight_unit_id
    repetition_unit = Rep_Unit.query.filter(Rep_Unit.rep_unit_name == repunit).one().rep_unit_id

    workout_created = Workout.query.get(session['workout_id'])
    workout_created.weight_unit_id = weight_unit_id
    workout_created.repetition_unit = repetition_unit
    workout_created.weight = weights
    workout_created.set_number = numberofsets
    workout_created.rep_number = reps

    # new_workout = Workout(weight_unit_id=weight_unit_id, repetition_unit=repetition_unit,
    #                         weight=weights, set_number=numberofsets, rep_number=reps,
    #                         )
    workout_created.exercises.append(exercise)
    db.session.add(workout_created)
    db.session.commit()
    workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()

    return render_template("workout_schedule.html", workout_schedule=workout_schedule)
    #all workout under this user

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
