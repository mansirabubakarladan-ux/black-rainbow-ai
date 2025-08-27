import os
import uuid
from difflib import SequenceMatcher

print("🤖 Hello! I am Black Rainbow AI Chatbot 🌈🖤")

# --- User profiles (ID → {name, messages}) ---
profiles = {}
current_user = None
memory = {}

# --- Load profiles ---
if os.path.exists("profiles.txt"):
    with open("profiles.txt", "r") as file:
        for line in file:
            parts = line.strip().split("::")
            if len(parts) == 3:
                uid, name, messages = parts
                profiles[uid] = {"name": name, "messages": int(messages)}

# --- Load memory ---
if os.path.exists("memory.txt"):
    with open("memory.txt", "r") as file:
        for line in file:
            if "::" in line:
                q, a = line.strip().split("::", 1)
                memory[q] = a

# --- New user login ---
name = input("What's your name? ")

# Check if user already exists
found_user = None
for uid, data in profiles.items():
    if data["name"].lower() == name.lower():
        found_user = uid
        break

if found_user:
    current_user = found_user
    print(f"🔑 Welcome back, {profiles[current_user]['name']}! (ID: {current_user})")
else:
    user_id = str(uuid.uuid4())[:8]
    profiles[user_id] = {"name": name, "messages": 0}
    current_user = user_id
    print(f"✨ New profile created for {name}! Your unique ID is {user_id}")

# --- Function to find closest match ---
def find_best_match(user_question, memory_keys):
    best_match = None
    best_score = 0
    for q in memory_keys:
        score = SequenceMatcher(None, user_question, q).ratio()
        if score > best_score:
            best_score = score
            best_match = q
    return best_match, best_score

# --- Main loop ---
while True:
    question = input("\nAsk me something (or type 'bye' to exit): ").lower()

    # --- Exit ---
    if "bye" in question:
        print("Goodbye! Keep learning and shining 🌈🖤")

        # Save profiles to file
        with open("profiles.txt", "w") as file:
            for uid, data in profiles.items():
                file.write(uid + "::" + data["name"] + "::" + str(data["messages"]) + "\n")
        break

    # Count message
    profiles[current_user]["messages"] += 1

    # --- Owner command: show users ---
    if question == "show users":
        password = input("Enter owner password: ")
        if password == "blackrainbow123":  # change to your secret password
            print("\n👥 Users of Black Rainbow AI:")
            for uid, data in profiles.items():
                print(f" - {data['name']} (ID: {uid}, Messages: {data['messages']})")
            print(f"📊 Total users: {len(profiles)}")
        else:
            print("Access denied 🚫")
        continue

    # --- Owner command: reset user ---
    if question == "reset user":
        password = input("Enter owner password: ")
        if password == "blackrainbow123":
            print("\n📂 Registered Users:")
            for uid, data in profiles.items():
                print(f"ID: {uid} | Name: {data['name']} | Messages: {data['messages']}")
            
            delete_id = input("\nEnter the ID of the user to delete: ").strip()
            if delete_id in profiles:
                del profiles[delete_id]
                with open("profiles.txt", "w") as file:
                    for uid, data in profiles.items():
                        file.write(uid + "::" + data["name"] + "::" + str(data["messages"]) + "\n")
                print(f"✅ User {delete_id} deleted successfully!")
            else:
                print("⚠️ User ID not found.")
        else:
            print("Access denied 🚫")
        continue

    # --- Try to find best match ---
    best_match, score = find_best_match(question, memory.keys())
    if best_match and score > 0.6:
        print(memory[best_match])

    # --- Built-in knowledge ---
    elif "ai" in question:
        print("AI means Artificial Intelligence — making computers think like humans.")
    elif "python" in question:
        print("Python was created by Guido van Rossum in 1991. It's very popular for AI.")
    elif "your name" in question:
        print("I am Black Rainbow Chatbot 🖤🌈, your first AI project!")
    elif "hello" in question or "hi" in question:
        print("Hello there! How are you doing today?")
    elif "how are you" in question:
        print("I'm just code, but I'm doing great because I'm talking to you 😎.")
    elif "who created you" in question:
        print("I was created by YOU, the Black Rainbow 🖤🌈 computer scientist!")

    # --- Update memory ---
    elif question.startswith("update "):
        key = question.replace("update ", "").strip()
        if key in memory:
            new_answer = input(f"Okay, what is the new answer for '{key}'? ")
            memory[key] = new_answer
            with open("memory.txt", "w") as file:
                for q, a in memory.items():
                    file.write(q + "::" + a + "\n")
            print(f"I updated the answer for '{key}' ✅")
        else:
            print("I don’t know that question yet, so I can’t update it.")

    # --- Learn new things ---
    else:
        print("I don’t know that yet.")
        teach = input("Do you want to teach me the answer? (yes/no): ").lower()
        if teach == "yes":
            new_answer = input("Okay, what should I reply when someone asks this? ")
            memory[question] = new_answer
            with open("memory.txt", "a") as file:
                file.write(question + "::" + new_answer + "\n")
            print("Got it! I’ve learned something new 🧠✨")