from model import Category, Exercise, Image, Workout, Equipment, ExerciseEquipment, WorkoutExercise, User, Rep_Unit, Weight_Unit, Schedule_Day, connect_to_db, db
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
        category_code = result_dict['category']

        # filter out non-English exercises
        if (language != 2) or not detect_en(description):
            continue
        equipment_code_list = result_dict['equipment']
        if not equipment_code_list:
            equipment_code_list = [7]

        # filter out exercises without a name
        if not name:
            continue

        exercise = Exercise(exercise_id=exercise_id,
                            name=name,
                            description=description,
                            equipment=equipment_code_list,
                            category_id=category_code)

        db.session.add(exercise)
        for code in equipment_code_list:
            if Exercise.query.get(exercise_id):
                ee_entry = ExerciseEquipment(exercise_id=exercise_id, equipment_id=code)
                db.session.add(ee_entry)

        db.session.commit()

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

def load_equipment():
    equipment_result_list = call_api('equipment')
    for result_dict in equipment_result_list:
        equipment_id = result_dict['id']
        equipment_name = result_dict['name']
    
        equipment = Equipment(equipment_id=equipment_id, 
                            equipment_name=equipment_name)

        db.session.add(equipment)
    db.session.commit()

def load_category():
    category_result_list = call_api('exercisecategory')
    for result_dict in category_result_list:
        category_id = result_dict['id']
        category_name = result_dict['name']

        category = Category(category_id=category_id,
                            category_name=category_name)
        db.session.add(category)

    db.session.commit()

def load_rep_unit():
    rep_unit_result_list = call_api("setting-repetitionunit")
    for result_dict in rep_unit_result_list:
        rep_unit_id = result_dict['id']
        rep_unit_name = result_dict['name']

        rep_unit = Rep_Unit(rep_unit_id=rep_unit_id,
                            rep_unit_name=rep_unit_name)
        db.session.add(rep_unit)
    db.session.commit()

def load_weight_unit():
    weight_unit_result_list = call_api("setting-weightunit")

    for result_dict in weight_unit_result_list:
        weight_unit_id = result_dict['id']
        weight_unit_name = result_dict['name']

        weight_unit = Weight_Unit(weight_unit_id=weight_unit_id,
                                weight_unit_name=weight_unit_name)
        db.session.add(weight_unit)
    db.session.commit()

def load_days_of_week():
    days_of_week_result_list = call_api("daysofweek")
    for result_dict in days_of_week_result_list:
        day_id = result_dict['id']
        day_of_week = result_dict['day_of_week']

        day_of_week = Schedule_Day(day_id=day_id, day_of_week=day_of_week)

        db.session.add(day_of_week)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # set_val_user_id()
    # valid_exercises_id_list = load_exercise()
    # print(len(valid_exercises_id_list))
    # load_image(valid_exercises_id_list)
    load_category()
    load_equipment()
    load_rep_unit()
    load_weight_unit()
    valid_exercises_id_list = load_exercise()
    print(len(valid_exercises_id_list))
    load_image(valid_exercises_id_list)
    load_days_of_week()
    
    # workout_1 = Workout(workout_id=1, priority=1, scheduled_at=1)
    # db.session.add(workout_1)
    # db.session.commit()

    # 
    # db.session.add(workout_exercise_1)
    # db.session.add(workout_exercise_2)
    # db.session.commit()

    # user_1 = User(user_id=1, workout_id=1)
    # db.session.add(user_1)
    # db.session.commit()
