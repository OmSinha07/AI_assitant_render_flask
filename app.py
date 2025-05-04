from flask import Flask, render_template, request, jsonify
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os

app = Flask(__name__)
memory = ""
# Speak function - no threading, fresh engine each time
def speak(text):
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[SPEAK ERROR]: {e}")

# Music dictionary
music = {
    "winning": "https://youtu.be/vsWxs1tuwDk?si=wZm2jEzOZitN6U-K",
    "allah": "https://youtu.be/ri3NctAmkWE?si=E7XsMi0McoRqHIul",
    "soni": "https://youtu.be/GFljvZMZI0U?si=pZ3Dt6C5pco8ufAX",
    "aao": "https://youtu.be/Mo5tQDcs__g?si=QC6BWCkSOJGURxyf",
    "gangland": "https://youtu.be/QgHbp2c66FI?si=1ry-lbkKZdNej_It",
    "obstacles": "https://youtu.be/O4N4RhbvvKM?si=8U_E6Y9jWLQ9EBR8",
    "people": "https://youtu.be/mj0XInqZMHY?si=sudSzvuHZGeYHVXi"
}

# Greet user
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    message = f"{greeting}. Hello! I am North, your AI assistant."
    speak(message)
    return message

# First time flag
first_use = True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    global first_use
    query = request.json.get("query", "").lower()
    full_response = ""
#1. First use pe wish krega
    if first_use:
        full_response += wish_me() + "\n"
        first_use = False



#3.Opening yt
    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")
        speak("opening you tube")
        full_response += "Opening YouTube"




#4.Open Insta
    elif 'open instagram' in query:
        webbrowser.open("https://instagram.com")
        speak("opening instagram")
        full_response += "Opening Instagram"




#5.Open Goolge
    elif 'open google' in query:
        webbrowser.open("https://google.com")
        speak("opening Google")
        full_response += "Opening Google"


#6.To check time

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        time_msg = f"The time is {strTime}"
        speak(time_msg)
        full_response += time_msg

#7.To check weather
 
    elif 'weather' in query:
        city = query.replace("weather", "").strip() or "Delhi"
        weather_url = f"https://wttr.in/{city}?format=%t"
        try:
            import requests
            import re

            temp = requests.get(weather_url).text.strip()
            temp_clean = re.search(r'-?\d+', temp)
            temp_number = temp_clean.group() if temp_clean else "unknown"

            response = f"The temperature in {city} is {temp_number}°C"
            speak(f"{temp_number} degrees")
            full_response += f"\nWeather: {temp_number}°C"

        except:
            response = "Sorry, I couldn't fetch the weather."
            speak(response)
            full_response += f"\n{response}"

    


#8.To play on youtube  
    elif 'play on youtube' in query:
        parts = query.split("play", 1)
        if len(parts) > 1:
            song = parts[1].strip()
            if song:
                speak(f"Playing {song} on YouTube")
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
                full_response += f"Playing {song} on YouTube"
            else:
                speak("Please say the song name after play")
                full_response += "Please say the song name after play"
        else:
            speak("Please say the song name after play")
            full_response += "Please say the song name after play"
    
    

#9.To search on google
    elif 'search on google' in query:
        import wikipedia
        search_query = query.replace("search on google", "").strip()
        if search_query:
            speak(f"Searching {search_query} on Google")

            try:
                summary = wikipedia.summary(search_query, sentences=2)
                speak(summary)
                full_response += f"Summary for {search_query}: {summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results. Please be more specific.")
                full_response += "Disambiguation error."
            except:
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(url)
                speak(f"I couldn't find a summary, but here are Google search results for {search_query}")
                full_response += f"Opened Google search for {search_query}"
  
#10.To see time and date 
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {strTime}")
        full_response += f"Time: {strTime}"

    elif 'date' in query:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {today}")
        full_response += f"Date: {today}"



#11.To ccheck news
    elif 'news' in query:
        speak("Fetching the latest news headlines...")
        try:
            import feedparser
            news_feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
            for entry in news_feed.entries[:5]:
                speak(entry.title)
                full_response += entry.title + "\n"
        except:
            speak("Sorry, I couldn't fetch the news.")


# 12.To tell joke 
    elif 'joke' in query:
        import pyjokes
        joke = pyjokes.get_joke()
        speak(joke)
        full_response += joke



# 13.To remember
    elif 'remember that' in query:
        memory = query.replace('remember that', '').strip()
        if memory:
            speak(f"You asked me to remember: {memory}")
            with open("memory.txt", "w") as file:
                file.write(memory)
        else:
            speak("What should I remember?")
    elif 'what do you remember' in query:
        try:
            with open("memory.txt", "r") as file:
                memory = file.read()
            response = f"You asked me to remember: {memory}"
            speak(response)
            print(response)  # Show on console
            full_response += response
        except FileNotFoundError:
            response = "I don't remember anything yet."
            speak(response)
            print(response)
            full_response += response



#14.To add to my to do list 
    elif 'add to my ' in query:
        task = query.replace('add to my to-do list', '').strip()
        if not task:
            speak("What task should I add?")
            task = takeCommand()  # assumes you have a voice input function
        if task:
            with open("todo.txt", "a") as file:
                file.write(task + "\n")
            response = f"I've added '{task}' to your to-do list."
            speak(response)
            full_response += response + "\n"
        else:
            response = "I didn't catch any task."
            speak(response)
            full_response += response + "\n"

    elif "what's on " in query:
        try:
            with open("todo.txt", "r") as file:
                tasks = file.readlines()
            if tasks:
                speak("Here are your tasks:")
                full_response += "Your To-Do List:\n"
                for i, task in enumerate(tasks, start=1):
                    task_line = f"Task {i}: {task.strip()}"
                    speak(task_line)
                    full_response += task_line + "\n"
            else:
                response = "Your to-do list is empty."
                speak(response)
                full_response += response + "\n"
        except FileNotFoundError:
            response = "You don't have a to-do list yet."
            speak(response)
            full_response += response + "\n"

    elif 'clear my to-do list' in query:
        open("todo.txt", "w").close()
        response = "Your to-do list has been cleared."
        speak(response)
        full_response += response + "\n"

    elif 'delete task number' in query:
        import re
        match = re.search(r'delete task number (\d+)', query)
        if match:
            task_num = int(match.group(1))
            try:
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()
                if 0 < task_num <= len(tasks):
                    deleted = tasks.pop(task_num - 1)
                    with open("todo.txt", "w") as file:
                        file.writelines(tasks)
                    response = f"Deleted task {task_num}: {deleted.strip()}"
                    speak(response)
                    full_response += response + "\n"
                else:
                    response = "Invalid task number."
                    speak(response)
                    full_response += response + "\n"
            except FileNotFoundError:
                response = "You don't have a to-do list yet."
                speak(response)
                full_response += response + "\n"
        else:
            response = "Please tell me which task number to delete."
            speak(response)
            full_response += response + "\n"

        


                
#15.For shuting down 
    elif 'shut up' in query:
        msg = "Hope I have helped you"
        speak(msg)
        full_response += "Shutting down"


# 16.To play fav song yt
    elif 'play' in query:
        parts = query.split()
        if len(parts) > 1:
            song = parts[1]
            link = music.get(song)
            if link:
                webbrowser.open(link)
                full_response += f"Playing {song}"
            else:
                full_response += "Song not found"
        else:
            full_response += "Please say the song name after play"

#Sorry i dont understand
    else:
        msg = "Sorry, I didn't understand that."
        speak(msg)
        full_response += "Command not recognized"

    return jsonify(response=full_response)

if __name__ == "__main__":
    app.run(debug=True)
