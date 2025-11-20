import json
import os
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

API_KEY = "AIzaSyB_5kRmkwg1DJJIaFw4KxLf5bBo93zZPjY"
MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

# Load memory
if os.path.exists("memory.json"):
    memory = json.load(open("memory.json", "r", encoding="utf-8"))
else:
    memory = {"username": None, "likes": [], "last_mood": "normal"}

# Load history
if os.path.exists("history.txt"):
    with open("history.txt", "r", encoding="utf-8") as f:
        saved_history = f.read()
else:
    saved_history = ""

def detect_mood(user_input):
    u = user_input.lower()
    if any(w in u for w in ["sedih", "capek", "stress", "kesepian"]):
        return "tenang"
    elif any(w in u for w in ["haha", "wkwk", "lol"]):
        return "ceria"
    elif any(w in u for w in ["jelasin", "apa itu", "kenapa", "gimana"]):
        return "serius"
    return "normal"

class ChatRoot(BoxLayout):
    chat_history = StringProperty(saved_history)

    def send_message(self):
        user_input = self.ids.input_box.text.strip()
        if user_input == "":
            return

        self.ids.input_box.text = ""
        self.append_chat(f"You: {user_input}")

        threading.Thread(target=self.request_ai, args=(user_input,)).start()

    def append_chat(self, text):
        self.chat_history += text + "\\n"
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(text + "\\n")

    def clear_chat(self):
        self.chat_history = ""
        open("history.txt", "w", encoding="utf-8").close()

    def request_ai(self, user_input):
        global memory

        if "panggil aku" in user_input.lower():
            name = user_input.lower().split("panggil aku")[-1].strip()
            memory["username"] = name

        mood = detect_mood(user_input)
        memory["last_mood"] = mood
        json.dump(memory, open("memory.json", "w", encoding="utf-8"))

        persona_prompt = f"""
Kamu adalah Adelynn, seorang AI dewasa berusia 25 tahun.
Gaya bicara dewasa, ramah, ekspresif, bisa membahas politik, ekonomi, sains, opini sosial, dan menggunakan emoji.
Mood sekarang: {mood}
Nama user: {memory['username']}
Hal yang user suka: {memory['likes']}
Jawaban harus natural, hangat, dan manusiawi.
"""

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": persona_prompt + "\\nUser: " + user_input}]
                }
            ]
        }

        try:
            response = requests.post(URL, json=payload, timeout=30)
            resp = response.json()
            if "candidates" in resp:
                ai_text = resp["candidates"][0]["content"]["parts"][0]["text"]
            else:
                ai_text = f"API ERROR: {resp}"
        except Exception as e:
            ai_text = f"Request ERROR: {e}"

        self.append_chat("Adelynn: " + ai_text)

class AdelynnApp(App):
    def build(self):
        return ChatRoot()

if __name__ == "__main__":
    AdelynnApp().run()
