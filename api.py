from model import Exercise, Image, Workout, WorkoutExercise, User, connect_to_db, db
from server import app
from helper import call_api, detect_en

def load_exercise():
    exercise_result_list = call_api('exercise')
    valid_exercises_id_list = []

    for result_dict in exercise_result_list:
        language = result_dict['language']

        exercise_id = result_dict['id']
        name = result_dict['name']
        description = result_dict['description']
        equipment_code_list = result_dict['equipment']
        category_code = result_dict['category']

        if (language != 2) or not detect_en(description):
            continue

        exercise = Exercise(exercise_id=exercise_id,
                            name=name,
                            description=description,
                            equipment=equipment_code_list,
                            category=category_code)
        db.session.add(exercise)

        valid_exercises_id_list.append(exercise_id)
    db.session.commit()
    return valid_exercises_id_list

def load_image(valid_exercises_id_list):
    image_result_list = call_api('exerciseimage')
    for result_dict in image_result_list:
        exercise_image = result_dict['image']
        exercise_id = result_dict['exercise']

        if exercise_id not in valid_exercises_id_list:
            continue

        image = Image(image_link=exercise_image, exercise_id=exercise_id)
        db.session.add(image)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # set_val_user_id()
    valid_exercises_id_list = load_exercise()
    print(len(valid_exercises_id_list))
    load_image(valid_exercises_id_list)

    workout_1 = Workout(workout_id=1, priority=1, schedualed_at=1)
    db.session.add(workout_1)
    db.session.commit()

    workout_exercise_1 = WorkoutExercise(table_id=1, workout_id=1, exercise_id=453)
    workout_exercise_2 = WorkoutExercise(table_id=2, workout_id=1, exercise_id=410)
    db.session.add(workout_exercise_1)
    db.session.add(workout_exercise_2)
    db.session.commit()

    user_1 = User(user_id=1, workout_id=1)
    db.session.add(user_1)
    db.session.commit()
