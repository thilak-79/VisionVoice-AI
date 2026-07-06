import os
import re
import sqlite3
import datetime
import subprocess
import webbrowser

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

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

USE_AI_BRAIN = True
AI_PROVIDER = "openrouter"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "700"))
AI_MAX_SPEAK_CHARS = 700


# -----------------------------
# NATURAL LANGUAGE WORD GROUPS
# -----------------------------

OPEN_WORDS = [
    "open", "launch", "start", "run", "execute", "turn on", "bring up"
]

TIME_WORDS = [
    "time", "clock", "current time"
]

DATE_WORDS = [
    "date", "day", "today"
]

REMEMBER_WORDS = [
    "remember", "save", "note", "note down", "add task", "add a task",
    "create task", "store", "keep in memory"
]

SHOW_TASK_WORDS = [
    "show tasks", "list tasks", "display tasks", "read tasks",
    "what are my tasks", "show my tasks", "list my tasks",
    "show reminders", "list reminders", "show memory", "what did you remember"
]

CLEAR_TASK_WORDS = [
    "clear tasks", "delete tasks", "remove tasks", "clear all tasks",
    "delete all tasks", "clear memory", "delete memory"
]

EXIT_WORDS = [
    "exit", "quit", "stop", "shutdown", "close jarvis", "bye", "goodbye"
]

HELP_WORDS = [
    "help", "what can you do", "commands", "show commands", "how can you help"
]

AI_TRIGGER_WORDS = [
    "explain",
    "teach",
    "what is",
    "what are",
    "how to",
    "how do",
    "why",
    "write",
    "generate",
    "give me",
    "solve",
    "summarize",
    "compare",
    "difference between",
    "idea",
    "project idea",
    "answer",
    "describe",
    "define",
    "make",
    "create"
]

APP_ALIASES = {
    "notepad": ["notepad", "text editor"],
    "calculator": ["calculator", "calc"],
    "chrome": ["chrome", "google chrome", "browser"],
    "vs code": ["vs code", "visual studio code", "vscode", "code editor"],
    "cmd": ["cmd", "command prompt"],
    "powershell": ["powershell", "terminal"],
    "camera": ["camera", "webcam"],
}



# -----------------------------
# TEXT TO SPEECH
# -----------------------------

VOICE_ENABLED = True


def speak(text):
    """
    Stable JARVIS voice output.
    This creates a fresh pyttsx3 engine each time to avoid silent voice issues.
    """
    print(f"JARVIS: {text}")

    if not VOICE_ENABLED:
        return

    if pyttsx3 is None:
        print("pyttsx3 is not installed. Voice output disabled.")
        return

    try:
        engine = pyttsx3.init("sapi5")  # Windows speech engine

        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")

        # Prefer common Windows English voices
        if voices:
            selected_voice = None

            for voice in voices:
                name = voice.name.lower()
                if "david" in name or "zira" in name:
                    selected_voice = voice.id
                    break

            if selected_voice is None:
                selected_voice = voices[0].id

            engine.setProperty("voice", selected_voice)

        engine.say(str(text))
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Text-to-speech error:", e)

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
# NATURAL LANGUAGE HELPERS
# -----------------------------

def normalize_text(text):
    text = text.lower().strip()

    for symbol in ["?", ".", ",", "!", ";", ":"]:
        text = text.replace(symbol, " ")

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_command(command):
    command = normalize_text(command)

    if command.startswith(WAKE_WORD):
        command = command.replace(WAKE_WORD, "", 1).strip()

    polite_words = [
        "please",
        "can you",
        "could you",
        "would you",
        "for me",
        "now",
        "just",
        "kindly"
    ]

    for word in polite_words:
        command = command.replace(word, " ")

    command = re.sub(r"\s+", " ", command)
    return command.strip()


def contains_phrase(command, phrase):
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, command) is not None


def contains_any(command, words):
    return any(contains_phrase(command, word) for word in words)


def is_exit_command(command):
    return command in EXIT_WORDS or contains_any(command, EXIT_WORDS)


def is_help_command(command):
    return contains_any(command, HELP_WORDS)


def is_greeting(command):
    greetings = [
        "hello", "hi", "hey", "good morning", "good afternoon",
        "good evening", "are you there"
    ]
    return contains_any(command, greetings)


def is_time_command(command):
    if "time complexity" in command:
        return False

    time_phrases = [
        "time",
        "current time",
        "what time",
        "tell me time",
        "clock"
    ]

    return contains_any(command, time_phrases)


