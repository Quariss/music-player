import os
import subprocess
from tkinter import Tk, filedialog
import imageio_ffmpeg as ffmpeg

# FFmpeg yolunu belirle
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

def convert_to_lower_quality(file_path, output_path):
    try:
        # ffmpeg komutunu doğrudan çalıştır
        command = [
            ffmpeg_path,
            '-i', file_path,
            '-ar', '8000',   # Örnekleme oranını 8000 Hz olarak ayarlama
            '-ac', '1',      # Mono kanala dönüştürme
            '-ab', '16k',    # Bit hızını 16 kbps olarak ayarlama
            output_path
        ]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        print(f"Düşük kaliteli dosya başarıyla oluşturuldu: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {str(e)}")

def main():
    # Tkinter kök penceresini gizle
    root = Tk()
    root.withdraw()

    # Kullanıcıdan bir dosya seçmesini iste
    file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 dosyaları", "*.mp3")])
    if file_path:
        # Kaydedilecek dosya yolunu belirle
        output_path = os.path.join(os.path.dirname(file_path), "lower_quality_" + os.path.basename(file_path))
        convert_to_lower_quality(file_path, output_path)

if __name__ == "__main__":
    main()
