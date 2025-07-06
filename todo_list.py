import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

TODO_FILE = "todos.json"

# --- To-Do List Core Logic ---
def load_todos():
    """Loads to-do items from a JSON file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Saves to-do items to a JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

def secret_admin_function():
    """This function contains a 'secret' string for demonstration."""
    admin_key = "SUPER_SECRET_ADMIN_KEY_12345"
    return admin_key

# --- GUI Application Class ---
class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple To-Do List")
        master.geometry("450x650") # Increased height for new button
        master.resizable(False, False) # Fixed size for simplicity

        self.todos = load_todos()

        # --- Widgets ---
        self.task_label = tk.Label(master, text="New Task:")
        self.task_label.pack(pady=5)

        self.task_entry = tk.Entry(master, width=40)
        self.task_entry.pack(pady=5)
        self.task_entry.bind("<Return>", lambda event=None: self.add_task()) # Bind Enter key

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_list_label = tk.Label(master, text="Your Tasks:")
        self.task_list_label.pack(pady=5)

        self.task_list_text = scrolledtext.ScrolledText(master, width=50, height=15, state='disabled')
        self.task_list_text.pack(pady=5)

        self.complete_label = tk.Label(master, text="Task # to Mark Complete:")
        self.complete_label.pack(pady=5)

        self.complete_entry = tk.Entry(master, width=10)
        self.complete_entry.pack(pady=5)
        self.complete_entry.bind("<Return>", lambda event=None: self.mark_task_complete())

        self.complete_button = tk.Button(master, text="Mark Complete", command=self.mark_task_complete)
        self.complete_button.pack(pady=5)

        # --- New: Delete Task Widgets ---
        self.delete_label = tk.Label(master, text="Task # to Delete:")
        self.delete_label.pack(pady=5)

        self.delete_entry = tk.Entry(master, width=10)
        self.delete_entry.pack(pady=5)
        self.delete_entry.bind("<Return>", lambda event=None: self.delete_task())

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)
        # --- End New: Delete Task Widgets ---

        self.secret_button = tk.Button(master, text="Access Secret Admin", command=self.access_secret_admin)
        self.secret_button.pack(pady=10)

        self.update_task_list()

    def update_task_list(self):
        self.task_list_text.config(state='normal')
        self.task_list_text.delete(1.0, tk.END)
        if not self.todos:
            self.task_list_text.insert(tk.END, "No tasks in your to-do list.")
        else:
            for i, todo in enumerate(self.todos):
                status = "✓" if todo["completed"] else " "
                self.task_list_text.insert(tk.END, f"{i + 1}. [{status}] {todo['task']}\n")
        self.task_list_text.config(state='disabled')

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            return

        # Check for duplicates (case-insensitive, uncompleted tasks)
        for todo in self.todos:
            if todo['task'].lower() == task.lower() and not todo['completed']:
                messagebox.showerror("Duplicate Task", f"Task '{task}' already exists and is not completed.")
                self.task_entry.delete(0, tk.END)
                return

        self.todos.append({"task": task, "completed": False})
        save_todos(self.todos)
        self.task_entry.delete(0, tk.END)
        self.update_task_list()
        messagebox.showinfo("Success", f"Added task: '{task}'")

    def mark_task_complete(self):
        try:
            task_num = int(self.complete_entry.get()) - 1 # Adjust for 0-based index
            if 0 <= task_num < len(self.todos):
                self.todos[task_num]["completed"] = True
                save_todos(self.todos)
                self.update_task_list()
                messagebox.showinfo("Success", f"Task '{self.todos[task_num]['task']}' marked as complete.")
            else:
                messagebox.showwarning("Input Error", "Invalid task number.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the task.")
        self.complete_entry.delete(0, tk.END)

    def delete_task(self):
        """Deletes a task from the list."""
        try:
            task_num = int(self.delete_entry.get()) - 1 # Adjust for 0-based index
            if 0 <= task_num < len(self.todos):
                deleted_task = self.todos.pop(task_num) # Remove the task
                save_todos(self.todos)
                self.update_task_list()
                messagebox.showinfo("Success", f"Task '{deleted_task['task']}' deleted.")
            else:
                messagebox.showwarning("Input Error", "Invalid task number to delete.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the task to delete.")
        self.delete_entry.delete(0, tk.END) # Clear the input field

    def access_secret_admin(self):
        admin_key = secret_admin_function()
        messagebox.showinfo("Secret Admin", f"Accessed Secret Admin Function!\nKey: {admin_key}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
