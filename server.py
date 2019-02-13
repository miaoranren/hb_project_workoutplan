from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Exercise, Image, Equipment, Category
# from helper import get_equipment_code


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("Searchpage.html")

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

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
