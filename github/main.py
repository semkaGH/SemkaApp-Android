from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import urllib.request
import threading

class SemkaApp(App):
    def build(self):
        self.title = "SemkaApp"
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Заголовок (в твоем стиле)
        layout.add_widget(Label(text="📢 SemkaApp - Новости", font_size='22sp', size_hint_y=None, height=60))

        # Текстовая область
        self.scroll = ScrollView()
        self.news_label = Label(text="Нажмите 'Обновить'...", size_hint_y=None, halign='left', valign='top', text_size=(None, None))
        self.news_label.bind(texture_size=self.news_label.setter('size'))
        self.scroll.add_widget(self.news_label)
        layout.add_widget(self.scroll)

        # Кнопка
        self.btn = Button(text="🔄 ОБНОВИТЬ", size_hint_y=None, height=70, background_color=(0.15, 0.65, 0.27, 1))
        self.btn.bind(on_press=self.start_loading)
        layout.add_widget(self.btn)

        return layout

    def start_loading(self, *args):
        self.news_label.text = "⏳ Загрузка..."
        threading.Thread(target=self.fetch_data, daemon=True).start()

    def fetch_data(self):
        try:
            req = urllib.request.Request("https://pastebin.com/raw/2V7sWegJ", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                text = response.read().decode('utf-8')
            Clock.schedule_once(lambda dt: self.show_text(text))
        except:
            Clock.schedule_once(lambda dt: self.show_text("❌ Ошибка сети"))

    def show_text(self, text):
        self.news_label.text = text

if __name__ == "__main__":
    SemkaApp().run()