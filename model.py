from flask_sqlalchemy import SQLAlchemy 



db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(64), nullable=True)

    exercises = db.relationship("Exercise", backref="categories")

    def __repr__(self):
        return f"<{self.category_code} : {self.category_name}>"

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(16), nullable=True)

    def __repr__(self):
        return f"<User {self.username} - Workout {self.workout_id}>"   

class Exercise(db.Model):
    __tablename__ = 'exercises'

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description =db.Column(db.String(4096), nullable=True)
    equipment = db.Column(db.ARRAY(db.Integer()), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=True)
    weight_unit_id = db.Column(db.Integer, db.ForeignKey("weight_unit.weight_unit_id"),nullable=True) 
    repetition_unit = db.Column(db.Integer, db.ForeignKey("rep_unit.rep_unit_id"), nullable=True) 
    weight = db.Column(db.Integer, nullable=True)
    set_number = db.Column(db.Integer, nullable=True)
    rep_number = db.Column(db.Integer, nullable=True)
    priority = db.Column(db.Integer, nullable=True) 

    images = db.relationship("Image",cascade="all,delete")
    equipments = db.relationship("Equipment", secondary="exercise_equipment", backref="exercises")
    weight_unit = db.relationship("Weight_Unit")
    rep_unit = db.relationship("Rep_Unit")

    def __repr__(self):
        return f"<{self.name} - {self.category_id} - {self.equipment}-{self.images}>"

    def serialize(self):
        return {'exercise_id': self.exercise_id,
                'name': self.name,
                'description': self.description,
                'equipment': self.equipment}

class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(300), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)

    def __repr__(self):
        return f"<{self.exercise_id} - {self.image_link}>"

class Equipment(db.Model):
    __tablename__ = "equipments"

    equipment_id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<{equipment_id} - {equipment_name}>"

class ExerciseEquipment(db.Model):
    __tablename__ = "exercise_equipment"

    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipments.equipment_id"), nullable=False)

    def __repr__(self):
        return f"<{self.exercise_id}> - <{self.equipment_id}>"

class Workout(db.Model):
    __tablename__ = "workouts"

    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    scheduled_at = db.Column(db.String(10))
    description = db.Column(db.String(30))

    exercises = db.relationship('Exercise', secondary='workout_exercise', backref='workouts')
    users = db.relationship('User', backref="workouts")
    # scheduled_at_days = db.relationship('Schedule_Day', secondary='scheduledday_workout', backref='workouts')

    def __repr__(self):
        return f"<Workout id: {self.workout_id} - User id: {self.user_id} - scheduled_at: {self.scheduled_at} - exercises: {self.exercises}>"

    def serialize(self):
        return {
            'workout_id' :self.workout_id,
            'scheduled_at': self.scheduled_at
        }

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'

    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.workout_id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)

    def __repr__(self):
        return f"<{self.workout_id} has {self.exercise_id}>"

class Weight_Unit(db.Model):
    __tablename__ = 'weight_unit'

    weight_unit_id = db.Column(db.Integer, primary_key=True)
    weight_unit_name = db.Column(db.String(128))

    def __repr__(self):
        return f"<{self.weight_unit_id} - {self.weight_unit_name}>"

class Rep_Unit(db.Model):
    __tablename__ = "rep_unit"

    rep_unit_id = db.Column(db.Integer, primary_key=True)
    rep_unit_name = db.Column(db.String(128))

    def __repr__(self):
        return f"<{self.rep_unit_id} - {self.rep_unit_name}>"


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
