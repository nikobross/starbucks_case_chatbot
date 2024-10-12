import nltk
import random
import speech_recognition as sr
import pyttsx3

nltk.download('punkt')
nltk.download('punkt_tab')

# Fake menu for reference
menu = {
    "drinks": ["coffee", "latte", "cappuccino", "espresso", "tea"],
    "sizes": ["small", "medium", "large"],
    "modifications": ["milk", "cream", "sugar", "honey", "ice"]
}

# Conversation states
states = ["order_drink", "order_size", "order_modifications", "payment", "tip", "thanks"]
current_state = "order_drink"

# Order details
order = {
    "drink": None,
    "size": None,
    "modifications": []
}

def generate_response(user_input):
    global current_state, order

    if current_state == "order_drink":
        for drink in menu["drinks"]:
            if drink in user_input.lower():
                order["drink"] = drink
                current_state = "order_size"
                return f"Great choice! What size would you like for your {drink}?"
        return "I'm sorry, we don't have that drink. Please choose from coffee, latte, cappuccino, espresso, or tea."

    elif current_state == "order_size":
        for size in menu["sizes"]:
            if size in user_input.lower():
                order["size"] = size
                current_state = "order_modifications"
                return f"Got it! Would you like any modifications for your {order['size']} {order['drink']}?"
        return "Please choose a size: small, medium, or large."

    elif current_state == "order_modifications":
        for mod in menu["modifications"]:
            if mod in user_input.lower():
                order["modifications"].append(mod)
        current_state = "payment"
        if order['modifications']:
            return f"Alright, your order is a {order['size']} {order['drink']} with {' and '.join(order['modifications'])}. How would you like to pay?"
        else:
            return f"Alright, your order is a {order['size']} {order['drink']}. How would you like to pay?"

    elif current_state == "payment":
        current_state = "tip"
        return "Would you like to add a tip?"

    elif current_state == "tip":
        current_state = "thanks"
        return "Thank you for your order! Your drink will be ready shortly."

    elif current_state == "thanks":
        return "Goodbye!"

def chat():
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()
    
    print("Chatbot: Welcome to Starbucks! What drink would you like to order?")
    tts_engine.say("Welcome to Starbucks! What drink would you like to order?")
    tts_engine.runAndWait()
    
    while True:
        with sr.Microphone() as source:
            print("You: ", end="")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                print(user_input)
                if user_input.lower() == 'exit':
                    print("Chatbot: Goodbye!")
                    tts_engine.say("Goodbye!")
                    tts_engine.runAndWait()
                    break
                response = generate_response(user_input)
                print(f"Chatbot: {response}")
                tts_engine.say(response)
                tts_engine.runAndWait()
                if current_state == "thanks":
                    break
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                tts_engine.say("Sorry, I did not understand that.")
                tts_engine.runAndWait()
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                tts_engine.say(f"Could not request results; {e}")
                tts_engine.runAndWait()

if __name__ == "__main__":
    chat()