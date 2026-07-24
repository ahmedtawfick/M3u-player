from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView, ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.core.audio import SoundLoader
import os

class M3UPlayerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.current_sound = None
        self.track_label = None
        self.playlist_listview = None
        
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='M3U Player',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # Current Track Display
        self.track_label = Label(
            text='No track loaded',
            size_hint_y=0.1,
            font_size='14sp',
            color=(0, 0, 1, 1)
        )
        main_layout.add_widget(self.track_label)
        
        # Playlist Display
        playlist_label = Label(
            text='Playlist:',
            size_hint_y=0.05,
            font_size='12sp'
        )
        main_layout.add_widget(playlist_label)
        
        # ScrollView for playlist
        scroll_view = ScrollView(size_hint=(1, 0.5))
        self.playlist_listview = ListView(
            adapter=None,
            size_hint_y=None
        )
        scroll_view.add_widget(self.playlist_listview)
        main_layout.add_widget(scroll_view)
        
        # Control Buttons
        button_layout = GridLayout(cols=4, size_hint_y=0.2, spacing=5)
        
        load_btn = Button(text='Load M3U', size_hint_x=0.25)
        load_btn.bind(on_press=self.load_m3u)
        button_layout.add_widget(load_btn)
        
        play_btn = Button(text='Play', size_hint_x=0.25)
        play_btn.bind(on_press=self.play)
        button_layout.add_widget(play_btn)
        
        pause_btn = Button(text='Pause', size_hint_x=0.25)
        pause_btn.bind(on_press=self.pause)
        button_layout.add_widget(pause_btn)
        
        stop_btn = Button(text='Stop', size_hint_x=0.25)
        stop_btn.bind(on_press=self.stop)
        button_layout.add_widget(stop_btn)
        
        main_layout.add_widget(button_layout)
        
        return main_layout
    
    def load_m3u(self, instance):
        """Load M3U file"""
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(
            filters=['*.m3u']
        )
        content.add_widget(file_chooser)
        
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        def select_file(path, filename):
            if filename:
                self.parse_m3u(os.path.join(path, filename[0]))
                popup.dismiss()
        
        select_btn = Button(text='Select')
        select_btn.bind(on_press=lambda x: select_file(file_chooser.path, file_chooser.selection))
        btn_layout.add_widget(select_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Load M3U File',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def parse_m3u(self, file_path):
        """Parse M3U file and load tracks"""
        self.playlist = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            playlist_dir = os.path.dirname(file_path)
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if os.path.isabs(line):
                        track_path = line
                    else:
                        track_path = os.path.join(playlist_dir, line)
                    
                    if os.path.exists(track_path):
                        self.playlist.append(track_path)
            
            self.update_playlist_display()
            self.track_label.text = f'Loaded {len(self.playlist)} tracks'
            
        except Exception as e:
            self.track_label.text = f'Error: {str(e)}'
    
    def update_playlist_display(self):
        """Update the playlist listview"""
        track_names = [os.path.basename(track) for track in self.playlist]
        
        adapter = ListAdapter(
            data=track_names,
            cls=ListItemButton,
            selection_mode='single',
            allow_empty_selection=False
        )
        
        self.playlist_listview.adapter = adapter
    
    def play(self, instance):
        """Play current track"""
        if not self.playlist:
            self.track_label.text = 'Please load an M3U file first'
            return
        
        try:
            if self.current_sound:
                self.current_sound.stop()
            
            track_path = self.playlist[self.current_index]
            self.current_sound = SoundLoader.load(track_path)
            
            if self.current_sound:
                self.current_sound.play()
                self.is_playing = True
                track_name = os.path.basename(track_path)
                self.track_label.text = f'Now Playing: {track_name}'
            else:
                self.track_label.text = 'Failed to load audio'
                
        except Exception as e:
            self.track_label.text = f'Error: {str(e)}'
    
    def pause(self, instance):
        """Pause playback"""
        if self.current_sound and self.is_playing:
            if self.current_sound.state == 'play':
                self.current_sound.stop()
                self.track_label.text = 'Paused'
            else:
                self.current_sound.play()
                self.track_label.text = 'Resumed'
    
    def stop(self, instance):
        """Stop playback"""
        if self.current_sound:
            self.current_sound.stop()
            self.is_playing = False
            self.track_label.text = 'Stopped'

if __name__ == '__main__':
    M3UPlayerApp().run()
