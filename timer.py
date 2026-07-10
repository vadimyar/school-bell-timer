import pygame
import sys
import re
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -----------------------------
# Парсинг расписания (без изменений)
# -----------------------------

def parse_schedule(filename):
    schedule = {}
    current_day = None
    time_pattern = re.compile(r'(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})\s+(.+)')
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']:
                current_day = line
                schedule[current_day] = []
                continue
            if current_day is None:
                continue
            match = time_pattern.match(line)
            if match:
                h1, m1, h2, m2, title = match.groups()
                start = f"{h1.zfill(2)}:{m1}"
                end = f"{h2.zfill(2)}:{m2}"
                schedule[current_day].append((start, end, title))
    return schedule

def find_current_interval(intervals, now_time_str):
    now = datetime.strptime(now_time_str, "%H:%M")
    for start_str, end_str, title in intervals:
        start = datetime.strptime(start_str, "%H:%M")
        end = datetime.strptime(end_str, "%H:%M")
        if start <= now < end:
            return start_str, end_str, title
    return None

# -----------------------------
# Простое окно без трея
# -----------------------------

class SimpleBellWindow(QMainWindow):

    def __init__(self, schedule_file):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # ← ЭТА СТРОКА
        # ... остальной код (setTitle, resize и т.д.)    
        self.setWindowTitle("- Звонилки -")
        self.resize(300, 330)
        self.setStyleSheet("background-color: #2e2e2e;")
        self.schedule = parse_schedule(schedule_file)

        # Инициализация звука
        pygame.mixer.init()
        try:
            self.lesson_sound = pygame.mixer.Sound("bell2.wav")     # для начала урока
            self.break_sound = pygame.mixer.Sound("bell.wav")     # для начала перемены
        except pygame.error as e:
            print(f"Ошибка загрузки звука: {e}")
            self.lesson_sound = self.break_sound = None

        self.last_interval_key = None
        self.last_interval_type = None  # 'lesson' или 'break'

        self.canvas = FigureCanvas(Figure(facecolor='#2e2e2e'))
        self.ax = self.canvas.figure.subplots()
        self.ax.set_facecolor('#2e2e2e')

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        container = QWidget()
        container.setStyleSheet("background-color: #2e2e2e;")
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(1000)
        self.update_chart()

    def update_chart(self):
        now = datetime.now()
        weekday_map = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}
        today = weekday_map[now.weekday()]
        now_str = now.strftime("%H:%M")

        intervals = self.schedule.get(today, [])
        current = find_current_interval(intervals, now_str)

        self.ax.clear()

        if not current:
            self.ax.text(0.5, 0.5, "Сейчас нет уроков", ha='center', va='center', fontsize=14, color='white')
            self.canvas.draw()
            self.last_interval_key = None
            self.last_interval_type = None
            return

        start_str, end_str, title = current
        start = datetime.strptime(start_str, "%H:%M")
        end = datetime.strptime(end_str, "%H:%M")

        total_duration = (end - start).total_seconds()
        elapsed = (now - start.replace(year=now.year, month=now.month, day=now.day)).total_seconds()
        remaining = max(0, total_duration - elapsed)
        elapsed = max(0, min(elapsed, total_duration))

        interval_key = (today, start_str, end_str)
        is_break = 'перемена' in title.lower()
        current_type = 'break' if is_break else 'lesson'

        # Проверка смены интервала
        if interval_key != self.last_interval_key:
            if self.last_interval_key is not None:  # не при первом запуске
                if current_type == 'break' and self.break_sound:
                    self.break_sound.play()
                elif current_type == 'lesson' and self.lesson_sound:
                    self.lesson_sound.play()

            self.last_interval_key = interval_key
            self.last_interval_type = current_type

        # Цвета
        color_elapsed = '#545454'
        color_remaining = '#18AC00' if is_break else '#FF2A2A'

        self.ax.pie(
            [elapsed, remaining],
            labels=['', ''],
            colors=[color_elapsed, color_remaining],
            autopct=lambda pct: f"{pct:.0f}%\n({str(int(pct/100*total_duration//60)).zfill(2)}:{str(int(pct/100*total_duration%60)).zfill(2)})",
            startangle=90,
            counterclock=False,
            textprops={'color': 'white'}
        )
        self.ax.set_title(f"{title}\n{start_str} – {end_str}", fontsize=14, color='#EEEEEE')
        self.ax.set_facecolor('#2e2e2e')
        self.canvas.draw()

# -----------------------------
# Запуск
# -----------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    SCHEDULE_FILE = "schedule.txt"
    try:
        window = SimpleBellWindow(SCHEDULE_FILE)
        window.show()  # ← КЛЮЧЕВО: окно показывается сразу
        sys.exit(app.exec_())
    except FileNotFoundError:
        print(f"Ошибка: файл '{SCHEDULE_FILE}' не найден!")
        sys.exit(1)
