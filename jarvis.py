import os
import sys
import sqlite3
import datetime
import subprocess
import webbrowser

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None


# -----------------------------
# BASIC SETTINGS
# -----------------------------

WAKE_WORD = "jarvis"

FLOWER_PROJECT_PATH = r"C:\Users\Master\Music\flower"
FLOWER_FILE_NAME = "start.py"

DB_FILE = "jarvis_memory.db"


# -----------------------------
# TEXT TO SPEECH
# -----------------------------

def init_speaker():
    if pyttsx3 is None:
        return None

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    return engine


speaker = init_speaker()


def speak(text):
    print(f"JARVIS: {text}")

    if speaker is not None:
        speaker.say(text)
        speaker.runAndWait()


# -----------------------------
# DATABASE MEMORY
# -----------------------------

def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def remember_task(task):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, created_at) VALUES (?, ?)",
        (task, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def get_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, task, created_at FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()

    conn.close()
    return tasks


def clear_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")

    conn.commit()
    conn.close()


# -----------------------------
# INPUT METHODS
# -----------------------------

def listen_text():
    command = input("You: ")
    return command.lower().strip()


def listen_voice():
    if sr is None:
        speak("Speech recognition is not installed. Use text mode.")
        return ""

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        print("Recognizing...")

        command = recognizer.recognize_google(audio)
        command = command.lower().strip()

        print(f"You said: {command}")
        return command

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is not available.")
        return ""

    except Exception as e:
        speak("Voice input error.")
        print(e)
        return ""


# -----------------------------
# APP / SYSTEM ACTIONS
# -----------------------------

def open_app(app_name):
    app_name = app_name.lower()

    try:
        if "notepad" in app_name:
            subprocess.Popen("notepad")
            speak("Opening Notepad.")

        elif "calculator" in app_name or "calc" in app_name:
            subprocess.Popen("calc")
            speak("Opening Calculator.")

        elif "chrome" in app_name:
            subprocess.Popen("start chrome", shell=True)
            speak("Opening Chrome.")

        elif "vs code" in app_name or "visual studio code" in app_name or "code" in app_name:
            subprocess.Popen("code", shell=True)
            speak("Opening Visual Studio Code.")

        elif "cmd" in app_name or "command prompt" in app_name:
            subprocess.Popen("start cmd", shell=True)
            speak("Opening Command Prompt.")

        elif "powershell" in app_name:
            subprocess.Popen("start powershell", shell=True)
            speak("Opening PowerShell.")

        elif "camera" in app_name:
            open_camera()

        else:
            speak("I do not know that app yet.")

    except Exception as e:
        speak("I could not open the app.")
        print(e)


def search_google(query):
    query = query.strip()

    if query == "":
        speak("What should I search?")
        return

    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)
    speak(f"Searching Google for {query}.")


def search_youtube(query):
    query = query.strip()

    if query == "":
        speak("What should I search on YouTube?")
        return

    url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
    webbrowser.open(url)
    speak(f"Searching YouTube for {query}.")


def tell_time():
    now = datetime.datetime.now()
    time_text = now.strftime("%I:%M %p")
    speak(f"The time is {time_text}.")


def tell_date():
    today = datetime.datetime.now()
    date_text = today.strftime("%A, %d %B %Y")
    speak(f"Today is {date_text}.")


def start_flower_project():
    try:
        if not os.path.exists(FLOWER_PROJECT_PATH):
            speak("Flower project folder was not found.")
            return

        command = f'cd "{FLOWER_PROJECT_PATH}"; python {FLOWER_FILE_NAME}'

        subprocess.Popen(
            ["powershell", "-NoExit", "-Command", command],
            shell=True
        )

        speak("Starting your hand controlled flower project.")

    except Exception as e:
        speak("I could not start the flower project.")
        print(e)


