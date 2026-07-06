# VisionVoice AI

<p align="center">
  <b>A Python-based voice, vision, and automation desktop assistant inspired by JARVIS.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green" />
  <img src="https://img.shields.io/badge/SQLite-Memory-lightgrey" />
  <img src="https://img.shields.io/badge/Status-In%20Development-orange" />
</p>

---

## Overview

**VisionVoice AI** is a personal desktop assistant built with Python.  
It can understand text or voice commands, open applications, search the web, remember tasks, access the camera, and launch other projects.

This project is developed as a practical AI/automation portfolio project focusing on:

- Voice-based human-computer interaction
- Desktop automation
- Task memory using SQLite
- Basic computer vision integration
- Natural language command handling

---

## Features

| Feature | Status |
|---|---|
| Text command mode | Done |
| Voice command mode | Done |
| Text-to-speech replies | Done |
| Open desktop apps | Done |
| Google search | Done |
| YouTube search | Done |
| Task memory using SQLite | Done |
| Show and clear saved tasks | Done |
| Camera access using OpenCV | Done |
| Launch external Python projects | Done |
| AI chatbot integration | Planned |
| PDF summarizer | Planned |
| GUI dashboard | Planned |

---

## Example Commands

```text
jarvis hello
jarvis what time is it
jarvis what is today's date
jarvis open calculator
jarvis launch chrome
jarvis open vs code
jarvis search google for Python tutorial
jarvis search YouTube for OpenCV hand tracking
jarvis remember submit database lab tomorrow
jarvis show tasks
jarvis clear tasks
jarvis open camera
jarvis start flower project
jarvis exit
```

---

## Project Architecture

```text
User Input
   |
   |-- Text Command
   |-- Voice Command
   |
   v
Command Processing
   |
   v
Natural Language Intent Detection
   |
   |-- Open Application
   |-- Search Web
   |-- Save Task
   |-- Show Tasks
   |-- Open Camera
   |-- Launch Project
   |
   v
Text-to-Speech Response
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Speech Recognition | SpeechRecognition |
| Text-to-Speech | pyttsx3 |
| Computer Vision | OpenCV |
| Database | SQLite |
| Automation | subprocess, os, webbrowser |
| Interface | Terminal / PowerShell |

---

## Project Structure

```text
VisionVoice-AI/
│
├── jarvis.py
├── README.md
├── requirements.txt
├── .gitignore
└── jarvis_memory.db    # Local database, ignored by Git
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/thilak-79/VisionVoice-AI.git
cd VisionVoice-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If PyAudio gives an error, install the basic packages first:

```bash
pip install pyttsx3 SpeechRecognition opencv-python
```

---

## How to Run

```bash
python jarvis.py
```

Then select a mode:

```text
1. Text mode
2. Voice mode
```

For first-time testing, use **Text mode**.

---

## Main Functions

### App Launcher

VisionVoice AI can open common desktop applications:

```text
jarvis open calculator
jarvis open notepad
jarvis open chrome
jarvis open vs code
jarvis open powershell
```

### Web Search

```text
jarvis search google for Python tutorial
jarvis search YouTube for MediaPipe hand tracking
```

### Task Memory

```text
jarvis remember submit lab tomorrow
jarvis show tasks
jarvis clear tasks
```

Tasks are saved locally using SQLite.

### Camera Mode

```text
jarvis open camera
```

Press `q` to close the camera window.

### Project Launcher

VisionVoice AI can launch other Python projects.

Example:

```text
jarvis start flower project
```

Update the project path inside `jarvis.py`:

```python
FLOWER_PROJECT_PATH = r"C:\Users\Master\Music\flower"
FLOWER_FILE_NAME = "start.py"
```

---

## Roadmap

Future improvements:

- Add AI chatbot responses
- Add PDF reading and summarization
- Add local file search
- Add reminder notifications
- Add GUI dashboard
- Add object detection using YOLO
- Add hand gesture control using MediaPipe
- Add smart home / IoT control
- Add user authentication for sensitive commands

---

## Safety Notes

This assistant is designed for personal productivity and learning.

It should not be used for:

- Unauthorized access
- Hidden recording
- Spying
- Deleting important files without confirmation
- Unsafe device control

Dangerous actions should always ask for confirmation first.

---

## Author

**Thilakshan Ravichandran**  
Computer Engineering Undergraduate  
University of Peradeniya  

GitHub: [thilak-79](https://github.com/thilak-79)

---

## License

This project is open-source and available for educational and learning purposes.