from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from difflib import get_close_matches
import re
import math

app = Flask(__name__)
CORS(app)

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
    best_match = None
    best_similarity = 0
    
    for q in questions:
        similarity = similarity_score(user_question, q)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = q
    
    return best_match

def similarity_score(str1: str, str2: str) -> float:
    # Function make similarity 
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    
    max_length = max(m, n)
    similarity = 1 - (dp[m][n] / max_length)
    return similarity

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

@app.route('/ask', methods=['POST', 'GET'])
def ask_question():
    if request.method == 'POST':
        user_input = request.json.get('question', '')  # take the question from the json
    elif request.method == 'GET':
        user_input = request.args.get('question', '')  # take the question from the url
    
    knowledge_data = load_knowledge("knowledge.json")  # load the knowledge data from the json 
    best_question_match = find_best_question_match(user_input, [q["question"] for q in knowledge_data["questions"]])
    response = {}
    if best_question_match:
        answer = get_answer_for_question(best_question_match, knowledge_data)
        response['answer'] = answer
    elif is_math_question(user_input):
        result = evaluate_math_expression(user_input)
        response['answer'] = result
    else:
        response['answer'] = "I don't know the answer to that question. Tell me the answer or 'skip' the answer"
        response['unanswered_question'] = user_input
    return jsonify(response)  # return the response in json

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) # start the server 
