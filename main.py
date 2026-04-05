from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random
import time


# ---------------- SCREENS ----------------
class SplashScreen(Screen):
    pass


class StartScreen(Screen):
    pass


class QuizScreen(Screen):
    pass


class ResultScreen(Screen):
    pass


class DeveloperScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# ---------------- LOAD KV ----------------
kv = Builder.load_file("kv_design.kv")


# ---------------- APP ----------------
class MathApp(App):

    def build(self):
        self.score = 0
        self.num1 = 0
        self.num2 = 0
        self.operation = "+"
        self.time_left = 60
        self.event = None
        self.level = "Primary 1"
        self.student_name = ""

        self.correct_sound = SoundLoader.load("assets/correct.wav")
        self.wrong_sound = SoundLoader.load("assets/wrong.wav")

        return kv

    # ---------------- SPLASH SCREEN ----------------
    def on_start(self):
        Clock.schedule_once(self.go_to_start, 3)

    def go_to_start(self, dt):
        self.root.current = "start"

    # ---------------- LEVEL + NAME ----------------
    def set_level(self, level):
        start = self.root.get_screen("start")
        name = start.ids.student_name.text.strip()

        if name == "":
            return

        self.student_name = name
        self.level = level
        self.start_app()

    def get_range(self):
        if self.level == "Primary 1":
            return 1, 10
        elif self.level == "Primary 2":
            return 1, 20
        elif self.level == "Primary 3":
            return 1, 50
        elif self.level == "Primary 4":
            return 10, 100
        elif self.level == "Primary 5":
            return 20, 150
        else:
            return 50, 200

    # ---------------- START QUIZ ----------------
    def start_app(self):
        self.score = 0
        self.time_left = 60
        self.root.current = "quiz"

        self.start_timer()
        self.generate_question()

    # ---------------- TIMER ----------------
    def start_timer(self):
        if self.event:
            self.event.cancel()

        self.event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.root.get_screen("quiz").ids.timer.text = f"Time: {self.time_left}"

        if self.time_left <= 0:
            if self.event:
                self.event.cancel()
            self.end()

    # ---------------- QUESTION ----------------
    def generate_question(self):
        low, high = self.get_range()

        self.num1 = random.randint(low, high)
        self.num2 = random.randint(low, high)
        self.operation = random.choice(["+", "-", "*"])

        if self.operation == "+":
            question = f"{self.num1} + {self.num2}"
        elif self.operation == "-":
            question = f"{self.num1} - {self.num2}"
        else:
            question = f"{self.num1} × {self.num2}"

        quiz = self.root.get_screen("quiz")

        quiz.ids.question.text = question
        quiz.ids.answer.text = ""
        quiz.ids.feedback.text = ""

        quiz.ids.answer.disabled = False

    # ---------------- CHECK ANSWER ----------------
    def check_answer(self):
        quiz = self.root.get_screen("quiz")

        if quiz.ids.answer.disabled:
            return

        try:
            user_answer = int(quiz.ids.answer.text)

            if self.operation == "+":
                correct = self.num1 + self.num2
            elif self.operation == "-":
                correct = self.num1 - self.num2
            else:
                correct = self.num1 * self.num2

            if user_answer == correct:
                self.score += 1
                quiz.ids.feedback.text = "✅ Correct!"
                if self.correct_sound:
                    self.correct_sound.play()
            else:
                quiz.ids.feedback.text = f"❌ {correct}"
                if self.wrong_sound:
                    self.wrong_sound.play()

            quiz.ids.score.text = f"Score: {self.score}"

            quiz.ids.answer.disabled = True

        except:
            quiz.ids.feedback.text = "Enter a number!"

    # ---------------- NEXT ----------------
    def next_question(self):
        self.generate_question()

    # ---------------- SAVE RESULT ----------------
    def save_result(self):
        with open("results.txt", "a") as file:
            file.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{self.student_name} | {self.level} | Score: {self.score}\n"
            )

    # ---------------- END ----------------
    def end(self):
        self.save_result()

        self.root.get_screen("result").ids.final_score.text = (
            f"{self.student_name} | {self.level}\nScore: {self.score}"
        )

        self.root.current = "result"

    # ---------------- RESTART ----------------
    def restart(self):
        self.root.current = "start"


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    MathApp().run()