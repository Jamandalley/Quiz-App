from tkinter import *
import json
from tkinter import messagebox

class QuizApp:
    def __init__(self, root, question_file):
        self.root = root
        self.root.title("GFG QUIZ APP")
        self.root.geometry("850x520")
        self.root.minsize(800, 400)

        self.load_questions(question_file)

        self.user_ans = StringVar()
        self.user_ans.set('None')
        self.user_score = IntVar()
        self.user_score.set(0)

        Label(root, text="Quiz App", 
              font="calibre 40 bold",
              relief=SUNKEN, background="cyan", 
              padx=10, pady=9).pack()

        Label(root, text="", font="calibre 10 bold").pack()

        self.start_button = Button(root, 
                                   text="Start Quiz",
                                   command=self.login_page, 
                                   font="calibre 17 bold")
        self.start_button.pack()

        self.f1 = Frame(root)
        self.f1.pack(side=TOP, fill=X)

        self.next_button = Button(root, text="Next Question",
                                  command=self.next_question, 
                                  font="calibre 17 bold")
        self.users = {}

    def load_questions(self, question_file):
        with open(question_file, 'r') as file:
            self.questions = json.load(file)
            self.current_question = 0

    def login_page(self):
        self.login_window = Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("300x250")
        
        self.username_entry_label = Label(self.login_window, text="Username:", 
                                                  font=("Times New Roman", 10))
        self.username_entry = Entry(self.login_window, font="calibre 15")
        self.username_entry_label.pack(pady=5)
        self.username_entry.pack(pady=10)
        
        self.password_entry_level = Label(self.login_window, text="Password:", 
                                                  font=("Times New Roman", 10))
        self.password_entry = Entry(self.login_window, font="calibre 15", show="*")
        self.password_entry_level.pack(pady=5)
        self.password_entry.pack(pady=10)

        self.sign_up_button = Radiobutton(self.login_window, text="Sign Up", value="sign_up", 
                                          command=self.sign_up_page)
        self.sign_up_button.pack(pady=10)

        self.login_button = Button(self.login_window, text="Login", 
                                   command=lambda: self.check_login(self.username_entry.get(),
                                                                    self.password_entry.get()))
        self.login_button.pack(pady=10)

    def sign_up_page(self):
        self.sign_up_window = Toplevel(self.root)
        self.sign_up_window.title("Sign Up")
        self.sign_up_window.geometry("300x300")

        self.sign_up_matric_entry_label = Label(self.sign_up_window, text="Matric Number:", 
                                                font=("Times New Roman", 10))
        self.sign_up_matric_entry = Entry(self.sign_up_window, font="calibre 15")
        self.sign_up_matric_entry_label.pack(pady=5)
        self.sign_up_matric_entry.pack(pady=10)

        self.sign_up_username_entry_label = Label(self.sign_up_window, text="Username:", 
                                                  font=("Times New Roman", 10))
        self.sign_up_username_entry = Entry(self.sign_up_window, font="calibre 15")
        self.sign_up_username_entry_label.pack(pady=5)
        self.sign_up_username_entry.pack(pady=10)

        self.sign_up_password_entry_label = Label(self.sign_up_window, text="Password:", 
                                                  font=("Times New Roman", 10))
        self.sign_up_password_entry = Entry(self.sign_up_window, font="calibre 15", show="*")
        self.sign_up_password_entry_label.pack(pady=5)
        self.sign_up_password_entry.pack(pady=10)

        self.sign_up_button = Button(self.sign_up_window, 
                                     text="Sign Up", 
                                     command=lambda: self.save_user(self.sign_up_matric_entry.get(), 
                                                                    self.sign_up_username_entry.get(), 
                                                                    self.sign_up_password_entry.get()))
        self.sign_up_button.pack(pady=10)

    def save_user(self, matric_no, username, password):
        if matric_no in self.users:
            Label(self.sign_up_window, text="Matriculation number already exists", font="calibre 12").pack()
        else:
            self.users[matric_no] = {'username': username, 'password': password, 'matric_no': matric_no}
            with open("Student_data.json", "w") as file:
                json.dump(self.users, file)
            messagebox.showinfo("Signup Successful", "Account created successfully. You can now login.")
            self.sign_up_window.destroy()

    def check_login(self, username, password):
        for details in self.users.values():
            if username == details['username'] and password == details['password']:
                messagebox.showinfo("Login Successful", f"Welcome, {username.capitalize()}!")
                self.login_window.destroy()
                self.start_quiz()
                return
            
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")

    def start_quiz(self):
        self.start_button.forget()
        self.next_button.pack()
        self.next_question()

    def next_question(self):
        if self.current_question < len(self.questions):
            self.check_ans()
            self.user_ans.set('None')
            current_question_data = self.questions[self.current_question]
            self.clear_frame()
            Label(self.f1, text=f"Question : {current_question_data['question']}", padx=15,
                  font="calibre 12 normal").pack(anchor=NW)

            for option in current_question_data['options']:
                Radiobutton(self.f1, text=f"{option[0]} {option[1]}", variable=self.user_ans,
                            value=option[0], padx=28).pack(anchor=NW)

            self.current_question += 1
        else:
            self.next_button.forget()
            self.check_ans()
            self.clear_frame()
            output = f"Your Score is {self.user_score.get()} out of {len(self.questions)}"
            Label(self.f1, text=output, font="calibre 25 bold").pack()
            Label(self.f1, text="Thanks for Participating",
                  font="calibre 18 bold").pack()
            self.end_button = Button(self.f1, text="End", command=self.root.destroy,
                                    font="calibre 15 bold")
            self.end_button.pack()

    def check_ans(self):
        if self.current_question > 0:
            temp_ans = self.user_ans.get()
            correct_answer = self.questions[self.current_question-1]['correct_answer']
            if temp_ans != 'None' and temp_ans == correct_answer:
                self.user_score.set(self.user_score.get()+1)

    def clear_frame(self):
        for widget in self.f1.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    quiz_app = QuizApp(root, "Question.json")
    root.mainloop()