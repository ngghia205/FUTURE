import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk
import pygame

# Thay thế de_data và kho_data bằng dữ liệu thích hợp của bạn
from de_data import de_data
from kho_data import kho_data

# Khởi tạo biến is_background_music_playing
is_background_music_playing = False
current_sound = None  # Biến lưu trữ đối tượng âm thanh hiện tại

def play_background_music():
    global is_background_music_playing
    pygame.mixer.init()

    if not is_background_music_playing:
        pygame.mixer.music.load("nhac_nen.mp3")
        pygame.mixer.music.play(-1)  # -1 để lặp lại nhạc nền liên tục
        is_background_music_playing = True

def stop_background_music():
    pygame.mixer.music.stop()

def play_sound(file_path):
    global current_sound
    if current_sound:
        current_sound.stop()  # Dừng âm thanh hiện tại nếu có

    sound = pygame.mixer.Sound(file_path)
    sound.play()
    current_sound = sound

def show_question():
    global current_question, question_data, difficulty
    question = question_data[current_question]

    # Dừng âm thanh nền trước khi phát âm thanh câu hỏi
    stop_background_music()

    # Tạo tên tệp âm thanh dựa trên độ khó và số câu hỏi
    audio_file = f"c{current_question + 1}-{difficulty.lower()}.mp3"
    play_sound(audio_file)  # Phát âm thanh câu hỏi

    qs_label.config(text=question["question"])

    for i in range(4):
        choice_btns[i].config(text=question["choices"][i], state="normal")

    feedback_label.config(text="")
    next_btn.config(state="disabled")

def check_answer(choice):
    global current_question, score, difficulty
    question = question_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
        score += 1
        score_label.config(text=f"Điểm: {score}/{len(question_data)}", foreground="green")
        feedback_label.config(text="Chính xác", foreground="green")
        play_sound("dung.mp3")  # Phát âm thanh khi trả lời đúng
    else:
        feedback_label.config(text="Câu trả lời sai", foreground="red")
        play_sound("sai.mp3")  # Phát âm thanh khi trả lời sai

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

def next_question():
    global current_question, current_sound
    current_question += 1

    if current_sound:
        current_sound.stop()  # Dừng âm thanh hiện tại khi chuyển câu hỏi

    if current_question < len(question_data):
        show_question()
    else:
        messagebox.showinfo("Kết thúc", f"Bạn trả lời đúng: {score}/{len(question_data)} câu hỏi")
        # Dừng âm thanh nền khi kết thúc
        stop_background_music()
        root.destroy()

def start_game(diff):
    global question_data, current_question, score, difficulty, is_background_music_playing, current_sound
    difficulty = diff
    current_question = 0
    score = 0
    is_background_music_playing = False

    if current_sound:
        current_sound.stop()  # Dừng âm thanh hiện tại nếu có

    if difficulty == "Dễ":
        question_data = de_data
    elif difficulty == "Khó":
        question_data = kho_data

    show_question()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("WHO ARE TALENTED ENGINEERS?")
root.geometry("1213x682")
style = Style(theme="flatly")
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Load hình nền từ tệp background_ueh.jpg
background_image = Image.open("background_ueh.png")
background_photo = ImageTk.PhotoImage(background_image)
# Tạo Canvas để chứa hình nền
canvas = tk.Canvas(root, width=1213, height=682)
canvas.pack()

# Vẽ hình nền lên Canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

# Tạo nhãn câu hỏi
qs_label = ttk.Label(root, anchor="center", wraplength=800, padding=5)
qs_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Tạo nút lựa chọn
choice_btns = [ttk.Button(root, command=lambda i=i: check_answer(i)) for i in range(4)]
for i, button in enumerate(choice_btns):
    button.place(relx=0.5, rely=0.3 + i * 0.1, anchor=tk.CENTER)

# Tạo nhãn phản hồi
feedback_label = ttk.Label(root, anchor="center", padding=10)
feedback_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Khởi tạo điểm
score = 0

# Tạo nhãn điểm
score_label = ttk.Label(root, text=f"Điểm: {score}/0", anchor="center", padding=10)
score_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# Tạo nút tiếp theo
next_btn = ttk.Button(root, text="Tiếp tục", command=next_question, state="disabled")
next_btn.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# Tạo nút bắt đầu game với độ khó "Dễ"
start_de_btn = ttk.Button(root, text="Bắt đầu - Dễ", command=lambda: start_game("Dễ"))
start_de_btn.place(relx=0.35, rely=0.105, anchor=tk.CENTER)

# Tạo nút bắt đầu game với độ khó "Khó"
start_kho_btn = ttk.Button(root, text="Bắt đầu - Khó", command=lambda: start_game("Khó"))
start_kho_btn.place(relx=0.65, rely=0.105, anchor=tk.CENTER)

# Chạy nhạc nền
play_background_music()

# Bắt đầu vòng lặp sự kiện chính
root.mainloop()
