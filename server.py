from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Exercise, Image, Equipment, Category, \
    Weight_Unit, Rep_Unit, Workout, User, Workout
from helper import fill_day_work_list

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# @app.route('/register', methods=['GET'])
# def register_form():
#     return render_template("register.html")

@app.route('/register', methods=['POST', 'GET'])
def register_process():
    if request.method == 'POST' and request.form:
        username = request.form["username"]
        password = request.form["password"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        
        new_user = User(username=username, password=password, age=age, gender=gender)
        db.session.add(new_user)
        db.session.commit()

        flash(f"User {username} added.")
        return redirect('/login?r=1')
    else:
        return render_template("register.html")

# @app.route('/login/', methods=['GET'])
# def login_form():
#     return render_template("login.html")

@app.route('/login', methods=['POST', 'GET'])
def login_process():
    if request.method == 'POST' and request.form:
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
        # flash("Logged In")
        return redirect('/dashboard')
    else:
        #r = request.form["registered"] if "registered" in request.form else None
        r = request.args.get("r", False)
        return render_template("login.html", registered=r)

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
    return render_template("choose_day.html")

@app.route('/choose_training_day', methods=['POST'])
def choose_training_day():
    workout_created = Workout.query.get(session['workout_id'])
    daysofweek_input_str = request.form.get("workout-date")
    description = request.form.get("description")

    session['day_id'] = daysofweek_input_str
    workout_created.scheduled_at = daysofweek_input_str
    workout_created.description = description
    print(workout_created.scheduled_at)
    print(workout_created.description)
    db.session.commit()
    return ('', 204)

@app.route('/', methods=['POST'])    

@app.route('/search/<int:exercise_id>')
def adddetails(exercise_id):
    session['exercise_id'] = exercise_id
    return ('', 204)

def add_exercises_helper():
    exercise_id = session['exercise_id']
    print("in addexercises: ", exercise_id)
    exercise = Exercise.query.get(exercise_id)
    numberofsets = request.form.get("numberofsets")
    reps = request.form.get("reps")
    repunit = request.form.get("repunit")
    weights = request.form.get("weights")
    weightunit = request.form.get("weightunit")

    weight_unit_id = Weight_Unit.query.filter(Weight_Unit.weight_unit_name == weightunit).one().weight_unit_id
    repetition_unit = Rep_Unit.query.filter(Rep_Unit.rep_unit_name == repunit).one().rep_unit_id

    exercise.weight_unit_id = weight_unit_id
    exercise.repetition_unit = repetition_unit
    exercise.weight = weights
    exercise.set_number = numberofsets
    exercise.rep_number = reps

    workout_created_before = Workout.query.get(session['workout_id'])
    workout_created_before.exercises.append(exercise)
    db.session.commit()

# @app.route('/addexercises/<int:exercise_id>', methods=['POST'])
# def addexercises(exercise_id):
@app.route('/addexercises', methods=['POST'])
def addexercises():
    add_exercises_helper()
    return ('',204)

@app.route('/addexercises_and_show_dashboard', methods=['POST'])
def addexercises_and_show_dashboard():
    add_exercises_helper()
    workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()
    day_workout_list = fill_day_work_list(workout_schedule)
    return render_template("workout_schedule.html", day_workout_list=day_workout_list, workout_schedule=workout_schedule)

@app.route('/dashboard')
def dashboard():
    workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()
    day_workout_list = fill_day_work_list(workout_schedule)
    return render_template("workout_schedule.html", day_workout_list=day_workout_list, workout_schedule=workout_schedule)

@app.route('/deleteexercises/<int:exercise_id>', methods=['POST'])
def delete_exercise(exercise_id):
    if session["user_id"]:
        exercise_to_delete = Exercise.query.get(exercise_id)
            # print(exercise_to_delete)
        workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()
        day_workout_list = fill_day_work_list(workout_schedule)
        db.session.delete(exercise_to_delete)
        db.session.commit()

        for workout in workout_schedule:
            if not workout.exercises:
                db.session.delete(workout)
                db.session.commit()
       
        return render_template("workout_schedule.html", day_workout_list=day_workout_list, workout_schedule=workout_schedule)
    else:
        return redirect('/')

@app.route('/updateexercises/<int:exercise_id>')
def update_details(exercise_id):
    if session['user_id']:
        exercise_to_update = Exercise.query.get(exercise_id)
    exercise = Exercise.query.get(exercise_id)
    return render_template("add_detail.html", exercise=exercise)

@app.route('/choose_exercises.json')
def get_exercises_result():
    equipment_inputs = request.args.getlist("equipment")
    exercises_1 = []
    for equipment_input in equipment_inputs:
        exercises_1 += Exercise.query.filter(Exercise.equipments.any(Equipment.equipment_name == equipment_input)).all()

    exercises_1 = list(set(exercises_1)) # remove duplication

    category_inputs = request.args.getlist("category")
    exercises_2 = []
    for category_input in category_inputs:
        category_id = Category.query.filter(Category.category_name == category_input).one().category_id
        exercises_2 += Exercise.query.filter(Exercise.category_id == category_id).all()

    exercises_2 = list(set(exercises_2)) # remove duplication

    exercises = []
    if exercises_1 and exercises_2:
        exercises = list(set(exercises_1) & set(exercises_2))
    elif exercises_1:
        exercises = exercises_1
    elif exercises_2:
        exercises = exercises_2

    exercises = sorted(exercises, key=lambda x: x.name)
    exercises_list = [e.serialize() for e in exercises]
    return jsonify(exercises_list)

@app.route('/reschedule_workout', methods=['POST'])
def reschedule_workout():
    workout_id = request.form.get('id')
    workout_to_update = Workout.query.get(workout_id)
    newDate = request.form.get('newDate')
    workout_to_update.scheduled_at = newDate
    db.session.commit()
    return ('', 204)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
