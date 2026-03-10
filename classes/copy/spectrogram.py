import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

class SpectrogramProcessor:
    def __init__(self, input_dir, output_dir, target_sr=16000, target_duration=30.0):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_sr = target_sr
        self.target_duration = target_duration

        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    # Function to preprocess and generate spectrogram for a single file
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

        # Generate the spectrogram
        spectrogram = librosa.feature.melspectrogram(y=audio, sr=self.target_sr, n_mels=128)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

        # Plot and save the spectrogram as an image
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(spectrogram_db, sr=self.target_sr, x_axis=None, y_axis=None)
        plt.axis('off')  # Remove axes labels and ticks
        plt.tight_layout(pad=0)

        # Save the spectrogram image in the output directory
        output_file = os.path.join(self.output_dir, f"{os.path.splitext(filename)[0]}_spectrogram.png")
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
        plt.close('all')

        return output_file