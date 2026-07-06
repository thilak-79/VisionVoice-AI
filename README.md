\# VisionVoice AI



\*\*VisionVoice AI\*\* is a Python-based personal desktop assistant inspired by JARVIS.  

It supports text commands, voice commands, app launching, web search, task memory, camera access, and project automation.



This project is designed as a practical AI/automation portfolio project for learning:



\- Python automation

\- Speech recognition

\- Text-to-speech

\- Computer vision basics

\- SQLite memory storage

\- Human-computer interaction



\---



\## Features



\### Current Features



\- Text command mode

\- Voice command mode

\- Text-to-speech replies

\- Natural language command handling

\- Open desktop applications

&#x20; - Calculator

&#x20; - Notepad

&#x20; - Chrome

&#x20; - VS Code

&#x20; - PowerShell

&#x20; - Command Prompt

\- Google search

\- YouTube search

\- Save tasks/reminders using SQLite

\- Show saved tasks

\- Clear saved tasks

\- Open webcam using OpenCV

\- Launch external projects such as the hand-controlled AR flower project



\---



\## Example Commands



```text

jarvis hello

jarvis what time is it

jarvis tell me the current time

jarvis what is today's date

jarvis open calculator

jarvis launch calculator

jarvis start calculator

jarvis open vs code

jarvis open chrome

jarvis search google for Python tutorial

jarvis search YouTube for OpenCV hand tracking

jarvis remember submit database lab tomorrow

jarvis show tasks

jarvis clear tasks

jarvis open camera

jarvis start flower project

jarvis exit

```



\---



\## Project Architecture



```text

User Command

&#x20;   |

&#x20;   v

Text Mode / Voice Mode

&#x20;   |

&#x20;   v

Command Cleaning and Natural Language Processing

&#x20;   |

&#x20;   v

Intent Detection

&#x20;   |

&#x20;   +--> Open Apps

&#x20;   +--> Search Google

&#x20;   +--> Search YouTube

&#x20;   +--> Save Tasks

&#x20;   +--> Show Tasks

&#x20;   +--> Open Camera

&#x20;   +--> Launch Projects

&#x20;   |

&#x20;   v

Text-to-Speech Response

```



\---



\## Tech Stack



| Component | Technology |

|---|---|

| Programming Language | Python |

| Voice Recognition | SpeechRecognition |

| Text-to-Speech | pyttsx3 |

| Camera Access | OpenCV |

| Memory Storage | SQLite |

| Automation | subprocess, os, webbrowser |

| Interface | Terminal / PowerShell |



\---



\## Project Structure



```text

VisionVoice-AI/

│

├── jarvis.py

├── README.md

├── requirements.txt

├── .gitignore

│

└── jarvis\_memory.db        # Local database, ignored by Git

```



Recommended files to ignore:



```text

venv/

\_\_pycache\_\_/

\*.pyc

.env

jarvis\_memory.db

.vscode/

```



\---



\## Installation



\### 1. Clone the Repository



```bash

git clone https://github.com/thilak-79/VisionVoice-AI.git

cd VisionVoice-AI

```



\### 2. Create Virtual Environment



```bash

python -m venv venv

```



\### 3. Activate Virtual Environment



For Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



For Command Prompt:



```cmd

venv\\Scripts\\activate.bat

```



\### 4. Install Required Packages



```bash

pip install -r requirements.txt

```



If `pyaudio` gives installation errors, install the basic packages first:



```bash

pip install pyttsx3 SpeechRecognition opencv-python

```



Then try:



```bash

pip install pyaudio

```



\---



\## How to Run



```bash

python jarvis.py

```



Then choose a mode:



```text

1\. Text mode

2\. Voice mode

```



For first-time testing, use \*\*Text mode\*\*.



\---



\## Voice Mode



Voice mode allows you to speak commands such as:



```text

Jarvis open calculator

Jarvis what time is it

Jarvis search YouTube for Python tutorial

Jarvis remember finish lab report

```



Make sure your microphone is connected and working.



\---



\## Task Memory



VisionVoice AI uses SQLite to save simple tasks.



Example:



```text

jarvis remember submit CO2050 lab tomorrow

```



Show saved tasks:



```text

jarvis show tasks

```



Clear saved tasks:



```text

jarvis clear tasks

```



The task database is stored locally in:



```text

jarvis\_memory.db

```



This file is ignored by Git to keep personal data private.



\---



\## Camera Mode



Open camera:



```text

jarvis open camera

```



Close the camera window by pressing:



```text

q

```



\---



\## External Project Launcher



VisionVoice AI can launch another Python project, such as a hand-controlled AR flower project.



Example command:



```text

jarvis start flower project

```



In the code, update these paths according to your computer:



```python

FLOWER\_PROJECT\_PATH = r"C:\\Users\\Master\\Music\\flower"

FLOWER\_FILE\_NAME = "start.py"

```



\---



\## Roadmap



Planned improvements:



\- Better natural language understanding

\- AI chatbot integration

\- PDF reading and lecture summarization

\- Local file search

\- Reminder notifications

\- Gesture control using MediaPipe

\- Object detection using YOLO

\- Futuristic desktop dashboard

\- Smart home / IoT control using ESP32

\- User authentication for sensitive commands



\---



\## Future Advanced Version



The final goal is to build a multimodal assistant with:



```text

Voice Input

Text Input

Computer Vision

Local Memory

AI Question Answering

Project Automation

Desktop Control

```



Possible final title:



> VisionVoice AI: A Voice, Vision, and Automation-Based Personal Desktop Assistant



\---



\## Safety Notes



This assistant is intended only for personal productivity and learning.



It should not be used for:



\- Unauthorized access

\- Hidden recording

\- Spying

\- Deleting important files without confirmation

\- Controlling unsafe physical devices



Always add confirmation before dangerous actions such as deleting files or shutting down the computer.



\---



\## Author



\*\*Thilakshan Ravichandran\*\*  

Computer Engineering Undergraduate  

University of Peradeniya



GitHub: \[thilak-79](https://github.com/thilak-79)



\---



\## License



This project is open-source and available for learning and educational use.

