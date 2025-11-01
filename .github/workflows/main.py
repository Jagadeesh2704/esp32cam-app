__version__ = '1.0'

import io
import os
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class ESP32SetupApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # Title
        self.add_widget(Label(text='ESP32-CAM Setup', font_size=28, size_hint_y=0.12))
        
        # Time display
        self.time_label = Label(text='', font_size=16, size_hint_y=0.08)
        self.add_widget(self.time_label)
        
        # IP Input
        ip_box = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        ip_box.add_widget(Label(text='ESP32 IP:', size_hint_x=0.3))
        self.ip_input = TextInput(text='http://172.16.1.169', multiline=False, size_hint_x=0.7)
        ip_box.add_widget(self.ip_input)
        self.add_widget(ip_box)
        
        # ROI Section
        self.add_widget(Label(text='Region of Interest', font_size=20, size_hint_y=0.1))
        
        roi_grid = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=5)
        
        # X
        x_box = BoxLayout(orientation='horizontal', spacing=10)
        x_box.add_widget(Label(text='X:', size_hint_x=0.2))
        self.x_input = TextInput(text='0', multiline=False, input_filter='int')
        x_box.add_widget(self.x_input)
        roi_grid.add_widget(x_box)
        
        # Y
        y_box = BoxLayout(orientation='horizontal', spacing=10)
        y_box.add_widget(Label(text='Y:', size_hint_x=0.2))
        self.y_input = TextInput(text='0', multiline=False, input_filter='int')
        y_box.add_widget(self.y_input)
        roi_grid.add_widget(y_box)
        
        # Width
        w_box = BoxLayout(orientation='horizontal', spacing=10)
        w_box.add_widget(Label(text='Width:', size_hint_x=0.2))
        self.w_input = TextInput(text='100', multiline=False, input_filter='int')
        w_box.add_widget(self.w_input)
        roi_grid.add_widget(w_box)
        
        # Height
        h_box = BoxLayout(orientation='horizontal', spacing=10)
        h_box.add_widget(Label(text='Height:', size_hint_x=0.2))
        self.h_input = TextInput(text='100', multiline=False, input_filter='int')
        h_box.add_widget(self.h_input)
        roi_grid.add_widget(h_box)
        
        self.add_widget(roi_grid)
        
        # Buttons
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        save_btn = Button(text='Save ROI')
        save_btn.bind(on_press=self.save_roi)
        btn_box.add_widget(save_btn)
        
        load_btn = Button(text='Load ROI')
        load_btn.bind(on_press=self.load_roi)
        btn_box.add_widget(load_btn)
        
        self.add_widget(btn_box)
        
        # Status
        self.status = Label(text='Ready', font_size=16, size_hint_y=0.15)
        self.add_widget(self.status)
        
        Clock.schedule_interval(self.update_time, 1)
        self.load_roi(None)
    
    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save_roi(self, instance):
        try:
            roi_data = {
                'x': int(self.x_input.text),
                'y': int(self.y_input.text),
                'w': int(self.w_input.text),
                'h': int(self.h_input.text),
                'ip': self.ip_input.text
            }
            
            with open('roi_settings.json', 'w') as f:
                json.dump(roi_data, f)
            
            self.status.text = f"✓ ROI saved: {roi_data['x']},{roi_data['y']} {roi_data['w']}x{roi_data['h']}"
        except Exception as e:
            self.status.text = f"Error: {str(e)}"
    
    def load_roi(self, instance):
        try:
            if os.path.exists('roi_settings.json'):
                with open('roi_settings.json', 'r') as f:
                    roi_data = json.load(f)
                
                self.x_input.text = str(roi_data.get('x', 0))
                self.y_input.text = str(roi_data.get('y', 0))
                self.w_input.text = str(roi_data.get('w', 100))
                self.h_input.text = str(roi_data.get('h', 100))
                self.ip_input.text = roi_data.get('ip', 'http://172.16.1.169')
                
                self.status.text = "✓ ROI loaded"
            else:
                self.status.text = "No saved ROI"
        except Exception as e:
            self.status.text = f"Load error: {str(e)}"

class ESP32ConfigApp(App):
    def build(self):
        self.title = 'ESP32-CAM Config'
        return ESP32SetupApp()

if __name__ == '__main__':
    ESP32ConfigApp().run()
