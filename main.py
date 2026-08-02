from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MyStudioApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.label = Label(
            text="🎬 My Studio Pro", 
            font_size='24sp', 
            bold=True,
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.label)
        
        btn_blur = Button(
            text="✨ Canvas Blur (Reels)", 
            background_color=(0.06, 0.72, 0.51, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(btn_blur)
        
        btn_trim = Button(
            text="✂️ Cut Video", 
            background_color=(0.96, 0.62, 0.04, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(btn_trim)
        
        btn_4k = Button(
            text="💎 Apply 4K / Sharp Filter", 
            background_color=(0.54, 0.36, 0.96, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(btn_4k)
        
        return layout

if __name__ == '__main__':
    MyStudioApp().run()
