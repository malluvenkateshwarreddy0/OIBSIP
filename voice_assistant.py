import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import os
from urllib.parse import quote

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level

# Initialize speech recognition
recognizer = sr.Recognizer()


def speak(text):
    """Convert text to speech"""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen to microphone input and return recognized text"""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10)
            
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Please try again.")
            return None
        except sr.RequestError:
            speak("Sorry, I'm unable to connect to the internet.")
            return None
    except sr.RequestError:
        speak("Microphone not available. Please check your audio settings.")
        return None


def get_time():
    """Get current time"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")


def get_date():
    """Get current date"""
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {current_date}")


def open_browser(query):
    """Open browser and search"""
    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={quote(query)}")


def open_youtube(query):
    """Search YouTube"""
    speak(f"Opening YouTube and searching for {query}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={quote(query)}")


def calculator(expression):
    """Simple calculator"""
    try:
        result = eval(expression.replace("plus", "+").replace("minus", "-")
                               .replace("times", "*").replace("divided by", "/"))
        speak(f"The answer is {result}")
    except:
        speak("I couldn't calculate that. Please try again.")


def open_application(app_name):
    """Open applications on Windows"""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
    }
    
    if app_name.lower() in apps:
        subprocess.Popen(apps[app_name.lower()])
        speak(f"Opening {app_name}")
    else:
        speak(f"I'm not familiar with {app_name}")


def process_command(command):
    """Process voice commands"""
    if not command:
        return False
    
    # Greetings
    if any(word in command for word in ["hello", "hi", "hey"]):
        speak("Hello! How can I assist you?")
    
    # Time
    elif "time" in command:
        get_time()
    
    # Date
    elif "date" in command:
        get_date()
    
    # Search
    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        if query:
            open_browser(query)
        else:
            speak("What would you like me to search for?")
    
    # YouTube
    elif "youtube" in command or "you tube" in command:
        query = command.replace("youtube", "").replace("you tube", "").strip()
        if query:
            open_youtube(query)
        else:
            speak("What would you like to search on YouTube?")
    
    # Calculator
    elif "calculate" in command or "math" in command:
        query = command.replace("calculate", "").replace("math", "").strip()
        if query:
            calculator(query)
        else:
            speak("What calculation would you like me to do?")
    
    # Open applications
    elif "open" in command:
        app = command.replace("open", "").strip()
        open_application(app)
    
    # Weather
    elif "weather" in command:
        speak("I don't have weather integration yet, but you can search for weather online.")
        open_browser("weather")
    
    # Exit
    elif any(word in command for word in ["exit", "quit", "bye", "goodbye"]):
        speak("Thank you for using the voice assistant. Goodbye!")
        return True
    
    # Help
    elif "help" in command or "commands" in command:
        help_text = """I can help you with:
        - Tell time: Say 'what time is it'
        - Tell date: Say 'what's the date'
        - Search: Say 'search for...' or 'google...'
        - YouTube: Say 'search youtube for...'
        - Calculator: Say 'calculate...'
        - Open apps: Say 'open notepad', 'open calculator', or 'open paint'
        - Exit: Say 'goodbye' or 'exit'"""
        speak(help_text)
        print(help_text)
    
    else:
        speak("I'm not sure how to help with that. Say 'help' to hear my commands.")
    
    return False


def main():
    """Main function to run the voice assistant"""
    speak("Voice Assistant activated. Say 'help' to hear my commands.")
    
    while True:
        command = listen()
        if command and process_command(command):
            break


if __name__ == "__main__":
    main()
