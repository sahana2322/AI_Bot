import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import random
import openai

# Optional: Set your OpenAI API key here
openai.api_key = "HEY HINATA"  # Replace with your actual key if needed

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    voices = engine.getProperty('voices')
    found = False
    for voice in voices:
        if "jenny" in voice.name.lower():  # Try to set Jenny
            engine.setProperty('voice', voice.id)
            found = True
            break
    if not found:
        for voice in voices:  # Fallback to female-like voice
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Hinata is listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Only wait 3s for you to start, then max 5s recording
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            print("⏳ Processing...")
            command = recognizer.recognize_google(audio)
            print("✅ User said:", command)
            return command.lower().strip()
        except sr.WaitTimeoutError:
            print("⚠️ Timeout: No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio.")
            return ""
        except sr.RequestError:
            print("⚠️ API error, speech service down.")
            speak("Speech service is not available.")
            return ""
        except Exception as e:
            print("⚠️ Unexpected error:", e)
            return ""

def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return answer.strip()
    except Exception as e:
        print("OpenAI error:", e)
        return "Sorry, I could not get an answer right now."

# Quotes list
quotes = [
    "Believe in yourself, and you will be unstoppable.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Your limitation—it’s only your imagination.",
    "Dream it. Wish it. Do it."
]

# Initial waiting state
speak("Hi, I am Hinata. Waiting for your call.")

# Wake-up loop
while True:
    command = listen()
    if "hey hinata" in command or "hi hinata" in command or "hello hinata" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"Yes sir, I am Hinata. The time is {current_time}")
        break

# Main command loop
while True:
    command = listen()

    if not command:  # Skip if nothing detected
        continue

    # --- Time & Date ---
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {current_time}")

    elif "date" in command or "today" in command:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}")

    # --- Web & Apps ---
    elif "open" in command and "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open" in command and "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "search" in command or "find" in command or "look up" in command:
        speak("What should I search for?")
        search_query = listen()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            speak(f"Searching {search_query}")
            webbrowser.open(url)

    elif "open notepad" in command or ("open" in command and "notepad" in command):
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif "open chrome" in command or ("open" in command and "chrome" in command):
        speak("Opening Chrome")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        os.startfile(chrome_path)

    # --- GPT Integration ---
    elif "ask gpt" in command or "question for gpt" in command:
        speak("What is your question?")
        question = listen()
        if question:
            speak("Let me think...")
            answer = ask_gpt(question)
            print("ChatGPT says:", answer)
            speak(answer)

    # --- Motivation & Fun ---
    elif "motivate me" in command or "quote" in command:
        quote = random.choice(quotes)
        speak(quote)

    elif "repeat after me" in command:
        speak("Sure, say the sentence you want me to repeat.")
        sentence = listen()
        if sentence:
            speak(sentence)

    elif "your name" in command or "who are you" in command:
        speak("I am Hinata, your well-wisher and assistant.")

    # --- Exit ---
    elif "stop" in command or "exit" in command or "quit" in command:
        speak("Goodbye sir! Have a great day!")
        break

    # --- Fallback ---
    else:
        speak("I did not understand that. Try again.")
