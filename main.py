import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Предопределённые задачи
        self.default_tasks = [
            {"name": "Прочитать статью", "type": "учёба"},
            {"name": "Сделать зарядку", "type": "спорт"},
            {"name": "Написать отчёт", "type": "работа"},
            {"name": "Выучить 10 слов", "type": "учёба"},
            {"name": "Пробежка 3 км", "type": "спорт"},
            {"name": "Проверить email", "type": "работа"},
            {"name": "Посмотреть лекцию", "type": "учёба"},
            {"name": "Отжимания 30 раз", "type": "спорт"},
            {"name": "Созвониться с клиентом", "type": "работа"}
        ]
        
        # Загрузка задач и истории
        self.tasks = self.load_tasks()
        self.history = self.load_history()
        self.current_filter = "все"
        
        self.setup_ui()
        self.update_task_list()
        self.update_history_list()
    
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Верхняя панель: Генерация задачи ===
        gen_frame = ttk.LabelFrame(main_frame, text="Генератор задач", padding="10")
        gen_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.task_var = tk.StringVar()
        self.task_label = ttk.Label(gen_frame, textvariable=self.task_var, font=("Arial", 14, "bold"))
        self.task_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.generate_btn = ttk.Button(gen_frame, text="🎲 Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.grid(row=0, column=1, padx=10, pady=5)
        
        # === Панель фильтрации ===
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(filter_frame, text="Тип задачи:").grid(row=0, column=0, padx=5)
        self.filter_type = tk.StringVar(value="все")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type, 
                                    values=["все", "учёба", "спорт", "работа"], state="readonly")
        filter_combo.grid(row=0, column=1, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # === Список доступных задач ===
        tasks_frame = ttk.LabelFrame(main_frame, text="Доступные задачи", padding="10")
        tasks_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.tasks_listbox = tk.Listbox(tasks_frame, height=8, width=35)
        self.tasks_listbox.grid(row=0, column=0, padx=5, pady=5)
        
        scroll_tasks = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        scroll_tasks.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tasks_listbox.config(yscrollcommand=scroll_tasks.set)
        
        # Кнопки управления задачами
        btn_frame = ttk.Frame(tasks_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="➕ Добавить задачу", command=self.add_task_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✖ Удалить задачу", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        
        # === История задач ===
        history_frame = ttk.LabelFrame(main_frame, text="История задач", padding="10")
        history_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.history_listbox = tk.Listbox(history_frame, height=8, width=35)
        self.history_listbox.grid(row=0, column=0, padx=5, pady=5)
        
        scroll_history = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scroll_history.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.config(yscrollcommand=scroll_history.set)
        
        ttk.Button(history_frame, text="🗑 Очистить историю", command=self.clear_history).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Нижняя панель
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.status_var = tk.StringVar(value="Готов к работе")
        ttk.Label(status_frame, textvariable=self.status_var, foreground="gray").pack(side=tk.LEFT)
        
        ttk.Button(status_frame, text="💾 Сохранить всё", command=self.save_all).pack(side=tk.RIGHT, padx=5)
    
    def load_tasks(self):
        """Загрузка задач из JSON"""
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return self.default_tasks.copy()
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        """Сохранение задач в JSON"""
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def save_history(self):
        """Сохранение истории в JSON"""
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def save_all(self):
        """Сохранить всё"""
        self.save_tasks()
        self.save_history()
        self.status_var.set("Все данные сохранены!")
        self.root.after(2000, lambda: self.status_var.set("Готов к работе"))
    
    def generate_task(self):
        """Генерация случайной задачи с учётом фильтра"""
        available_tasks = self.get_filtered_tasks()
        
        if not available_tasks:
            messagebox.showwarning("Нет задач", "Нет задач выбранного типа!")
            return
        
        task = random.choice(available_tasks)
        task_with_date = {
            "name": task["name"],
            "type": task["type"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.history.insert(0, task_with_date)  # Новые задачи сверху
        self.task_var.set(f"📌 {task['name']} ({task['type']})")
        self.status_var.set(f"Сгенерирована задача: {task['name']}")
        
        self.save_history()
        self.update_history_list()
    
    def get_filtered_tasks(self):
        """Получить задачи с учётом фильтра"""
        if self.current_filter == "все":
            return self.tasks
        return [t for t in self.tasks if t["type"] == self.current_filter]
    
    def on_filter_change(self, event=None):
        """Обработчик изменения фильтра"""
        self.current_filter = self.filter_type.get()
        self.update_task_list()
        self.status_var.set(f"Фильтр: {self.current_filter}")
    
    def update_task_list(self):
        """Обновить список доступных задач"""
        self.tasks_listbox.delete(0, tk.END)
        filtered = self.get_filtered_tasks()
        for task in filtered:
            self.tasks_listbox.insert(tk.END, f"{task['name']} [{task['type']}]")
    
    def update_history_list(self):
        """Обновить список истории"""
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, f"{item['date']} - {item['name']} ({item['type']})")
    
    def add_task_dialog(self):
        """Диалог добавления новой задачи"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить задачу")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Название задачи:").pack(pady=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Тип задачи:").pack(pady=10)
        type_var = tk.StringVar(value="учёба")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, values=["учёба", "спорт", "работа"])
        type_combo.pack(pady=5)
        
        def add():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Ошибка", "Название задачи не может быть пустым!")
                return
            
            self.tasks.append({"name": name, "type": type_var.get()})
            self.save_tasks()
            self.update_task_list()
            self.status_var.set(f"Добавлена задача: {name}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Добавить", command=add).pack(pady=20)
    
    def delete_task(self):
        """Удалить выбранную задачу"""
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления!")
            return
        
        filtered = self.get_filtered_tasks()
        task_to_delete = filtered[selection[0]]
        
        # Находим и удаляем из основного списка
        for i, task in enumerate(self.tasks):
            if task["name"] == task_to_delete["name"] and task["type"] == task_to_delete["type"]:
                del self.tasks[i]
                break
        
        self.save_tasks()
        self.update_task_list()
        self.status_var.set(f"Удалена задача: {task_to_delete['name']}")
    
    def clear_history(self):
        """Очистить историю"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_list()
            self.task_var.set("")
            self.status_var.set("История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()