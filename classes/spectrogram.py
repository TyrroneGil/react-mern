import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend('Agg')

class SpectrogramProcessor:
    def __init__(self, input_dir, output_dir, target_sr=30000, target_duration=30.0):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_sr = target_sr
        self.target_duration = target_duration

        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    # Function to preprocess and generate both waveform and spectrogram for a single file
    def process_file(self, filename):
        file_path = os.path.join(self.input_dir, filename)
        print(f"Processing {filename}...")

        # Load the audio file
        audio, sr = librosa.load(file_path, sr=None)

        # Resample to the target sampling rate if needed
        if sr != self.target_sr:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=self.target_sr)

        # Normalize the audio
        audio = audio / np.max(np.abs(audio))

        # Trim or pad to the target duration
        max_length = int(self.target_sr * self.target_duration)
        if len(audio) > max_length:
            audio = audio[:max_length]
        else:
            padding = max_length - len(audio)
            audio = np.pad(audio, (0, padding), 'constant')

        # 1. Generate and save the waveform with a white background and blue line
        plt.figure(figsize=(10, 4))
        plt.gca().set_facecolor("white")
        librosa.display.waveshow(audio, sr=self.target_sr, color="blue")
        plt.axis('off')  # Remove axes for a clean look
        output_file_waveform = os.path.join(self.output_dir, f"{os.path.splitext(filename)[0]}_waveform_white.png")
        plt.savefig(output_file_waveform, bbox_inches='tight', pad_inches=0, facecolor="white")
        plt.close()

        # 2. Generate and save the spectrogram with a black background and red-orange colormap
        spectrogram = librosa.feature.melspectrogram(y=audio, sr=self.target_sr, n_mels=128)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

        plt.figure(figsize=(10, 4))
        plt.gca().set_facecolor("black")
        librosa.display.specshow(spectrogram_db, sr=self.target_sr, x_axis=None, y_axis=None, cmap="inferno")
        plt.axis('off')
        output_file_spectrogram = os.path.join(self.output_dir, f"{os.path.splitext(filename)[0]}_spectrogram_black.png")
        plt.savefig(output_file_spectrogram, bbox_inches='tight', pad_inches=0, facecolor="black")
        plt.close()

        return output_file_waveform, output_file_spectrogram
