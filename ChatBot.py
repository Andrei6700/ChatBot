import json
from difflib import get_close_matches
import re
import math

def load_knowledge(file_path: str) -> dict:
    # Function to load knowledge data from the specified JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge(file_path: str, data: dict):
    # Function to save knowledge data to the specified JSON file
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


def chat_bot():
    knowledge_data: dict = load_knowledge("knowledge.json")

    while True:
        user_input: str = input("You: ")
       
        if user_input.lower() == "exit":
            break
    
        best_question_match: str | None = find_best_question_match(user_input, [q["question"] for q in knowledge_data["questions"]])
    
        if best_question_match:
            answer: str = get_answer_for_question(best_question_match, knowledge_data)
            print(f"ChatBot: {answer}")
        elif is_math_question(user_input):
            result = evaluate_math_expression(user_input)
            print(f"ChatBot: {result}")
        else:
            print("ChatBot: I don't know the answer to that question. Tell me the answer ")
            new_answer: str = input("Type the answer or 'skip' to skip: ")

            if new_answer.lower() == "skip":
                continue

            knowledge_data["questions"].append({"question": user_input, "answers": [new_answer]})
            save_knowledge("knowledge.json", knowledge_data)
            print("ChatBot: OK ")

if __name__ == "__main__":
    chat_bot()