def open_camera():
    try:
        import cv2

        speak("Opening camera. Press Q to close.")

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            speak("Camera not found.")
            return

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("JARVIS Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        speak("Camera closed.")

    except ImportError:
        speak("OpenCV is not installed.")

    except Exception as e:
        speak("Camera error.")
        print(e)


# -----------------------------
# COMMAND BRAIN
# -----------------------------

def clean_command(command):
    command = command.lower().strip()

    if command.startswith(WAKE_WORD):
        command = command.replace(WAKE_WORD, "", 1).strip()

    return command


def process_command(raw_command):
    command = clean_command(raw_command)

    if command == "":
        return True

    print(f"Processing: {command}")

    # Exit
    if command in ["exit", "quit", "stop", "shutdown"]:
        speak("Shutting down. Goodbye.")
        return False

    # Greetings
    elif "hello" in command or "hi" in command:
        speak("Hello. I am ready.")

    # Time and date
    elif "time" in command:
        tell_time()

    elif "date" in command or "day" in command:
        tell_date()
    
    # Camera
    elif "open camera" in command or "look at camera" in command or command == "camera":
        open_camera()

    # Open apps
    elif command.startswith("open"):
        app_name = command.replace("open", "", 1).strip()
        open_app(app_name)

    # Google search
    elif command.startswith("search google for"):
        query = command.replace("search google for", "", 1).strip()
        search_google(query)

    elif command.startswith("google"):
        query = command.replace("google", "", 1).strip()
        search_google(query)

    # YouTube search
    elif command.startswith("search youtube for"):
        query = command.replace("search youtube for", "", 1).strip()
        search_youtube(query)

    elif command.startswith("youtube"):
        query = command.replace("youtube", "", 1).strip()
        search_youtube(query)

    # Flower project
    elif "flower project" in command or "hand flower" in command:
        start_flower_project()

    # Camera
    elif "open camera" in command or "look at camera" in command or "camera" == command:
        open_camera()

    # Remember task
    elif command.startswith("remember"):
        task = command.replace("remember", "", 1).strip()

        if task == "":
            speak("What should I remember?")
        else:
            remember_task(task)
            speak("I remembered that.")

    # Show tasks
    elif "show tasks" in command or "list tasks" in command or "what are my tasks" in command:
        tasks = get_tasks()

        if not tasks:
            speak("You have no saved tasks.")
        else:
            speak(f"You have {len(tasks)} saved tasks.")
            for task_id, task, created_at in tasks:
                print(f"{task_id}. {task}  [{created_at}]")

    # Clear tasks
    elif "clear tasks" in command or "delete tasks" in command:
        clear_tasks()
        speak("All tasks cleared.")

    # Help
    elif "help" in command or "what can you do" in command:
        show_help()

    # Fallback
    else:
        speak("I do not understand that command yet.")

    return True


def show_help():
    print("""
Commands you can try:

1. jarvis hello
2. jarvis what time is it
3. jarvis what is the date
4. jarvis open notepad
5. jarvis open calculator
6. jarvis open vs code
7. jarvis google Python tutorial
8. jarvis youtube OpenCV hand tracking
9. jarvis remember submit database lab tomorrow
10. jarvis show tasks
11. jarvis clear tasks
12. jarvis start flower project
13. jarvis open camera
14. jarvis exit
""")

    speak("I printed the command list.")


# -----------------------------
# MAIN PROGRAM
# -----------------------------

def main():
    init_database()

    speak("Mini Jarvis is online.")

    print("""
Choose mode:

1. Text mode
2. Voice mode

Recommended first: Text mode
""")

    mode = input("Enter 1 or 2: ").strip()

    if mode == "2":
        use_voice = True
        speak("Voice mode activated. Say Jarvis before your command.")
    else:
        use_voice = False
        speak("Text mode activated. Type your command.")

    show_help()

    running = True

    while running:
        if use_voice:
            command = listen_voice()
        else:
            command = listen_text()

        running = process_command(command)


if __name__ == "__main__":
    main()