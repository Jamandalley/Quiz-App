import tkinter as tk
from tkinter import messagebox
import json

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Application")
        self.master.geometry("400x400")
        self.master.config(bg="#87BDD8")
        self.is_signup = tk.BooleanVar(value=False) 
        self.question_number = 1
        self.username_label = tk.Label(self.master, text="Username:", font=("Times New Roman", 10))
        self.username_entry = tk.Entry(self.master)

        self.password_label = tk.Label(self.master, text="Password:", font=("Times New Roman", 10))
        self.password_entry = tk.Entry(self.master, show="*")
        
        self.matric_label = tk.Label(self.master, text="Matric Number:", font=("Times New Roman", 10))
        self.matric_entry = tk.Entry(self.master)
        
        self.toggle_button = tk.Button(self.master, text="Switch to Signup", command=self.toggle_mode)
        self.action_button = tk.Button(self.master, text="Login", command=self.login_signup)

        self.login_button = tk.Button(self.master, text="Login", font=("Times New Roman", 10), command=self.login)
        self.signup_button = tk.Button(self.master, text="Signup", font=("Times New Roman", 10), command=self.signup)
        self.quit_button = tk.Button(self.master, text="Quit", font=("Times New Roman", 10), command=self.master.destroy)

        self.username_label.pack(pady=10)
        self.username_entry.pack(pady=5)
        self.password_label.pack(pady=10)
        self.password_entry.pack(pady=5)

        self.matric_label.pack(pady=10)
        self.matric_entry.pack(pady=5)

        self.toggle_button.pack(pady=5)
        self.action_button.pack(pady=10)

        self.quit_button.pack(pady=10)
        
    def toggle_mode(self):
        self.is_signup.set(not self.is_signup.get())  # Toggle between login and signup
        if self.is_signup.get():
            self.toggle_button.config(text="Switch to Login")
            self.action_button.config(text="Signup")
        else:
            self.toggle_button.config(text="Switch to Signup")
            self.action_button.config(text="Login")

    def login_signup(self):
        username = self.username_entry.get().upper()
        password = self.password_entry.get()
        matric_no = self.matric_entry.get()

        if self.is_signup.get():
            self.signup(username, password, matric_no)
        else:
            self.login(username, password)

    def signup(self, username, password, matric_no):
        if matric_no in student_data:
            messagebox.showerror("Signup Failed", "Matriculation number already exists. Choose a different one.")
            return

        student_data[matric_no] = {'username': username, 'password': password, 'matric_no': matric_no}
        self.save_data_to_file()
        messagebox.showinfo("Signup Successful", "Account created successfully. You can now login.")

    def login(self, username, password):
        for details in student_data.values():
            if username == details['username'] and password == details['password']:
                messagebox.showinfo("Login Successful", f"Welcome, {username.capitalize()}!")
                self.show_quiz()
                return

        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")
    
    def save_data_to_file(self):
        with open("Student_data.json", "w") as file:
            json.dump(student_data, file)

    def load_questions_from_file(self, filename="Question.json"):
        try:
            with open(filename, "r") as file:
                questions = json.load(file)
            return questions
        except FileNotFoundError:
            messagebox.showerror("Error", "Questions file not found.")
            return []

    def show_quiz(self):
        self.master.withdraw() 
        questions = self.load_questions_from_file()
        if not questions:
            messagebox.showerror("Error", "No questions available. Cannot start the quiz.")
            self.master.deiconify()  # Show the main window
            return
        
        if hasattr(self, 'quiz_window') and self.quiz_window.winfo_exists():
            self.quiz_window.destroy()

        quiz_window = tk.Toplevel(self.master)
        quiz_window.title(f"Question {self.question_number}")
        quiz_window.geometry("400x300")
        quiz_window.config(bg="#87BDD8")
        
        current_question_index = 0
        self.show_question(quiz_window, questions, current_question_index)
    
    def show_next_question(self, quiz_window, questions, current_question_index):
        if current_question_index < len(questions) - 1:
            current_question_index += 1
            self.question_number += 1
            quiz_window.destroy()
            self.show_question(self.master, questions, current_question_index)
            # quiz_window.title(f"Question {self.question_number}")
        else:
            messagebox.showinfo("Quiz Completed", "You have completed the quiz!")
            quiz_window.destroy()
            self.master.deiconify()  # Show the main window
    
    def show_previous_question(self, quiz_window, questions, current_question_index):
        if current_question_index > 0:
            current_question_index -= 1
            self.question_number -= 1
            self.quiz_window.destroy()
            self.show_question(self.master, questions, current_question_index)


    def quit_quiz(self, quiz_window):
        quiz_window.destroy()
        self.master.deiconify()  # Show the main window
        messagebox.showinfo("Quiz Quit", "Quiz exited. You are now back on the home page.")
        
    def show_question(self, quiz_window, questions, current_question_index):
        current_question = questions[current_question_index]
        quiz_window.title(f"Question {self.question_number}")
        question_label = tk.Label(quiz_window, text=current_question['question'])
        option_buttons = []

        question_label.pack(pady=10)
        for i, option in enumerate(current_question['options']):
            option_buttons.append(tk.Button(quiz_window, text=f"{option}",
                                            command=lambda i=i: self.check_answer(quiz_window, current_question, i)))

        for button in option_buttons:
            button.pack()

        continue_button = tk.Button(quiz_window, text="Next Question",
                                    command=lambda: self.show_next_question(quiz_window, questions, 
                                                                            current_question_index))
          
        quit_button = tk.Button(quiz_window, text="Quit Quiz", command=lambda: self.quit_quiz())
        
        previous_button = tk.Button(quiz_window, text="Previous Question",
                                    command=lambda: self.show_previous_question(quiz_window, questions,
                                                                              current_question_index))

        continue_button.pack(pady=10)
        previous_button.pack(pady=10)
        quit_button.pack(pady=10)

    def check_answer(self):
        # Add your answer checking logic here
        messagebox.showinfo("Result", "Correct answer!")  # Placeholder for demonstration

# Sample student_data dictionary
try:
    with open("Student_data.json", "r") as file:
        student_data = json.load(file)
except FileNotFoundError:
    student_data = {}

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
