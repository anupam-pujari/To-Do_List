import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.tasks = []
        self.load_tasks()
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)
        self.add_button = tk.Button(self.root, text="Add Task", width=20, command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)
        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.complete_button = tk.Button(self.root, text="Complete Task", width=20, command=self.complete_task)
        self.complete_button.grid(row=2, column=0, padx=10, pady=10)
        self.delete_button = tk.Button(self.root, text="Delete Task", width=20, command=self.delete_task)
        self.delete_button.grid(row=2, column=1, padx=10, pady=10)
        self.edit_button = tk.Button(self.root, text="Edit Task", width=20, command=self.edit_task)
        self.edit_button.grid(row=3, column=0, padx=10, pady=10)
        self.sort_button = tk.Button(self.root, text="Sort by Deadline", width=20, command=self.sort_tasks)
        self.sort_button.grid(row=3, column=1, padx=10, pady=10)
        self.filter_button = tk.Button(self.root, text="Filter Pending", width=20, command=self.filter_pending)
        self.filter_button.grid(row=4, column=0, padx=10, pady=10)
    def load_tasks(self):
        if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 0:
            try:
                with open("tasks.json", "r") as f:
                    self.tasks = json.load(f)
                    for task in self.tasks:
                        if isinstance(task.get("deadline"), str):
                            task["deadline"] = datetime.strptime(task["deadline"], "%Y-%m-%d")
            except json.JSONDecodeError:
                messagebox.showwarning("File Error", "Error decoding tasks from file. ")
                self.tasks = []  
        else:
            self.tasks = []  
    def save_tasks(self):
        try:
            for task in self.tasks:
                if isinstance(task["deadline"], datetime):
                    task["deadline"] = task["deadline"].strftime("%Y-%m-%d") 
            with open("tasks.json", "w") as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving tasks: {e}")
    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            deadline = self.ask_for_deadline()
            if deadline:
                self.tasks.append({"task": task, "status": "Pending", "deadline": deadline})
                self.update_task_list()
                self.save_tasks()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "Please enter a valid deadline!")
        else:
            messagebox.showwarning("Input Error", "Please enter a task!")
    def ask_for_deadline(self):
        deadline_str = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD):")
        if deadline_str:
            try:
                return datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
                return None
        return None
    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]["status"] = "Completed"
            self.update_task_list()
            self.save_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed!")
    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.update_task_list()
            self.save_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            task = self.tasks[task_index]
            new_task_name = simpledialog.askstring("Edit Task", f"Edit task: {task['task']}")
            if new_task_name:
                new_deadline = self.ask_for_deadline()
                if new_deadline:
                    self.tasks[task_index]["task"] = new_task_name
                    self.tasks[task_index]["deadline"] = new_deadline
                    self.update_task_list()
                    self.save_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit!")
    def sort_tasks(self):
        self.tasks.sort(key=lambda x: x["deadline"])
        self.update_task_list()
        self.save_tasks()
    def filter_pending(self):
        filtered_tasks = [task for task in self.tasks if task["status"] == "Pending"]
        self.update_task_list(filtered_tasks)
    def update_task_list(self, tasks=None):
        self.task_listbox.delete(0, tk.END)
        tasks = tasks or self.tasks  
        for task in tasks:
            deadline = task["deadline"].strftime('%Y-%m-%d') if isinstance(task["deadline"], datetime) else task["deadline"]
            task_display = f"{task['task']} - {task['status']} - Deadline: {deadline}"
            self.task_listbox.insert(tk.END, task_display)
def main():
    try:
        root = tk.Tk()
        app = ToDoApp(root)
        root.mainloop()
    except tk.TclError as e:
        messagebox.showerror("Tkinter Error", f"Error initializing Tkinter: {e}")
        print(f"Tkinter Error: {e}")
if __name__ == "__main__":
    main()
    