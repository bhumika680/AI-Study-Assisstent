
import tkinter as tk
from tkinter import ttk, messagebox
from google import genai
import threading

# Main window
root = tk.Tk()
root.title("AI Study Assistant")
root.geometry("850x700")
root.configure(bg="#eef2f7")

# Heading
heading = tk.Label(
    root,
    text="AI STUDY ASSISTANT",
    font=("Arial", 22, "bold"),
    bg="#eef2f7",
    fg="#243b64"
)
heading.pack(pady=15)

# API key
tk.Label(
    root,
    text="Gemini API Key:",
    font=("Arial", 11, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=25)

api_entry = tk.Entry(root, show="*", font=("Arial", 11))
api_entry.pack(fill="x", padx=25, pady=5)

# Task selection
tk.Label(
    root,
    text="Select Task:",
    font=("Arial", 11, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=25, pady=(10, 0))

task_box = ttk.Combobox(
    root,
    values=[
        "Generate Short Notes",
        "Generate Important Questions",
        "Explain in Simple Language",
        "Generate MCQs"
    ],
    state="readonly",
    font=("Arial", 11)
)
task_box.current(0)
task_box.pack(fill="x", padx=25, pady=5)

# Input area
tk.Label(
    root,
    text="Enter Topic or Study Material:",
    font=("Arial", 11, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=25, pady=(10, 0))

input_box = tk.Text(
    root, height=7, wrap="word",
    font=("Arial", 11)
)
input_box.pack(fill="x", padx=25, pady=5)

# Output area
tk.Label(
    root,
    text="AI Generated Result:",
    font=("Arial", 11, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=25, pady=(10, 0))

output_box = tk.Text(
    root, height=12, wrap="word",
    font=("Arial", 11)
)
output_box.pack(fill="both", expand=True, padx=25, pady=5)

status = tk.StringVar(value="Ready")
tk.Label(
    root,
    textvariable=status,
    bg="#eef2f7",
    fg="#243b64"
).pack(anchor="w", padx=25, pady=5)


def generate_content():
    api_key = api_entry.get().strip()
    study_text = input_box.get("1.0", tk.END).strip()
    task = task_box.get()

    if not api_key:
        messagebox.showwarning(
            "Missing API Key",
            "Please enter your Gemini API key."
        )
        return

    if not study_text:
        messagebox.showwarning(
            "Missing Input",
            "Please enter your study material."
        )
        return

    prompts = {
        "Generate Short Notes":
            "Create concise exam-oriented notes with headings and bullet points.",
        "Generate Important Questions":
            "Generate 10 important questions with short answers.",
        "Explain in Simple Language":
            "Explain the topic in simple language with examples.",
        "Generate MCQs":
            "Create 10 MCQs with four options and correct answers."
    }

    prompt = (
        prompts[task]
        + "\nUse the following study material:\n"
        + study_text
    )

    output_box.delete("1.0", tk.END)
    status.set("Generating response...")
    generate_button.config(state="disabled")

    def api_worker():
        try:
            client = genai.Client(api_key=api_key)

            # Find a supported model ID in Google AI Studio
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            result = response.text or "No text response received."

        except Exception as error:
            result = (
                "Unable to generate the response.\n\n"
                "Check your API key, internet connection, "
                "model availability, and usage quota.\n\n"
                f"Details: {error}"
            )

        def finish():
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, result)
            status.set("Completed")
            generate_button.config(state="normal")

        root.after(0, finish)

    threading.Thread(target=api_worker, daemon=True).start()


def copy_result():
    result = output_box.get("1.0", tk.END).strip()

    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo("Success", "Result copied!")


def clear_all():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    status.set("Ready")


# Buttons
button_frame = tk.Frame(root, bg="#eef2f7")
button_frame.pack(pady=12)

generate_button = tk.Button(
    button_frame,
    text="Generate with AI",
    command=generate_content,
    bg="#315a9b",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=6
)
generate_button.pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Copy Result",
    command=copy_result,
    font=("Arial", 10),
    padx=12,
    pady=6
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_all,
    font=("Arial", 10),
    padx=12,
    pady=6
).pack(side="left", padx=5)

root.mainloop()