def is_date_command(command):
    return contains_any(command, DATE_WORDS)


def is_open_intent(command):
    return contains_any(command, OPEN_WORDS)


def detect_app(command):
    for app_name, aliases in APP_ALIASES.items():
        for alias in aliases:
            if contains_phrase(command, alias):
                return app_name

    return None


def remove_words(text, words):
    for word in words:
        text = text.replace(word, " ")

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_google_query(command):
    remove_list = [
        "search google for", "search on google for", "search in google for",
        "google search for", "google for", "search for", "look up",
        "find", "search", "google", "on google", "in google"
    ]

    query = remove_words(command, remove_list)
    return query.strip()


def extract_youtube_query(command):
    remove_list = [
        "search youtube for", "search on youtube for", "search in youtube for",
        "youtube search for", "search yt for", "yt search for",
        "youtube", "yt", "search for", "search", "look up", "find",
        "on youtube", "in youtube"
    ]

    query = remove_words(command, remove_list)
    return query.strip()


def extract_task_text(command):
    remove_list = [
        "remember that", "remember to", "remember",
        "save that", "save this", "save",
        "note down that", "note down", "note that", "note",
        "add a task to", "add task to", "add a task", "add task",
        "create a task", "create task",
        "store that", "store this", "store",
        "keep in memory that", "keep in memory"
    ]

    task = remove_words(command, remove_list)
    return task.strip()


def is_show_tasks_command(command):
    return contains_any(command, SHOW_TASK_WORDS)


def is_clear_tasks_command(command):
    return contains_any(command, CLEAR_TASK_WORDS)


def is_remember_command(command):
    return contains_any(command, REMEMBER_WORDS)


def is_camera_command(command):
    if "camera" in command or "webcam" in command:
        if is_open_intent(command) or contains_any(command, ["look", "show"]):
            return True

    if command in ["camera", "webcam"]:
        return True

    return False


def is_flower_project_command(command):
    has_flower = (
        "flower" in command
        or "hand flower" in command
        or "gesture flower" in command
    )

    has_project = (
        "project" in command
        or "program" in command
        or "app" in command
    )

    if has_flower and (is_open_intent(command) or has_project):
        return True

    return False


def is_youtube_search(command):
    return contains_any(command, ["youtube", "yt"])


def is_google_search(command):
    if contains_phrase(command, "google"):
        return True

    search_phrases = [
        "search for",
        "search about",
        "look up",
        "find about"
    ]

    return contains_any(command, search_phrases)


def is_ai_command(command):
    return contains_any(command, AI_TRIGGER_WORDS)


# -----------------------------
# APP / SYSTEM ACTIONS
# -----------------------------

def open_app(app_name):
    app_name = app_name.lower()

    try:
        if app_name == "notepad":
            subprocess.Popen("notepad")
            speak("Opening Notepad.")

        elif app_name == "calculator":
            subprocess.Popen("calc")
            speak("Opening Calculator.")

        elif app_name == "chrome":
            subprocess.Popen("start chrome", shell=True)
            speak("Opening Chrome.")

        elif app_name == "vs code":
            subprocess.Popen("code", shell=True)
            speak("Opening Visual Studio Code.")

        elif app_name == "cmd":
            subprocess.Popen("start cmd", shell=True)
            speak("Opening Command Prompt.")

        elif app_name == "powershell":
            subprocess.Popen("start powershell", shell=True)
            speak("Opening PowerShell.")

        elif app_name == "camera":
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
            ["powershell", "-NoExit", "-Command", command]
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
# OPENROUTER AI BRAIN
# -----------------------------

