import customtkinter as ctk
import urllib.request
import threading
from tkinter import messagebox
from datetime import datetime
import os
import sys

# Определяем путь к папке, где лежит сам скрипт
if getattr(sys, 'frozen', False):
    # Если запущено как .exe
    base_path = sys._MEIPASS
else:
    # Если запущено как .py
    base_path = os.path.dirname(__file__)

icon_path = os.path.join(base_path, "icon.ico")

# Настройки
PASTEBIN_URL = "https://pastebin.com/raw/2V7sWegJ"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SemkaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(icon_path)

        self.title("📢 SemkaApp")
        self.geometry("700x550")
        
        # --- ВОТ ЭТА СТРОКА ДОБАВЛЯЕТ ИКОНКУ ---
        # Убедись, что файл icon.ico лежит в той же папке, что и скрипт
        try:
            self.after(200, lambda: self.iconbitmap("icon.ico")) 
        except:
            pass # Если файла нет, приложение просто запустится со стандартным значком
        
        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- 1. ВЕРХНЯЯ ПАНЕЛЬ (Заголовок и Поиск) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        self.title_label = ctk.CTkLabel(self.header_frame, text="📰 НОВОСТИ КАНАЛА", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(side="left")

        # Поле поиска - очень удобно, если новостей много
        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Найти в тексте...", width=220)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self.search_text)

        # --- 2. ТЕКСТОВОЕ ПОЛЕ (Новости) ---
        self.news_text = ctk.CTkTextbox(
            self, 
            font=ctk.CTkFont(family="Consolas", size=14), 
            border_width=2, 
            border_color="#8C00FF"
        )
        self.news_text.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.news_text.insert("0.0", "Ожидание загрузки...")
        self.news_text.configure(state="disabled")

        # --- 3. НИЖНЯЯ ПАНЕЛЬ (Кнопки и Статус) ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.update_btn = ctk.CTkButton(
            self.bottom_frame, 
            text="🔄 ОБНОВИТЬ", 
            fg_color="#28a745", 
            hover_color="#218838",
            command=self.start_load_news
        )
        self.update_btn.pack(side="left")

        self.status_label = ctk.CTkLabel(self.bottom_frame, text="✨ Готов")
        self.status_label.pack(side="left", padx=20)

        self.info_btn = ctk.CTkButton(self.bottom_frame, text="ℹ", width=40, command=self.show_info)
        self.info_btn.pack(side="right", padx=5)

        self.exit_btn = ctk.CTkButton(self.bottom_frame, text="✕ ВЫХОД", fg_color="#dc3545", command=self.destroy)
        self.exit_btn.pack(side="right", padx=5)

        # Авто-загрузка при старте
        self.start_load_news()

    def search_text(self, event=None):
        """Мгновенный поиск и подсветка текста"""
        query = self.search_entry.get().lower()
        self.news_text.tag_remove("highlight", "1.0", "end")
        
        if query and len(query) > 1: # Ищем если введено больше 1 символа
            start_pos = "1.0"
            while True:
                start_pos = self.news_text.search(query, start_pos, stopindex="end", nocase=True)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(query)}c"
                self.news_text.tag_add("highlight", start_pos, end_pos)
                self.news_text.tag_config("highlight", foreground="black", background="#FFCC00")
                start_pos = end_pos

    def start_load_news(self):
        """Запуск загрузки в фоне"""
        self.status_label.configure(text="⏳ Загрузка...", text_color="yellow")
        self.update_btn.configure(state="disabled")
        threading.Thread(target=self.load_news_logic, daemon=True).start()

    def load_news_logic(self):
        """Запрос к Pastebin"""
        try:
            req = urllib.request.Request(PASTEBIN_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('utf-8')
            self.after(0, lambda: self.update_ui(content))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text="❌ Ошибка сети", text_color="#dc3545"))
            self.after(0, lambda: self.update_btn.configure(state="normal"))

    def update_ui(self, content):
        """Отображение результата"""
        now = datetime.now().strftime("%H:%M")
        self.news_text.configure(state="normal")
        self.news_text.delete("1.0", "end")
        self.news_text.insert("1.0", content)
        self.news_text.configure(state="disabled")
        self.status_label.configure(text=f"✅ Обновлено в {now}", text_color="#28a745")
        self.update_btn.configure(state="normal")

    def show_info(self):
        messagebox.showinfo("SemkaApp", "Версия 0.1\nАвтор: @plsemen\n\nПриложение для мониторинга новостей канала.")

if __name__ == "__main__":
    app = SemkaApp()
    app.mainloop()
