import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- Конфигурация ---
# Путь к файлу истории (изменён согласно вашему запросу)
FILENAME = r"C:\Users\student\Desktop\g.json"

# --- Предопределенные задачи ---
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть обучающее видео", "type": "учёба"},
    {"name": "Погулять на свежем воздухе", "type": "спорт"},
    {"name": "Разобрать почту", "type": "работа"},
]


class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")

        # Данные приложения
        self.history = self.load_history()
        self.all_tasks = PREDEFINED_TASKS.copy()
        self.current_task = tk.StringVar()
        self.filter_type = tk.StringVar(value="все")

        # Создание интерфейса
        self.create_widgets()
        self.update_history_display()

    # --- Логика работы с данными ---
    def load_history(self):
        """Загружает историю из JSON файла по указанному пути."""
        try:
            with open(FILENAME, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файл не существует или он пустой/битый, возвращаем пустой список
            return []

    def save_history(self):
        """Сохраняет историю в JSON файл по указанному пути."""
        # Убедимся, что директория существует (в данном случае Desktop)
        os.makedirs(os.path.dirname(FILENAME), exist_ok=True)

        with open(FILENAME, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_task_to_history(self, task_dict):
        """Добавляет задачу в историю и сохраняет её."""
        self.history.append(task_dict)
        self.save_history()

    # --- Логика генерации и фильтрации ---
    def generate_random_task(self):
        """Генерирует случайную задачу и обновляет интерфейс."""
        task = random.choice(self.all_tasks)
        self.current_task.set(task['name'])
        self.add_task_to_history(task)
        self.update_history_display()

    def add_custom_task(self):
        """Добавляет новую задачу, введённую пользователем."""
        task_name = self.entry_new_task.get().strip()

        # Проверка корректности ввода (не пустая строка)
        if not task_name:
            messagebox.showwarning("Ошибка", "Поле задачи не может быть пустым!")
            return

        task_type = self.type_var.get()
        new_task = {"name": task_name, "type": task_type}

        self.all_tasks.append(new_task)  # Добавляем в общий пул для генерации
        self.add_task_to_history(new_task)  # Сразу добавляем в историю

        self.entry_new_task.delete(0, tk.END)  # Очищаем поле ввода
        self.update_history_display()

    def update_history_display(self, *args):
        """Обновляет виджет списка истории в зависимости от фильтра."""
        selected_filter = self.filter_type.get()

        if selected_filter == "все":
            tasks_to_show = self.history
        else:
            tasks_to_show = [task for task in self.history if task['type'] == selected_filter]

        self.listbox_history.delete(0, tk.END)
        for task in tasks_to_show:
            self.listbox_history.insert(tk.END, f"{task['name']} ({task['type']})")

    # --- Создание GUI ---
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Блок генерации задачи
        frame_generate = ttk.LabelFrame(main_frame, text="Сгенерировать задачу", padding="5")
        frame_generate.pack(fill=tk.X, pady=5)

        ttk.Button(frame_generate, text="Сгенерировать задачу", command=self.generate_random_task).pack()

        ttk.Label(frame_generate, text="Текущая задача:").pack(anchor='w')

        ttk.Label(
            frame_generate,
            textvariable=self.current_task,
            font=("TkDefaultFont", 12, 'bold'),
            foreground="darkblue"
        ).pack(fill=tk.X, pady=5)

        # Блок добавления новой задачи
        frame_add = ttk.LabelFrame(main_frame, text="Добавить свою задачу", padding="5")
        frame_add.pack(fill=tk.X, pady=5)

        # Создаем фрейм для строки ввода и кнопки, чтобы положить их в одну линию
        input_frame = ttk.Frame(frame_add)
        input_frame.pack(fill=tk.X)

        self.entry_new_task = ttk.Entry(input_frame)
        self.entry_new_task.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Список типов для выпадающего меню (берём уникальные из предопределенных + 'прочее')
        types_from_tasks = sorted(list({task['type'] for task in PREDEFINED_TASKS}))
        types_from_tasks.append("прочее")
        self.type_var = tk.StringVar(value="прочее")

        ttk.OptionMenu(input_frame, self.type_var, *types_from_tasks).pack(side=tk.LEFT)

        ttk.Button(frame_add, text="Добавить", command=self.add_custom_task).pack(side=tk.RIGHT)

        # Блок фильтрации и истории
        frame_filter = ttk.Frame(main_frame)
        frame_filter.pack(fill=tk.X, pady=5)

        ttk.Label(frame_filter, text="Фильтр по типу:").pack(side=tk.LEFT)
        filter_options = ["все"] + sorted(list({task['type'] for task in self.all_tasks}))
        ttk.OptionMenu(frame_filter, self.filter_type, *filter_options,
                       command=self.update_history_display).pack(side=tk.LEFT)

        # Виджет для отображения истории (с прокруткой)
        history_frame = ttk.LabelFrame(main_frame, text="История задач", padding="5")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_history = tk.Listbox(
            history_frame,
            yscrollcommand=scrollbar.set,
            height=10,
            font=("TkDefaultFont", 10),
            selectmode=tk.SINGLE
        )
        self.listbox_history.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar.config(command=self.listbox_history.yview)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()