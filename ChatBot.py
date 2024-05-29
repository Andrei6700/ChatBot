from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from difflib import get_close_matches
import re
import math
from dotenv import load_dotenv 
import os 
from colorama import init, Fore
from datetime import datetime
import requests
from google.cloud import firestore
import google.auth.exceptions

# Load environment variables from .env file
load_dotenv() 

app = Flask(__name__)
CORS(app)
init(autoreset=True)
# Attempt to initialize Firestore client with service account credentials
try:
    db = firestore.Client.from_service_account_json('./serviceAccountKey.json')
except google.auth.exceptions.DefaultCredentialsError:
    print("Failed to initialize Firestore. Please check your credentials.")

# load knoledge from JSON file
def load_knowledge(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# save knowledge data to a JSON file
def save_knowledge(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# find the best match for the user question
def find_best_question_match(user_question: str, questions: list) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# get the answer for a question
def get_answer_for_question(question:str, knowledge: dict) -> str | None:
    for q in knowledge["questions"]:
        if q["question"] == question:
            return q["answers"][0] 

def is_math_question(user_input: str) -> bool:
    return any(char in user_input for char in "+-*/√π0123456789")

def evaluate_math_expression(expression: str) -> str:
    try:
        expression = re.sub(r'(?<![a-zA-Z0-9])sqrt', 'math.sqrt', expression)
        expression = re.sub(r'(?<![a-zA-Z0-9])log', 'math.log', expression)
        result = eval(expression, {"__builtins__": None}, {"math": math})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, list):
            result = ', '.join(str(x) for x in result)
        return str(result)
    except SyntaxError:
        return "Invalid syntax"
    except NameError as e:
        return f"Unsupported function: {e}"
    except ZeroDivisionError:
        return "Division by zero"
    except Exception as e:
        return str(e)

# get the current time in Hour:Min:Sec format
def get_current_time() -> str:
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"The exact time is {current_time}"

# get the current date in YYYY-MM-DD format
def get_current_date() -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"The exact date is {current_date}"

# fetch weather data for a specific city using OpenWeatherMap API
def get_weather(city):
    api_key = "1fb71e32979fe74ad081e6259618a1b4"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        temperature_celsius = temperature - 273.15
        return f"Current weather in {city}: {weather_description}. Temperature: {temperature_celsius:.2f}°C"
    else:
        return "Unable to fetch weather data."

# Load the knowledge data from the JSON file
knowledge_data = load_knowledge("knowledge.json")

# a route for handling questions via POST and GET requests
@app.route('/ask', methods=['POST', 'GET'])
def ask_question():
    global knowledge_data #  knowledge_data as global to save new questions and answers
    if request.method == 'POST':
        user_input = request.json.get('question', '')
        previous_question = request.json.get('previous_question', '')
        print(f"Received POST request with question: {user_input}")
    elif request.method == 'GET':
        user_input = request.args.get('question', '')
        previous_question = request.args.get('previous_question', '')
        print(f"Received GET request with question: {user_input}")

    response = {}

    if previous_question:
        if user_input.lower() != "skip":
            # Save the new question and answer to knowledge_data
            new_entry = {
                "question": previous_question,
                "answers": [user_input]
            }
            knowledge_data["questions"].append(new_entry)
            save_knowledge("knowledge.json", knowledge_data)
            response['answer'] = "Thank you! I have learned something new."
        else:
            response['answer'] = "Question skipped."
    else:
        best_question_match = find_best_question_match(user_input, [q["question"] for q in knowledge_data["questions"]])
        if best_question_match:
            answer = get_answer_for_question(best_question_match, knowledge_data)
            response['answer'] = answer
        elif is_math_question(user_input):
            result = evaluate_math_expression(user_input)
            response['answer'] = result
        elif 'ora' in user_input.lower() and 'cat' in user_input.lower():
            response['answer'] = get_current_time()
        elif 'data' in user_input.lower() or 'zi' in user_input.lower():
            response['answer'] = get_current_date()
        else:
            response['answer'] = "I don't know the answer to that question. Tell me the answer or 'skip' the answer"
            response['unanswered_question'] = user_input

    print(f"Sending response: {response}")
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
