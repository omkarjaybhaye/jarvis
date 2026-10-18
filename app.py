from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import datetime
import wikipedia
import os
import pyautogui
import psutil
import pyjokes
import webbrowser as wb

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests for your HTML frontend

def get_time():
    return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

def get_date():
    now = datetime.datetime.now()
    return f"The current date is {now.day}/{now.month}/{now.year}"

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.get_json()
    query = data.get('command', '').lower()
    response_text = "I didn't quite catch that, sir."

    if 'time' in query:
        response_text = get_time()

    elif 'date' in query:
        response_text = get_date()
    
    elif 'wikipedia' in query:
        query = query.replace("wikipedia","")
        try:
            response_text = wikipedia.summary(query, sentences=2)
        except Exception:
            response_text = "I couldn't find anything relevant on Wikipedia."

    elif 'logout' in query:
        os.system("Shutdown -l")
        response_text = "Logging out, sir."

    elif 'shutdown' in query:
        os.system("Shutdown /s /t 1")
        response_text = "Shutting down the system, sir."

    elif 'restart' in query:
        os.system("Shutdown /r /t 1")
        response_text = "Restarting the system, sir."

    elif 'screenshot' in query:
        img = pyautogui.screenshot()
        img.save("ss.png")
        response_text = "Screenshot taken successfully."

    elif 'cpu' in query:
        usage = str(psutil.cpu_percent())
        battery = psutil.sensors_battery()
        bat_str = f"and battery is at {battery.percent} percent" if battery else ""
        response_text = f"CPU usage is at {usage} percent {bat_str}"

    elif 'joke' in query:
        response_text = pyjokes.get_joke()

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
