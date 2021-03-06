from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Exercise, ExerciseSetting, Image, Equipment, Category, \
    Weight_Unit, Rep_Unit, Workout, User, Workout
from helper import fill_day_work_list
from datetime import date
import pytz

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


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
        session['username'] = user.username
        
        return redirect('/todaydashboard')
    else:
        
        r = request.args.get("r", False)
        return render_template("login.html", registered=r)

@app.route('/logout')
def logout():
    del session["user_id"]
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
    db.session.commit()
    return ('', 204)

@app.route('/')
def first_page():
    return render_template("first_page.html")    

@app.route('/search/<int:exercise_id>')
def adddetails(exercise_id):
    session['exercise_id'] = exercise_id
    workout_id = request.args.get('workout_id')
    if workout_id:
        session['workout_id'] = workout_id
    return ('', 204)

def add_exercises_helper(new_exercise):
    workout_id = session['workout_id']
    exercise_id = session['exercise_id']
    print("add_exercises_helper:", new_exercise, workout_id, exercise_id)
    current_workout = Workout.query.get(workout_id)
    exercise_setting = None
    if not new_exercise:
        for es in current_workout.exercise_settings:
            if es.exercise_id == exercise_id:
                exercise_setting = es
                break

    # add new exercise setting
    if exercise_setting is None:
        new_es = ExerciseSetting(exercise_id=int(exercise_id))
        current_workout.exercise_settings.append(new_es)
        exercise_setting = current_workout.exercise_settings[-1]

    numberofsets = request.form.get("numberofsets")
    reps = request.form.get("reps")
    repunit = request.form.get("repunit")
    weights = request.form.get("weights")
    weightunit = request.form.get("weightunit")

    weight_unit_id = Weight_Unit.query.filter(Weight_Unit.weight_unit_name == weightunit).one().weight_unit_id
    repetition_unit = Rep_Unit.query.filter(Rep_Unit.rep_unit_name == repunit).one().rep_unit_id

    exercise_setting.weight_unit_id = weight_unit_id
    exercise_setting.repetition_unit = repetition_unit
    exercise_setting.weight = weights
    exercise_setting.set_number = numberofsets
    exercise_setting.rep_number = reps

    db.session.commit()

@app.route('/addexercises', methods=['POST'])
def addexercises():
    add_exercises_helper(True)
    return ('', 204)

@app.route('/addexercises_and_show_dashboard', methods=['POST'])
def addexercises_and_show_dashboard():
    add_exercises_helper(True)
    workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()
    day_workout_list = fill_day_work_list(workout_schedule)
    return render_template("workout_schedule.html", day_workout_list=day_workout_list, workout_schedule=workout_schedule)

@app.route('/dashboard')
def dashboard():
    workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()
    day_workout_list = fill_day_work_list(workout_schedule)
    today_date = date.today()
    print('today', today_date)
    return render_template("workout_schedule.html", day_workout_list=day_workout_list, workout_schedule=workout_schedule, today_date=today_date)

@app.route('/todaydashboard')
def todaydashboard():
    today_date = date.today().strftime('%Y-%m-%d')
    print('today', today_date)
    workout_schedule = Workout.query.filter(Workout.user_id == session['user_id']).all()
    day_workout_list = fill_day_work_list(workout_schedule)
    print(day_workout_list[today_date])
    return render_template("workout_schedule_today.html",  day_workout_list=day_workout_list, workout_schedule=workout_schedule, today_date=today_date)

@app.route('/deleteexercises/<int:es_id>', methods=['POST'])
def delete_exercise(es_id):
    if session["user_id"]:
        workout_id = request.form.get('workout_id')
        workout = Workout.query.get(workout_id)
        for es in workout.exercise_settings:
            if es.exercise_setting_id == es_id:
                db.session.delete(es)
                db.session.commit()
                break

        if not workout.exercise_settings:
            db.session.delete(workout)
            db.session.commit()
        return ('', 204)
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

@app.route('/click_day_details', methods=['GET'])
def click_day_details():
    workout_id = request.args.get('id')
    scheduled_at = request.args.get('date')
    return redirect(f'/click_day_details/{workout_id}')

@app.route('/click_day_details/<int:workout_id>')
def show_details(workout_id):
    workout_to_display = Workout.query.get(workout_id)
    session['workout_id'] = workout_id
    print(workout_to_display)
    return render_template("click_day_details.html", workout=workout_to_display)

@app.route('/addexercises.json/<int:exercise_id>', methods=['POST'])
def update_exercises(exercise_id):
    session['exercise_id'] = exercise_id
    add_exercises_helper(False)
    return ('', 204)

@app.route('/add_more_exercises/<int:workout_id>')
def add_more_exercises(workout_id):
    workout_to_add_more_exercises = Workout.query.get(workout_id)
    session['workout_id'] = workout_id
    print(session['workout_id'])
    return render_template("add_more_exercise.html")

@app.route('/exercises_description.json/<int:exercise_id>')
def exercises_description(exercise_id):
    exercise_to_display = Exercise.query.get(exercise_id)
    exercise_to_display_description = exercise_to_display.description

    return jsonify(exercise_to_display_description)
@app.route('/exercises_name.json/<int:exercise_id>')
def exercises_name(exercise_id):
    exercise_to_display = Exercise.query.get(exercise_id)
    exercise_to_display_name = exercise_to_display.name

    return jsonify(exercise_to_display_name)
 
if __name__ == "__main__":

    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
