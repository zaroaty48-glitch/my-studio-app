import os
import threading
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.clock import Clock

class StudioProApp(BoxLayout):
    def __init__(self, **kwargs):
        super(StudioProApp, __init__)(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.selected_file = None

        # Header
        self.add_widget(Label(
            text='[b]MyStudio Pro 4K - CapCut Suite[/b]', 
            markup=True, font_size='22sp', size_hint_y=None, height=40
        ))

        # File Select Button
        self.btn_select = Button(
            text='📁 اختر فيديو من الجهاز', size_hint_y=None, height=45,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.btn_select.bind(on_press=self.open_file_chooser)
        self.add_widget(self.btn_select)

        self.status_label = Label(text='لم يتم اختيار فيديو', font_size='14sp', size_hint_y=None, height=30)
        self.add_widget(self.status_label)

        # Scrollable Options Area
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # --- Section 1: 4K & Quality Enhancements ---
        content.add_widget(Label(text='[b]✨ تحسين الجودة والدقة الفائقة[/b]', markup=True, size_hint_y=None, height=30))
        grid_qual = GridLayout(cols=2, spacing=8, size_hint_y=None, height=140)
        
        self.btn_hd = Button(text='💎 تحسين الجودة HD', on_press=lambda x: self.process_preset('hd'))
        self.btn_noise = Button(text='🔇 تقليل تشويش الصورة', on_press=lambda x: self.process_preset('denoise'))
        self.btn_stab = Button(text='📐 تثبيت الصورة (Stabilize)', on_press=lambda x: self.process_preset('stab'))
        self.btn_optical = Button(text='🌊 التدفق البصري (Slow-Mo)', on_press=lambda x: self.process_preset('optical'))
        self.btn_flicker = Button(text='⚡ إزالة الومضات', on_press=lambda x: self.process_preset('flicker'))
        self.btn_super4k = Button(text='🚀 الدقة الفائقة 4K AI', on_press=lambda x: self.process_preset('4k_ai'))

        for b in [self.btn_hd, self.btn_noise, self.btn_stab, self.btn_optical, self.btn_flicker, self.btn_super4k]:
            grid_qual.add_widget(b)
        content.add_widget(grid_qual)

        # --- Section 2: Color & Image Adjustments (الضبط) ---
        content.add_widget(Label(text='[b]🎨 أدوات الضبط والتخصيص[/b]', markup=True, size_hint_y=None, height=30))
        
        # Brightness & Contrast & Sharpen Controls
        content.add_widget(Label(text='زيادة الحدة (Sharpen / Clarity)', size_hint_y=None, height=20))
        self.slide_sharp = Slider(min=0, max=5, value=1, size_hint_y=None, height=30)
        content.add_widget(self.slide_sharp)

        content.add_widget(Label(text='السطوع والتباين (Brightness & Contrast)', size_hint_y=None, height=20))
        self.slide_contrast = Slider(min=0.5, max=2.0, value=1.1, size_hint_y=None, height=30)
        content.add_widget(self.slide_contrast)

        content.add_widget(Label(text='درجة الحرارة والألوان (Warmth & Saturation)', size_hint_y=None, height=20))
        self.slide_sat = Slider(min=0.0, max=2.5, value=1.2, size_hint_y=None, height=30)
        content.add_widget(self.slide_sat)

        # --- Section 3: Export Settings (إعدادات التصدير) ---
        content.add_widget(Label(text='[b]⚙️ إعدادات التصدير (Export Settings)[/b]', markup=True, size_hint_y=None, height=30))
        
        grid_exp = GridLayout(cols=2, spacing=8, size_hint_y=None, height=90)
        self.btn_res_1080 = Button(text='1080p (Full HD)', background_color=(0.3, 0.8, 0.3, 1))
        self.btn_res_4k = Button(text='2K / 4K Ultra', background_color=(0.9, 0.2, 0.4, 1))
        self.btn_fps_60 = Button(text='60 FPS (سلاسة فائقة)')
        self.btn_bitrate_high = Button(text='Bitrate عالي (18+ Mbps)')

        for b in [self.btn_res_1080, self.btn_res_4k, self.btn_fps_60, self.btn_bitrate_high]:
            grid_exp.add_widget(b)
        content.add_widget(grid_exp)

        scroll.add_widget(content)
        self.add_widget(scroll)

        # Export Action Button
        self.btn_export = Button(
            text='🎬 تصدير الفيديو النهائي (Export)', size_hint_y=None, height=50,
            background_color=(0, 0.8, 0.4, 1), font_size='18sp'
        )
        self.btn_export.bind(on_press=lambda x: self.process_preset('full_custom'))
        self.add_widget(self.btn_export)

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView(filters=['*.mp4', '*.mkv', '*.avi', '*.mov'])
        content.add_widget(file_chooser)
        
        btn_layout = BoxLayout(size_hint_y=0.2)
        btn_confirm = Button(text='تأكيد')
        btn_cancel = Button(text='إلغاء')
        btn_layout.add_widget(btn_confirm)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup = Popup(title='اختر فيديو', content=content, size_hint=(0.9, 0.9))

        def confirm(instance):
            if file_chooser.selection:
                self.selected_file = file_chooser.selection[0]
                self.status_label.text = f"تم اختيار: {os.path.basename(self.selected_file)}"
            popup.dismiss()

        btn_confirm.bind(on_press=confirm)
        btn_cancel.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def process_preset(self, mode):
        if not self.selected_file:
            self.status_label.text = "⚠️ اختر فيديو أولاً!"
            return

        self.status_label.text = "⚙️ جاري معالجة وتصدير الفيديو... يرجى الانتظار"
        threading.Thread(target=self.run_ffmpeg_pipeline, args=(mode,)).start()

    def run_ffmpeg_pipeline(self, mode):
        out_dir = "/sdcard/Download"
        if not os.path.exists(out_dir):
            out_dir = os.path.expanduser("~")
        
        output_file = os.path.join(out_dir, f"CapCut_Pro_{mode}_{os.path.basename(self.selected_file)}")

        # Build FFmpeg filters dynamically
        sharp_val = self.slide_sharp.value
        cont_val = self.slide_contrast.value
        sat_val = self.slide_sat.value

        vf_list = [f"eq=contrast={cont_val}:saturation={sat_val}"]

        if sharp_val > 0:
            vf_list.append(f"unsharp=5:5:{sharp_val}:5:5:0.0")

        if mode == 'hd' or mode == '4k_ai':
            vf_list.append("scale=3840:2160:flags=lanczos") # 4K Upscale
        elif mode == 'denoise':
            vf_list.append("hqdn3d=1.5:1.5:6:6") # Noise reduction
        elif mode == 'optical':
            vf_list.append("minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60'") # Optical flow 60fps

        vf_str = ",".join(vf_list)

        cmd = [
            'ffmpeg', '-y', '-i', self.selected_file,
            '-vf', vf_str,
            '-c:v', 'libx264', '-crf', '16', '-preset', 'fast',
            '-c:a', 'copy',
            output_file
        ]

        try:
            subprocess.run(cmd, check=True)
            Clock.schedule_once(lambda dt: self.update_success(output_file))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_error(str(e)))

    def update_success(self, file_path):
        self.status_label.text = f"✅ تم التصدير بنجاح إلى:\n{file_path}"

    def update_error(self, err):
        self.status_label.text = f"❌ خطأ بالمعالجة: {err}"

class MainApp(App):
    def build(self):
        return StudioProApp()

if __name__ == '__main__':
    MainApp().run()
