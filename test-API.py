import requests
from ChatBot import load_knowledge, save_knowledge

API_URL = 'http://127.0.0.1:5000/ask'

def ask_question(question):
    response = requests.post(API_URL, json={'question': question})
    return response.json()

    
def main():
    print("pune intrebarea :")
    while True:
        user_input = input("Tu: ")
        if user_input.lower() == 'exit':
            break
        response = ask_question(user_input)
        if isinstance(response, dict):  # Verificăm dacă răspunsul este un dicționar JSON
            print("ChatBot:", response.get('answer', ''))
            if 'unanswered_question' in response:
                print("ChatBot: Te rog să-mi spui răspunsul corect pentru întrebarea:", response['unanswered_question'])
                user_response = input("Tu: ")
                if user_response.strip().lower() != 'skip':
                    # Aici ar trebui să salvezi răspunsul utilizatorului în cunoștințele tale și să reiei bucla de întrebare
                    knowledge_data = load_knowledge("knowledge.json")
                    knowledge_data["questions"].append({"question": response['unanswered_question'], "answers": [user_response]})
                    save_knowledge("knowledge.json", knowledge_data)
                    print("ChatBot: Am adăugat răspunsul tău în cunoștințele mele.")
        else:
            print("ChatBot:", response)


if __name__ == "__main__":
    main()
