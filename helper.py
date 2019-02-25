import requests

# pip install langdetect
from langdetect import detect
from datetime import datetime, timedelta

equipment = {}
category = {}

def call_api(endpoint):
    base_url = "https://wger.de/api/v2"
    api_url = f'{base_url}/{endpoint}?limit=1000'
    r = requests.get(api_url)
    results = r.json()
    
    return results['results']

def detect_en(in_str):
    desc_lang = []
    try:
        desc_lang = detect(in_str)
    finally:
        return 'en' in desc_lang

# improve?
# def get_equipment_code(endpoint, equipment_input):
#     # endpoint = "equipment"
#     equipment_result_list = call_api(endpoint)
#     equipment = {}
#     for result_dict in equipment_result_list:
#         code = result_dict['id']
#         equipment_name = result_dict['name']
        
#         if equipment_name not in equipment:
#             equipment[equipment_name] = code
#     return equipment[equipment_name]

# # same
# def get_category_code(endpoint, category_input):
#     # endpoint = "equipment"
#     category_result_list = call_api(endpoint)
    
#     for result_dict in category_result_list:
#         code = result_dict['id']
#         category_name = result_dict['name']
        
#         if category_name not in category:
#             category[category_name] = code
#     return category[category_input]

def fill_day_work_list(workout_list):
    day_workout_list = {}

    # construct days in this week
    days_in_current_week = []
    dt = datetime.today()
    start_day_of_week_monday = dt - timedelta(days=dt.weekday())
    for day_diff in range(7):
        curr_day = start_day_of_week_monday + timedelta(days=day_diff)
        days_in_current_week.append(curr_day.strftime('%Y-%m-%d'))

    for day in days_in_current_week:
        day_workout_list[day] = []

    for workout in workout_list:
        for day in days_in_current_week:
            if workout.scheduled_at == day:
                day_workout_list[day].append(workout)
    return day_workout_list


# def get_code(equipment_input):
#     equipment[]
# print(get_equipment_code("equipment", "Swiss Ball"))
# print(get_category_code("exercisecategory", "Arms"))
# print(call_api('equipment'))