import pyttsx3
import os
import datetime
import speech_recognition as s
import webbrowser
import pyjokes
import requests,json
import scipy.signal
import dateparser

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)         # voices[1]- here 1 is used for female voices and 0 for male voices
engine.setProperty('rate',150)                   # rate is used to regulate the speed of voice ,200 is the default setting

def speak(text):
    engine.say(text)
    engine.runAndWait() 
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else : speak("Good Evening")
def listen():
    recognizer = s.Recognizer()
    with s.Microphone() as source:
        print("LISTENING....")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognizing {command}")
            return command.lower()
        except s.UnknownValueError:
            speak("Sorry, I could not recognize it, Please speak again")
            return ""
        except s.RequestError:
            speak("Failed to execute,Kindly check your network connection")
            return ""

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"Its {current_time}"

def find_joke():
    return pyjokes.get_joke()

def open_website(command):
        website = command.split("open ")[1]
        url = f"https://{website.strip()}.com"
        print(f"Opening {url}...")
        webbrowser.open(url)
        speak(f"Opening {website}")
        
def get_weather(city):
    api_key = "5506651e2ffb3e198de6e247bd2008d2"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}&q={city}&units=metrices&appid={api_key}"
    response = requests.get(complete_url)
    data = response.json()
    main = data['main']
    weather = data['weather'][0]
    temperature = main['temp'] - 273.15
    humidity = main['humidity']
    description = weather['description']
    return f"The temperature in {city} is {temperature:.2f} degrees celsius with {humidity}% humidity and the weather description is described as {description}."
def set_reminder(engine):
    speak("What should I remind you about?")
    reminder = listen()
    
    speak("When do you want to be reminded? Please say the time in hours and minutes.")
    reminder_time = listen()
    reminder_datetime=dateparser.parse(reminder_time)

    try:
        hour, minute = map(int, reminder_time.split())
        now = datetime.datetime.now()
        reminder_datetime = now.replace(hour=hour, minute=minute)

        if now >= reminder_datetime:
            reminder_datetime += datetime.timedelta(days=1)

        speak(engine,f"Alright, I will remind you about '{reminder}' at {reminder_datetime.strftime('%H:%M')}.")
        
        while True:
            if datetime.datetime.now() >= reminder_datetime:
                speak(f"Reminder: {reminder}")
                break
            time.sleep(10)  #checks time in every 10 sec not everytime
    except ValueError:
        speak("Sorry, I couldn't understand the time you provided. Please try again.")
    
def main():
    speak("Hello")
    wishMe()
    speak("I am your Voice assistant. How may I help you")
    while True:
        command = listen()
        if 'time' in command:
            time = get_time()
            speak(time)
        elif 'temperature' in command:
            speak("Can you tell me the city name")
            city_name = listen()
            weather_info = get_weather(city_name)
            speak(weather_info)
        elif 'open' in command:
            speak("sure")
            open_website(command)
        elif 'joke' in command:
            joke = find_joke()
            speak(joke)
        elif 'how are you' in command:
            speak("I am fine, Thank you For asking")
        elif 'reminder' in command:
            set_reminder(engine)
        elif 'what is your name' in command:
            speak("I do not have a name, You can give me one")
        elif 'exit' in command or 'bye' in command:
            speak("Great to help you Goodbye")
            break

if __name__ == "__main__":
    main()
