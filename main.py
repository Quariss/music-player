import os
import tkinter as tk
from tkinter import filedialog
import pygame
from tkinter import ttk
from pydub import AudioSegment


class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Müzik Çalar")

        # Müzik listesi
        self.playlist = []

        # Pygame başlat
        pygame.init()

        # Arayüzü oluştur
        self.create_widgets()

        # Müzik çalma durumunu takip etmek için bir değişken
        self.playing = False

    def create_widgets(self):
        # Müzik ekleme düğmesi
        self.add_button = tk.Button(self.root, text="Müzik Ekle", command=self.add_music)
        self.add_button.pack(pady=20)

        # Müzik listesi oluştur
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)

        # ProgressBar
        self.progressbar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=200, mode="determinate")
        self.progressbar.pack(pady=10)

        # Oynat, durdur
        self.play_button = tk.Button(self.root, text="Oynat", command=self.play_pause_music)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.root, text="Durdur", command=self.stop_music)
        self.stop_button.pack(side=tk.LEFT, padx=10)

    def add_music(self):
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 dosyaları", "*.mp3")])
        if file_path:
            self.playlist.append(file_path)
            self.listbox.insert(tk.END, os.path.basename(file_path))

    def play_pause_music(self):
        if not self.playlist:
            return

        selected_index = self.listbox.curselection()
        if selected_index:
            selected_music = self.playlist[selected_index[0]]
            if not self.playing:
                pygame.mixer.music.load(selected_music)
                pygame.mixer.music.play()
                self.play_button.config(text="Duraklat")
                self.playing = True
                self.update_progressbar()
            else:
                pygame.mixer.music.pause()
                self.play_button.config(text="Oynat")
                self.playing = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.play_button.config(text="Oynat")
        self.playing = False
        self.progressbar.stop()

    def update_progressbar(self):
        if pygame.mixer.music.get_busy():
            current_position = pygame.mixer.music.get_pos() / 1000  # Müzik pozisyonunu saniye cinsinden al
            music_length = pygame.mixer.Sound(self.playlist[self.listbox.curselection()[0]]).get_length()  # Müzik'in uzunluğunu saniye cinsinden aldık
            if music_length > 0:
                progress = (current_position / music_length) * 100
                self.progressbar["value"] = progress
            self.root.after(1000, self.update_progressbar)  # Her saniyede bir güncelle

    def convert_to_lower_quality(self,file_path):
        try:
            audio = AudioSegment.from_mp3(file_path)
            # Örnek olarak sesi daha düşük kaliteye dönüştürme ( bit hızını düşürme)
            lower_quality_audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(1)
            # Dönüştürülen sesi geçiçi bir dosya olarak kaydet
            lower_quality_file_path = "lower_quality_" + os.path.basename(file_path)
            lower_quality_audio.export((lower_quality_file_path), format="mp3")
            return lower_quality_file_path
            return lower_quality_audio
        except Exception as e:
            print(f"Hata oluştu : {str(e)}")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()