def ask_ai_brain(user_question):
    if OpenAI is None:
        speak("OpenAI package is not installed. Run pip install openai.")
        return

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        speak("OpenRouter API key was not found. Please add it to your .env file.")
        return

    try:
        speak("Thinking...")

        client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/thilak-79/VisionVoice-AI",
                "X-OpenRouter-Title": "VisionVoice AI"
            }
        )

        system_prompt = """
You are VisionVoice AI, a helpful desktop assistant for a Computer Engineering undergraduate.

Rules:
- Answer clearly and simply.
- Use step-by-step explanations for programming, databases, computer architecture, electronics, AI, ML, and computer vision.
- Keep answers short unless the user asks for a detailed explanation.
- Do not claim you opened apps, changed files, sent emails, or controlled the computer unless the Python program actually executed that action.
- When the user asks for code, provide clean and runnable code.
"""

        response = client.chat.completions.create(
           model=OPENROUTER_MODEL,
           messages=[
               {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ],
            temperature=0.4,
            max_tokens=OPENROUTER_MAX_TOKENS
)

        answer = response.choices[0].message.content.strip()

        print("\nAI ANSWER:")
        print(answer)
        print()

        if answer:
            speak(answer[:AI_MAX_SPEAK_CHARS])
        else:
            speak("I received an empty answer from the AI model.")

    except Exception as e:
        error_text = str(e).lower()

        if "no auth credentials" in error_text or "401" in error_text or "unauthorized" in error_text:
            speak("Your OpenRouter API key is missing or invalid. Please check your .env file.")
        elif "insufficient" in error_text or "credits" in error_text or "402" in error_text:
            speak("Your OpenRouter credits may be finished. Please check your OpenRouter account.")
        elif "rate" in error_text or "429" in error_text:
            speak("The OpenRouter rate limit was reached. Please wait and try again.")
        elif "model" in error_text and "not" in error_text:
            speak("The selected OpenRouter model is not available. Please change OPENROUTER_MODEL in your .env file.")
        else:
            speak("I could not connect to OpenRouter. Check your API key, internet connection, model name, and credits.")

        print(e)


# -----------------------------
# COMMAND BRAIN
# -----------------------------

def process_command(raw_command):
    command = clean_command(raw_command)

    if command == "":
        return True

    print(f"Processing: {command}")

    # Exit
    if is_exit_command(command):
        speak("Shutting down. Goodbye.")
        return False

    # Help
    if is_help_command(command):
        show_help()
        return True

    # Greetings
    if is_greeting(command):
        speak("Hello. I am ready.")
        return True

    # Camera
    if is_camera_command(command):
        open_camera()
        return True

    # Flower project
    if is_flower_project_command(command):
        start_flower_project()
        return True

    # Time and date
    if is_time_command(command):
        tell_time()
        return True

    if is_date_command(command):
        tell_date()
        return True

    # Remember task
    if is_remember_command(command):
        task = extract_task_text(command)

        if task == "":
            speak("What should I remember?")
        else:
            remember_task(task)
            speak("I remembered that.")

        return True

    # Show tasks
    if is_show_tasks_command(command):
        tasks = get_tasks()

        if not tasks:
            speak("You have no saved tasks.")
        else:
            speak(f"You have {len(tasks)} saved tasks.")
            for task_id, task, created_at in tasks:
                print(f"{task_id}. {task}  [{created_at}]")

        return True

    # Clear tasks
    if is_clear_tasks_command(command):
        clear_tasks()
        speak("All tasks cleared.")
        return True

    # YouTube search
    if is_youtube_search(command):
        query = extract_youtube_query(command)
        search_youtube(query)
        return True

    # Google search
    if is_google_search(command):
        query = extract_google_query(command)
        search_google(query)
        return True

    # Open apps naturally
    if is_open_intent(command):
        app_name = detect_app(command)

        if app_name:
            open_app(app_name)
        else:
            speak("Which app should I open?")

        return True

    # AI brain commands
    if USE_AI_BRAIN and is_ai_command(command):
        ask_ai_brain(command)
        return True

    # Direct app names
    app_name = detect_app(command)
    if app_name:
        speak(f"Do you want me to open {app_name}? Say open {app_name}.")
        return True

    # Fallback
    if USE_AI_BRAIN:
        ask_ai_brain(command)
    else:
        speak("I do not understand that command yet.")

    return True


def show_help():
    print("""
Natural commands you can try:

1. jarvis hello
2. jarvis what time is it
3. jarvis tell me the current time
4. jarvis what is today's date
5. jarvis open calculator
6. jarvis launch calculator
7. jarvis start calculator
8. jarvis run calculator
9. jarvis please open vs code
10. jarvis can you launch chrome for me
11. jarvis open notepad
12. jarvis open powershell
13. jarvis open command prompt
14. jarvis open camera
15. jarvis look at camera
16. jarvis start flower project
17. jarvis run my hand flower project
18. jarvis google Python tutorial
19. jarvis search google for OpenCV hand tracking
20. jarvis search YouTube for MediaPipe hand tracking
21. jarvis remember submit database lab tomorrow
22. jarvis note down finish computer architecture report
23. jarvis save buy bread
24. jarvis show tasks
25. jarvis what are my tasks
26. jarvis clear tasks
27. jarvis explain Dijkstra algorithm
28. jarvis write SQL query for students table
29. jarvis give me computer vision project ideas
30. jarvis what can you do
31. jarvis exit
""")

    speak("I printed the natural command list.")


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