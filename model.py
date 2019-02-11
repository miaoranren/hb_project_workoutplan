from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

# class Equipment(db.Model):
#     __tablename__ = 'equipments'
    
#     equipment_name = db.Column(db.String(64), nullable=True)
#     equipment_id = db.Column(db.Integer, primary_key=True)
#     exercise = db.relationship("Exercise")

#     def __repr__(self):
#         return f"<{equipment_id}:{equipment_name}>"

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_code = db.Column(db.Integer,nullable=True)
    category_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return f"<{category_code}:{category_name}>"

class Exercise(db.Model):
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description =db.Column(db.String(4096), nullable=True)
    equipment = db.Column(db.ARRAY(db.Integer()), nullable=True)
    category = db.Column(db.Integer, nullable=True)

    image = db.relationship("Image")

    def __repr__(self):
        return f"<{name}-{category}-{equipment}>"

class Image(db.Model):
    __tablename__ = "images"
    image_id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(300), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"), nullable=False)

    def __repr__(self):
        return f"<exercise_id - image_link>"


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
    print("Connected to DB.")