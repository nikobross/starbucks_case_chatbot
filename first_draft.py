import nltk
import random
import speech_recognition as sr
import pyttsx3

nltk.download('punkt')
nltk.download('punkt_tab')

responses = {
    "order": [
        "What type of drink would you like?",
        "What size would you like?",
        "Would you like that hot or iced?",
        "Would you like that with milk or cream?",
        "Would you like that sweetened?"
    ],
    "payment": [
        "How are you paying today?",
        "Tap card here.",
        "Would you like to add a tip?",
        "Would you like to donate change to Doctors without Borders?"
    ],
    "thanks": [
        "Your drink is coming right up!",
        "Thanks for the tip!",
        "Thank you for your order!"
    ]
}

context = "order"
asked_questions = set()

def generate_response(user_input):
    global context, asked_questions
    if context == "order":
        if len(asked_questions) == len(responses["order"]):
            context = "payment"
            asked_questions.clear()
        else:
            available_questions = [q for q in responses["order"] if q not in asked_questions]
            response = random.choice(available_questions)
            asked_questions.add(response)
            return response
    elif context == "payment":
        if "pay" in user_input.lower() or "tip" in user_input.lower():
            context = "thanks"
        response = random.choice(responses[context])
        return response
    elif context == "thanks":
        response = random.choice(responses[context])
        return response

def chat():
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()
    
    print("Chatbot: Welcome to Starbucks! How can I help you today?")
    tts_engine.say("Welcome to Starbucks! How can I help you today?")
    tts_engine.runAndWait()
    
    last_response = ""
    
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
                while response == last_response:
                    response = generate_response(user_input)
                last_response = response
                print(f"Chatbot: {response}")
                tts_engine.say(response)
                tts_engine.runAndWait()
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