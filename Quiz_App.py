import tkinter as tk
from tkinter import messagebox
import json

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.score = 0
        self.questions = self.load_questions_from_file()
        self.current_question_index = 0
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
        self.is_signup.set(not self.is_signup.get())  
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
                questions = json.loads(file)
                return questions.get('questions', '')
        except FileNotFoundError:
            messagebox.showerror("Error", "Questions file not found.")
            return []

    def show_quiz(self):
        self.master.withdraw() 
        if not self.questions:
            messagebox.showerror("Error", "No questions available. Cannot start the quiz.")
            self.master.deiconify()  
            return
        
        if hasattr(self, 'quiz_window') and self.quiz_window.winfo_exists():
            self.quiz_window.destroy()

        quiz_window = tk.Toplevel(self.master)
        quiz_window.title(f"Question {self.question_number}")
        quiz_window.geometry("400x300")
        quiz_window.config(bg="#87BDD8")
        
        self.show_question(quiz_window, self.questions, self.current_question_index)
    
    def show_next_question(self, quiz_window, current_question_index):
        if quiz_window and quiz_window.winfo_exists():
            quiz_window.destroy()

        if current_question_index < len(self.questions) - 1:
            self.current_question_index = current_question_index + 1
            # self.question_number += 1

            new_quiz_window = tk.Toplevel(self.master)
            new_quiz_window.geometry("400x300")
            new_quiz_window.config(bg="#87BDD8")

            self.show_question(new_quiz_window, self.questions, self.current_question_index)
        else:
            messagebox.showinfo("Quiz Completed", f"You have completed the quiz!\nYour final score is: {self.score}")
            self.master.deiconify()  
    
    def show_previous_question(self, quiz_window, current_question_index):
        if quiz_window and quiz_window.winfo_exists():
            quiz_window.destroy()

        if current_question_index > 0:
            current_question_index = self.current_question_index - 1
            # self.question_number -= 1
            new_quiz_window = tk.Toplevel(self.master)
            new_quiz_window.geometry("400x300")
            new_quiz_window.config(bg="#87BDD8")

            self.show_question(new_quiz_window, self.questions, current_question_index)
            
        elif current_question_index == 0:
            messagebox.showinfo("Info", "You are already at the first question.")
            first_quiz_window = tk.Toplevel(self.master)
            first_quiz_window.geometry("400x300")
            first_quiz_window.config(bg="#87BDD8")

            self.show_question(first_quiz_window, self.current_question_index)

    def quit_quiz(self, quiz_window):
        quiz_window.destroy()
        self.master.deiconify()  
        messagebox.showinfo("Quiz Quit", "Quiz exited. You are now back on the home page.")
        
    def show_question(self, quiz_window, questions, current_question_index):
        self.questions = questions
        current_question = questions[current_question_index]
        quiz_window.title(f"Question {self.question_number}")
        question_label = tk.Label(quiz_window, text=current_question['question'])
        option_buttons = []

        question_label.pack(pady=10)
        # for i, option_tuple in enumerate(current_question['options']):
        #     option, option_text = option_tuple
        #     option_buttons.append(tk.Button(quiz_window, text=f"{option}. {option_text}",
        #                                     command=lambda option=option: self.check_answer(quiz_window, current_question, option)))
        for option in current_question['options']:
                option_buttons.append(tk.Button(quiz_window, text=f"{option[0]}. {option[1]}",
                                                command=lambda opt=option: self.check_answer(quiz_window, current_question, opt)))
        
        for button in option_buttons:
            button.pack()

        continue_button = tk.Button(quiz_window, text="Next Question",
                                    command=lambda: self.show_next_question(quiz_window, 
                                                                            current_question_index))
          
        quit_button = tk.Button(quiz_window, text="Quit Quiz", command=lambda: self.quit_quiz(quiz_window))
        
        previous_button = tk.Button(quiz_window, text="Previous Question",
                                    command=lambda: self.show_previous_question(quiz_window,
                                                                              current_question_index))

        continue_button.pack(pady=10)
        previous_button.pack(pady=10)
        quit_button.pack(pady=10)

    def check_answer(self, quiz_window, current_question, selected_option):
        correct_answer = current_question['correct_answer']

        if selected_option == correct_answer:
            messagebox.showinfo("Correct", "Your answer is correct!")
            self.score += 1 
        else:
            messagebox.showinfo("Incorrect", f"Sorry, the correct answer is {correct_answer}.")

        messagebox.showinfo("Score", f"Your current score is: {self.score}")
        self.show_next_question(quiz_window, self.current_question_index)
        
try:
    with open("Student_data.json", "r") as file:
        student_data = json.load(file)
except FileNotFoundError:
    student_data = {}


root = tk.Tk()
app = QuizApp(root)
# app.show_question(root, app.current_question_index)
root.mainloop()
