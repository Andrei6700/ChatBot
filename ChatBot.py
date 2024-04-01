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

load_dotenv() 
app = Flask(__name__)
CORS(app)
init(autoreset=True)

def load_knowledge(file_path: str) -> dict:
    # Function to load data from json
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge(file_path: str, data: dict):
    # Function to save data to json file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_question_match(user_question: str, questions: list) -> str | None:
    # Function to find the best match for the user's question
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question:str, knowledge: dict) -> str | None:
    # Function to get the answer for the given question from the knowledge data
     for q in knowledge["questions"]:
        if q["question"] == question:
            return q["answers"][0] 

def is_math_question(user_input: str) -> bool:
    # Check if the input contains mathematical characters
    return any(char in user_input for char in "+-*/√π0123456789")

def evaluate_math_expression(expression: str) -> str:
    try:
        # Replace mathematical symbols to make them compatible with eval()
        expression = re.sub(r'(?<![a-zA-Z0-9])sqrt', 'math.sqrt', expression)
        expression = re.sub(r'(?<![a-zA-Z0-9])log', 'math.log', expression)
        
        # Evaluate the mathematical expression
        result = eval(expression, {"__builtins__": None}, {"math": math})
        
        if isinstance(result, float) and result.is_integer():
            # Convert integer results to integer strings
            result = int(result)
        elif isinstance(result, list):
            # Convert list to a single value
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

def get_current_time() -> str:
    current_time = datetime.now().strftime("%H:%M:%S")
    return f" The exact time is {current_time}"

def get_current_date() -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"The exact date is {current_date}"

def get_weather(city):
    api_key = "1fb71e32979fe74ad081e6259618a1b4"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        temperature_celsius = temperature - 273.15  # Convert Kelvin to Celsius
        return f"Current weather in {city}: {weather_description}. Temperature: {temperature_celsius:.2f}°C"
    else:
        return "Unable to fetch weather data."

@app.route('/ask', methods=['POST', 'GET'])
def ask_question():

    decryption_key = os.environ.get('REACT_APP_DECRYPTION_KEY') 
    if request.method == 'POST':
        user_input = request.json.get('question', '')  # take the question from the json

    elif request.method == 'GET':
        user_input = request.args.get('question', '')  # take the question from the url
    
    knowledge_data = load_knowledge("knowledge.json")  # load the knowledge data from the json 
    best_question_match = find_best_question_match(user_input, [q["question"] for q in knowledge_data["questions"]])
    response = {}

    if best_question_match:
        answer = get_answer_for_question(best_question_match, knowledge_data)
        response['answer'] = Fore.RED + answer

    elif is_math_question(user_input):
        result = evaluate_math_expression(user_input)
        response['answer'] = Fore.GREEN + result

    elif 'ora' in user_input.lower() and 'cat' in user_input.lower(): # check if the user asked for the current time
        response['answer'] = Fore.BLUE + get_current_time()

    elif 'data' in user_input.lower() or 'zi' in user_input.lower():
            response['answer'] = Fore.MAGENTA + get_current_date()
    
    else:
        response['answer'] = Fore.LIGHTYELLOW_EX + "I don't know the answer to that question. Tell me the answer or 'skip' the answer"
        response['unanswered_question'] = Fore.BLACK + user_input

    if 'vreme' in user_input.lower() or 'meteo' in user_input.lower():
        # in case the user's request involves the weather, extract the city, it it s specified
        city = 'sibiu'  # Setăm un oraș implicit
        # check if the user specified a city in the question
        # if not, we will use the default city sibiu
        if 'in' in user_input.lower():
            #take the city from the user , using a string between 'in' and 'pe'
            city = user_input.lower().split('in')[1].split('pe')[0].strip()
        elif 'pe' in user_input.lower():
            # take the city using a string after 'pe'
            city = user_input.lower().split('pe')[1].strip()

        # take the meteo
        weather_response = get_weather(city)
        response['answer'] = Fore.YELLOW + weather_response
        
    return jsonify(response)  # return the response in json

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) # start the server 

