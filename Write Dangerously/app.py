import tkinter as tk
from tkinter import filedialog
import time

class WriteOrDie:
    def __init__(self, master):
        self.master = master
        self.master.title("Write or Die")

        self.text_area = tk.Text(master, wrap='word', font=("Helvetica", 14))
        self.text_area.pack(expand=1, fill='both')

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        self.start_button = tk.Button(button_frame, text="Start", font=("Helvetica", 12),
                                      command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(button_frame, text="Stop", font=("Helvetica", 12),
                                      command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(button_frame, text="Save", font=("Helvetica", 12),
                                      command=self.save_text)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.timer_label = tk.Label(master, text="Time: 10s", font=("Helvetica", 14))
        self.timer_label.pack(padx=5, pady=5)

        self.is_running = False
        self.timeout = 10  # seconds before deletion
        self.last_typing_time = None
        self.elapsed_time = 0

    def on_key_press(self, event):
        if self.is_running:
            self.last_typing_time = time.time()

    def start_timer(self):
        self.is_running = True
        self.last_typing_time = time.time()
        self.elapsed_time = 0
        self.update_timer()  # Start the timer display
        self.check_time()  # Start checking for inactivity

    def stop_timer(self):
        self.is_running = False
        self.timer_label.config(text="Time: 10s")  # Reset timer display

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = int(time.time() - self.last_typing_time)
            remaining_time = max(0, self.timeout - self.elapsed_time)
            self.timer_label.config(text=f"Time: {remaining_time}s")

            if remaining_time <= 0:
                self.text_area.delete(1.0, tk.END)  # Clear the text area

            self.master.after(1000, self.update_timer) # Update every second

    def check_time(self):
        if self.is_running and self.last_typing_time is not None:
            if time.time() - self.last_typing_time > self.timeout:
                self.text_area.delete(1.0, tk.END)  # Clear the text area
            self.master.after(1000, self.check_time)  # Check again in 1 second

    def save_text(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    app = WriteOrDie(root)
    root.bind('<Key>', app.on_key_press)  # Bind key press events to the app
    root.mainloop()

