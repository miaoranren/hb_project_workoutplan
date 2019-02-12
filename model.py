from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

# class Equipment(db.Model):
#     __tablename__ = 'equipments'
#
#     equipment_name = db.Column(db.String(64), nullable=True)
#     equipment_id = db.Column(db.Integer, primary_key=True)

#     exercise = db.relationship("Exercise")

#     def __repr__(self):
#         return f"<{self.equipment_id} : {self.equipment_name}>"

# class Category(db.Model):
#     __tablename__ = 'categories'
#
#     category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     category_code = db.Column(db.Integer,nullable=True)
#     category_name = db.Column(db.String(64), nullable=True)

#     def __repr__(self):
#         return f"<{self.category_code} : {self.category_name}>"

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.workout_id"), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(16), nullable=True)

    workouts = db.relationship("Workout")

    def __repr__(self):
        return f"<User {self.username} - Workout {self.workout_id}>"   

class Exercise(db.Model):
    __tablename__ = 'exercises'

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description =db.Column(db.String(4096), nullable=True)
    equipment = db.Column(db.ARRAY(db.Integer()), nullable=True)
    category = db.Column(db.Integer, nullable=True)

    image = db.relationship("Image")

    def __repr__(self):
        return f"<{self.name} - {self.category} - {self.equipment}>"

class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(300), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)

    def __repr__(self):
        return f"<{self.exercise_id} - {self.image_link}>"

class Workout(db.Model):
    __tablename__ = "workouts"

    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight_unit = db.Column(db.String(64), nullable=True) #helper
    repetition_unit = db.Column(db.String(64), nullable=True) # helper
    weight = db.Column(db.Integer, nullable=True)
    set_number = db.Column(db.Integer, nullable=True)
    rep_number = db.Column(db.Integer, nullable=True)
    priority = db.Column(db.Integer, nullable=False) #####
    schedualed_at = db.Column(db.Integer, nullable=False)

    exercises = db.relationship('Exercise', secondary='workout_exercise', backref='workouts')

    def __repr__(self):
        return f"<{self.workout_id} - {self.exercise_id} - {self.schedualed_at}>"

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'

    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.workout_id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)

    def __repr__(self):
        return f"<{self.workout_id} has {self.exercise_id}>"

# class UserWorkout(db.Model):
#     __tablename__ = 'user_workout'

#     user_workout_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)

#     def __repr__(self):
#         return f"<{self.user_id} - {self.workout_id}>"

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///workoutplan'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")