import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
from pathlib import Path

class M3UPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("M3U Player")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Variables
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.current_file = None
        
        # UI Setup
        self.setup_ui()
        
    def setup_ui(self):
        """Create the UI components"""
        # Title Label
        title_label = tk.Label(
            self.root, 
            text="M3U Player", 
            font=("Arial", 24, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Current Track Label
        self.track_label = tk.Label(
            self.root,
            text="No track loaded",
            font=("Arial", 12),
            fg="blue",
            wraplength=550,
            pady=10
        )
        self.track_label.pack()
        
        # Playlist Frame
        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        playlist_label = tk.Label(playlist_frame, text="Playlist:", font=("Arial", 10, "bold"))
        playlist_label.pack(anchor="w")
        
        # Listbox with Scrollbar
        scrollbar = tk.Scrollbar(playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_listbox = tk.Listbox(
            playlist_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=10
        )
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.playlist_listbox.yview)
        
        # Control Buttons Frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=15)
        
        self.load_btn = tk.Button(
            control_frame,
            text="Load M3U",
            command=self.load_m3u,
            width=12,
            font=("Arial", 10)
        )
        self.load_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = tk.Button(
            control_frame,
            text="Play",
            command=self.play,
            width=12,
            font=("Arial", 10)
        )
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.pause_btn = tk.Button(
            control_frame,
            text="Pause",
            command=self.pause,
            width=12,
            font=("Arial", 10)
        )
        self.pause_btn.grid(row=0, column=2, padx=5)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="Stop",
            command=self.stop,
            width=12,
            font=("Arial", 10)
        )
        self.stop_btn.grid(row=0, column=3, padx=5)
        
    def load_m3u(self):
        """Load M3U file and parse playlist"""
        file_path = filedialog.askopenfilename(
            title="Select M3U file",
            filetypes=[("M3U files", "*.m3u"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.playlist = []
        self.playlist_listbox.delete(0, tk.END)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            playlist_dir = os.path.dirname(file_path)
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle relative and absolute paths
                    if os.path.isabs(line):
                        track_path = line
                    else:
                        track_path = os.path.join(playlist_dir, line)
                    
                    if os.path.exists(track_path):
                        track_name = os.path.basename(track_path)
                        self.playlist.append(track_path)
                        self.playlist_listbox.insert(tk.END, track_name)
            
            if self.playlist:
                messagebox.showinfo("Success", f"Loaded {len(self.playlist)} tracks")
                self.current_index = 0
            else:
                messagebox.showwarning("Warning", "No valid tracks found in M3U file")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load M3U file:\n{str(e)}")
    
    def play(self):
        """Play the selected track"""
        if not self.playlist:
            messagebox.showwarning("Warning", "Please load an M3U file first")
            return
        
        try:
            if not self.is_playing:
                track_path = self.playlist[self.current_index]
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
                self.is_playing = True
                
                track_name = os.path.basename(track_path)
                self.track_label.config(text=f"Now Playing: {track_name}")
                self.playlist_listbox.selection_clear(0, tk.END)
                self.playlist_listbox.selection_set(self.current_index)
                self.playlist_listbox.see(self.current_index)
            else:
                pygame.mixer.music.unpause()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play track:\n{str(e)}")
    
    def pause(self):
        """Pause the current track"""
        if self.is_playing:
            pygame.mixer.music.pause()
    
    def stop(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.track_label.config(text="No track loaded")
        self.playlist_listbox.selection_clear(0, tk.END)

def main():
    root = tk.Tk()
    app = M3UPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
