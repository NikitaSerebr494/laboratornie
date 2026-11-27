"""Необязательный графический просмотр и поиск (дополнительное задание).

Консольная версия из main.py остаётся основной. Запуск: python gui.py
"""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from logic import find_records, statistics, validate_records
from storage import load_records

DATA_PATH = Path(__file__).resolve().parent / "data.json"


class App:
    def __init__(self, root, records):
        self.root = root
        self.records = records
        root.title("Печатные заказы")
        root.geometry("720x420")

        panel = ttk.Frame(root, padding=8)
        panel.pack(fill="x")

        ttk.Label(panel, text="Поиск по названию:").pack(side="left")
        self.query = tk.StringVar()
        entry = ttk.Entry(panel, textvariable=self.query)
        entry.pack(side="left", fill="x", expand=True, padx=6)
        entry.bind("<Return>", lambda event: self.show_found())
        ttk.Button(panel, text="Найти", command=self.show_found).pack(side="left")
        ttk.Button(panel, text="Все записи", command=self.show_all).pack(side="left", padx=6)

        self.table = ttk.Treeview(
            root,
            columns=("id", "title", "category", "amount", "status"),
            show="headings",
            height=12,
        )
        headings = {
            "id": ("ID", 50),
            "title": ("Название", 240),
            "category": ("Категория", 150),
            "amount": ("Страниц", 80),
            "status": ("Статус", 130),
        }
        for column, (text, width) in headings.items():
            self.table.heading(column, text=text)
            self.table.column(column, width=width, anchor="w")
        self.table.pack(fill="both", expand=True, padx=8)

        self.status = tk.StringVar()
        ttk.Label(root, textvariable=self.status, padding=8).pack(fill="x")
        self.show_all()

    def fill(self, records):
        for item in self.table.get_children():
            self.table.delete(item)
        for record in records:
            status = "напечатан" if record["completed"] else "не напечатан"
            self.table.insert(
                "",
                "end",
                values=(
                    record["id"],
                    record["title"],
                    record["category"],
                    record["amount"],
                    status,
                ),
            )
        stats = statistics(records)
        self.status.set(
            f"Всего: {stats['total']}, напечатано: {stats['completed']}, "
            f"не напечатано: {stats['pending']}, сумма страниц: {stats['amount']}"
        )

    def show_all(self):
        self.query.set("")
        self.fill(self.records)

    def show_found(self):
        query = self.query.get().strip()
        if not query:
            messagebox.showinfo("Поиск", "Введите часть названия.")
            return
        found = find_records(self.records, query)
        if not found:
            messagebox.showinfo("Поиск", "Ничего не найдено.")
            return
        self.fill(found)


def main():
    warning = ""
    try:
        records = load_records(DATA_PATH)
        validate_records(records)
    except FileNotFoundError:
        records = []
        warning = "Файл data.json не найден, показан пустой список."
    except (ValueError, OSError) as error:
        records = []
        warning = f"Данные не загружены: {error}"

    root = tk.Tk()
    App(root, records)
    if warning:
        messagebox.showwarning("Данные", warning)
    root.mainloop()


if __name__ == "__main__":
    main()
