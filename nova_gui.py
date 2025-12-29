import tkinter as tk
import threading
import speech_recognition as sr
from main import processCommand, speak  

recognizer = sr.Recognizer()

# ---------- THEMES ----------
LIGHT_THEME = {
    "bg": "#ffffff",
    "text": "#000000",
    "chat_bg": "#F2F3F7",
    "input_bg": "#EDEEF2",
    "send_btn_bg": "#1E941C",
    "listen_btn_bg": "#15306F",
    "exit_btn_bg": "#d51414",
    "status_fg": "#1E941C"
}

DARK_THEME = {
    "bg": "#000000",
    "text": "#FFFFFF",
    "chat_bg": "#121212",
    "input_bg": "#1E1E1E",
    "send_btn_bg": "#1E941C",
    "listen_btn_bg": "#15306F",
    "exit_btn_bg": "#d51414",
    "status_fg": "#1E941C"
}

current_theme = "dark"

# -------- Voice Listening Function --------
def listen():
    status_label.config(text="Listening...")  

    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        command = recognizer.recognize_google(audio)
        chat_box.insert(tk.END, f"You: {command}\n")  
        chat_box.see(tk.END)

        response = processCommand(command)

        if response == "EXIT":
            speak("Goodbye. Have a great day.")
            root.destroy()
            return

        if response:
            chat_box.insert(tk.END, f"NOVA: {response}\n")
            chat_box.see(tk.END)
            speak(response)

    except:
        chat_box.insert(tk.END, "NOVA: Sorry, I couldn't understand.\n")
        speak("Sorry, I couldn't understand")

    status_label.config(text="Idle")


# -------- Text Input Handler --------
def handle_text_command():
    command = text_entry.get()  

    if command.strip():
        chat_box.insert(tk.END, f"USER: {command}\n")
        chat_box.see(tk.END)

        response = processCommand(command)

        if response == "EXIT":
            speak("Goodbye. Have a great day.")
            root.destroy()
            return

        if response:
            chat_box.insert(tk.END, f"NOVA: {response}\n")
            chat_box.see(tk.END)
            speak(response)

        text_entry.delete(0, tk.END) 
        

# -------- Thread Wrapper --------
def start_listening(): 
    threading.Thread(target=listen).start()

# -------- Toggle Theme --------
def toggle_theme():
    global current_theme

    if current_theme == "dark":
        apply_theme(LIGHT_THEME)
        current_theme = "light"
        theme_btn.config(text = "🌙 Dark Mode")

    else:
        apply_theme(DARK_THEME)
        current_theme = "dark"
        theme_btn.config(text = "☀ Light Mode")


def apply_theme(theme):
    root.config(bg=theme["bg"])

    header.config(bg=theme["bg"], fg=theme["text"])
    sub_header.config(bg=theme["bg"], fg=theme["text"])

    chat_box.config(
    bg=theme["chat_bg"],
    fg=theme["text"],
    insertbackground=theme["text"]
    )

    input_frame.config(bg=theme["input_bg"])
    send_btn.config(bg=theme["send_btn_bg"], fg=theme["text"])

    text_entry.config(
    bg=theme["text"],
    fg=theme["bg"],
    insertbackground=theme["bg"]
    )       

    btn_frame.config(bg=theme["bg"])
    listen_btn.config(bg=theme["listen_btn_bg"], fg=theme["text"])
    exit_btn.config(bg=theme["exit_btn_bg"], fg=theme["text"])

    status_label.config(bg=theme["bg"], fg=theme["status_fg"])


# Creates the main application window
root = tk.Tk()


# -------- GUI Setup --------
root.title("NOVA - Virtual Assistant")  
root.update_idletasks()  
x = (root.winfo_screenwidth() // 2) - (1100 // 2)  
y = (root.winfo_screenheight() // 2) - (700 // 2) - 30
root.geometry(f"1100x700+{x}+{y}") 
root.config(bg="#000000") 

# Header
header = tk.Label(
    root,
    text="NOVA",
    font=("Segoe UI", 35, "bold"),
    fg="#ffffff",
    bg="#000000"
)
header.pack(pady=(15, 5))  

sub_header = tk.Label(
    root,
    text="Your Voice & Text Assistant",
    font=("Segoe UI", 12),
    fg="#ffffff",
    bg="#000000"
)
sub_header.pack(pady=(0, 10))

# Chat Box
chat_box = tk.Text(
    root,
    height=16,
    width=100,
    font=("Consolas", 11),
    bg="#FFFFFF",
    fg="#2C2C54",
    wrap=tk.WORD,  
    bd=0,
    padx=20,  
    pady=20
)
chat_box.pack(padx=10, pady=10)
chat_box.config(state=tk.NORMAL) 
chat_box.insert(tk.END, "NOVA: Hello! Click 'Start Listening' to begin.\n")

# Text like chat gpt(input area)
input_frame = tk.Frame(root, bg="#F5F6FA")
input_frame.pack(pady=5)

text_entry = tk.Entry(
    input_frame,
    width=48,
    font=("Segoe UI", 11),
    bd=1,
    relief=tk.FLAT
)
text_entry.pack(side=tk.LEFT, padx=(5))

send_btn = tk.Button(  # Creates a clickable button
    input_frame,
    text="Send",
    command=handle_text_command,
    bg="#1E941C",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief=tk.FLAT,
    padx=15
)
send_btn.pack(side=tk.LEFT)

# buttons 
btn_frame = tk.Frame(root, bg="#000000")
btn_frame.pack(pady=10)

listen_btn = tk.Button(
    btn_frame,
    text="🎙 Start Listening",
    command=start_listening,
    bg="#15306F",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief=tk.FLAT,
    padx=20
)
listen_btn.pack(side=tk.LEFT, padx=5)

exit_btn = tk.Button(
    btn_frame,
    text="Exit",
    command=root.destroy,  
    bg="#d51414",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief=tk.FLAT,
    padx=20
)
exit_btn.pack(side=tk.LEFT, padx=5)

theme_btn = tk.Button(
    root,
    text="☀ Light Mode",
    command=toggle_theme,
    bg="#444444",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief=tk.FLAT,
    padx=20
)
theme_btn.pack(pady=5)

status_label = tk.Label(root, text="Idle", fg="green")
status_label.pack()

speak("Initializing Nova...")
apply_theme(DARK_THEME)

# main loop
root.mainloop()

