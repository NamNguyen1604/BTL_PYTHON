import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class TriviaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧐 Trivia Challenge")
        self.skip_empty_warning = False  # Đánh dấu đã cảnh báo chưa

        # Load ảnh nền
        try:
            self.bg_image = Image.open("background.png")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file background.png.")
            self.root.destroy()
            return

        self.canvas = tk.Canvas(root, width=self.bg_image.width, height=self.bg_image.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.center_x = self.bg_image.width // 2
        self.center_y = self.bg_image.height // 2

        # Load câu hỏi
        self.questions = self.load_questions("trivia.txt")
        self.score = 0
        self.question_index = 0

        # Giao diện bắt đầu
        self.start_button = tk.Button(root, text="🎮 Bắt đầu chơi", font=("Arial", 16, "bold"),
                                      bg="#4CAF50", fg="white", command=self.start_game)
        self.start_window = self.canvas.create_window(self.center_x, self.center_y, window=self.start_button)

    def load_questions(self, filename):
        questions = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    if '|' in line:
                        q, a = line.strip().split("|")
                        questions.append((q.strip(), a.strip()))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file trivia.txt.")
            self.root.destroy()
        return questions

    def start_game(self):
        # Reset
        self.score = 0
        self.question_index = 0
        self.skip_empty_warning = False
        self.questions = self.load_questions("trivia.txt")

        # Xoá mọi thứ cũ
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Các thành phần chính
        self.question_label = self.canvas.create_text(
            self.center_x, 100, text="", font=("Arial", 20, "bold"), fill="black", width=600
        )

        self.answer_entry = tk.Entry(self.root, font=("Arial", 16))
        self.entry_window = self.canvas.create_window(self.center_x, 160, window=self.answer_entry, width=300)

        self.submit_button = tk.Button(self.root, text="Trả lời", font=("Arial", 14),
                                       bg="#2196F3", fg="white", command=self.check_answer)
        self.submit_window = self.canvas.create_window(self.center_x, 210, window=self.submit_button)

        self.score_label = self.canvas.create_text(
            self.center_x, 50, text="🌟 Điểm: 0", font=("Arial", 16, "bold"), fill="blue"
        )

        self.end_button = tk.Button(self.root, text="Thoát", font=("Arial", 12),
                                    bg="gray", fg="white", command=self.root.destroy)
        self.end_window = self.canvas.create_window(self.center_x, 260, window=self.end_button)

        self.load_next_question()

        self.root.bind("<Return>", lambda event: self.check_answer())
        self.root.bind("<Escape>", lambda event: self.root.destroy())

    def load_next_question(self):
        if self.question_index < len(self.questions):
            q_text = f"Câu {self.question_index + 1}: {self.questions[self.question_index][0]}"
            self.canvas.itemconfig(self.question_label, text=q_text)
        else:
            self.show_result()

    def check_answer(self):
        user_ans = self.answer_entry.get().strip()
        correct_ans = self.questions[self.question_index][1]

        if user_ans == "":
            if not self.skip_empty_warning:
                messagebox.showwarning("Chưa nhập đáp án", "⚠️ Vui lòng nhập đáp án trước khi tiếp tục.")
                self.skip_empty_warning = True
                return  # Không chuyển tiếp ngay lần đầu
            # Nếu đã cảnh báo trước đó, cho qua và chuyển tiếp như sai
            messagebox.showinfo("Bỏ qua", f"Bạn đã bỏ qua câu này. Đáp án đúng là: {correct_ans}")
        elif user_ans.lower() == correct_ans.lower():
            self.score += 1
            messagebox.showinfo("🎉 Đúng rồi!", "Bạn đã trả lời chính xác!")
        else:
            messagebox.showwarning("❌ Sai rồi!", f"Đáp án đúng là: {correct_ans}")

        self.answer_entry.delete(0, tk.END)
        self.question_index += 1
        self.skip_empty_warning = False  # Reset cho câu tiếp theo
        self.canvas.itemconfig(self.score_label, text=f"🌟 Điểm: {self.score}")
        self.load_next_question()

    def show_result(self):
        self.canvas.delete(self.question_label)
        self.canvas.delete(self.entry_window)
        self.canvas.delete(self.submit_window)
        self.canvas.delete(self.end_window)
        self.canvas.delete(self.score_label)

        self.canvas.create_text(
            self.center_x, self.center_y - 30,
            text=f"🎉 Trò chơi kết thúc!\nBạn ghi được {self.score} điểm 🌟.",
            font=("Arial", 22, "bold"),
            fill="darkgreen",
            justify="center"
        )

        self.retry_button = tk.Button(self.root, text="🔁 Chơi lại", font=("Arial", 14, "bold"),
                                      bg="#f57c00", fg="white", command=self.start_game)
        self.retry_window = self.canvas.create_window(self.center_x, self.center_y + 50, window=self.retry_button)

# Khởi chạy
if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaGame(root)
    root.mainloop()