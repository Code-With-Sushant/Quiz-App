import tkinter as tk
import random
import time

class CustomTkinter:
 
    def custom_button(master, text, command=None):
        button = tk.Button(master, text=text, command=command, bg="#3498db", fg="white", font=("Helvetica", 12))
        return button

 
    def custom_label(master, text, font=("Helvetica", 14)):
        label = tk.Label(master, text=text, font=font)
        return label

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("400x300")

        self.current_question = 0
        self.score = 0

        # Create a frame for the quiz questions
        self.quiz_frame = tk.Frame(root)
        self.quiz_frame.pack(pady=10)

        # Create a frame for the result screen
        self.result_frame = tk.Frame(root)

        # Quiz data (questions, options, correct answers)
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Mars", "Venus", "Jupiter"],
                "correct_answer": "Mars"
            },
            {
                "question": "What is the largest mammal?",
                "options": ["Elephant", "Giraffe", "Blue Whale", "Lion"],
                "correct_answer": "Blue Whale"
            },
            {
                "question": "What is the chemical symbol for gold?",
                "options": ["Ag", "Au", "Fe", "Hg"],
                "correct_answer": "Au"
            }
        ]

        # Shuffle the questions to randomize the order
        random.shuffle(self.questions)

        # Timer variables
        self.timer_seconds = 10
        self.timer_label = CustomTkinter.custom_label(self.quiz_frame, "")
        self.timer_label.pack()

        # Create the timer
        self.timer = None

        # Display the first question
        self.show_next_question()

    def show_next_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.quiz_label = CustomTkinter.custom_label(self.quiz_frame, question_data["question"])
            self.quiz_label.pack(pady=10)

            options = question_data["options"]
            for i in range(4):
                button = CustomTkinter.custom_button(self.quiz_frame, options[i], command=lambda i=i: self.check_answer(i))
                button.pack(fill="both", expand=True, padx=10, pady=5)

            self.start_timer()
        else:
            self.show_result()

    def start_timer(self):
        self.timer_seconds = 10
        self.update_timer_label()
        self.timer = self.root.after(1000, self.update_timer)

    def update_timer(self):
        self.timer_seconds -= 1
        self.update_timer_label()
        if self.timer_seconds == 0:
            self.root.after_cancel(self.timer)
            self.next_question()

        else:
            self.timer = self.root.after(1000, self.update_timer)

    def update_timer_label(self):
        self.timer_label.config(text=f"Time left: {self.timer_seconds} seconds")

    def check_answer(self, selected_option):
        question_data = self.questions[self.current_question]
        if question_data["options"][selected_option] == question_data["correct_answer"]:
            self.score += 1
            feedback = "Correct!"
        else:
            feedback = "Wrong!"
        self.show_feedback(feedback)

    def show_feedback(self, feedback):
        feedback_label = CustomTkinter.custom_label(self.quiz_frame, feedback)
        feedback_label.pack(pady=10)
        self.root.after(2000, lambda: feedback_label.pack_forget())
        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.timer:
            self.root.after_cancel(self.timer)
        self.quiz_label.pack_forget()
        for button in self.quiz_frame.winfo_children():
            button.pack_forget()
        self.show_next_question()

    def show_result(self):
        self.quiz_frame.pack_forget()

        result_label = CustomTkinter.custom_label(self.result_frame, "Quiz Over!\nYour Score: {}/{}".format(self.score, len(self.questions)))
        result_label.pack(pady=20)

        restart_button = CustomTkinter.custom_button(self.result_frame, "Restart Quiz", self.restart_quiz)
        restart_button.pack()

        self.result_frame.pack()

    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.result_frame.pack_forget()
        self.quiz_frame.pack()
        self.questions = random.sample(self.questions, len(self.questions))  # Randomize question order
        self.show_next_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

