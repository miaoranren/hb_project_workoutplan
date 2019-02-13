

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Exercise, Image
from helper import get_equipment_code


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
    # print(equipment_inputs)
    equipment = []
    for equipment_input in equipment_inputs:

        equipment_code = get_equipment_code("equipment", equipment_input)
        equipment.append(equipment_code)
    # equipment_code = get_equipment_code("equipment",equipment_inputs)
    # equipment.append(equipment_code)
    print(equipment)
    exercises = db.session.query(Exercise.equipment == equipment).all()
    # print(exercises)

    return render_template("exercise_results.html", exercises=exercises)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
