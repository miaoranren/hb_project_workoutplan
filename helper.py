import requests

# pip install langdetect
from langdetect import detect

equipment = {}
category = {}

def call_api(endpoint):
    base_url = "https://wger.de/api/v2"
    api_url = f'{base_url}/{endpoint}?limit=1000'
    r = requests.get(api_url)
    results = r.json()
    return results['results']

def detect_en(in_str):
    try:
        desc_lang = detect(in_str)
    except:
        return False
    if desc_lang == 'en':
        return True
    return False

def get_equipment_code(endpoint, equipment_input):
    # endpoint = "equipment"
    equipment_result_list = call_api(endpoint)
    equipment = {}
    for result_dict in equipment_result_list:
        code = result_dict['id']
        equipment_name = result_dict['name']
        
        if equipment_name not in equipment:
            equipment[equipment_name] = code
    return equipment[equipment_name]

def get_category_code(endpoint, category_input):
    # endpoint = "equipment"
    category_result_list = call_api(endpoint)
    
    for result_dict in category_result_list:
        code = result_dict['id']
        category_name = result_dict['name']
        
        if category_name not in category:
            category[category_name] = code
    return category[category_input]

def fill_day_work_dictionary(workout_list):
    day_workout_dict = {
                            'Monday': [], 
                            'Tuesday': [], 
                            'Wednesday': [],
                            'Thursday': [],
                            'Friday': [],
                            'Saturday': [],
                            'Sunday': [],
                        }

    for workout in workout_list:
        # get workout day id, append to the corresponding list in day_workout_dict
        for day in workout.scheduled_at_days:
            print(day.day_id)

            if day.day_id == 1:
                day_workout_dict['Monday'].append(workout)
            elif day.day_id == 2:
                day_workout_dict['Tuesday'].append(workout)
            elif day.day_id == 3:
                day_workout_dict['Wednesday'].append(workout)
            elif day.day_id == 4:
                day_workout_dict['Thursday'].append(workout)
            elif day.day_id == 5:
                day_workout_dict['Friday'].append(workout)
            elif day.day_id == 6:
                day_workout_dict['Saturday'].append(workout)
            elif day.day_id == 7:
                day_workout_dict['Sunday'].append(workout)

    return day_workout_dict


# def get_code(equipment_input):
#     equipment[]
# print(get_equipment_code("equipment", "Swiss Ball"))
# print(get_category_code("exercisecategory", "Arms"))
# print(call_api('equipment'))