import os
from pydub import AudioSegment
from scipy.signal import butter, lfilter
import numpy as np
import wave

class HeartSoundProcessor:
    def __init__(self, input_folder, lowcut=20, highcut=600, target_sample_rate=44100):
        self.input_folder = input_folder
        self.lowcut = lowcut
        self.highcut = highcut
        self.target_sample_rate = target_sample_rate

    # Function to apply a bandpass filter
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    # Function to apply filter to data
    def bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # Function to save filtered wave data
    def save_wave(self, output_path, data, sample_rate):
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(sample_rate)
            wf.writeframes(data.tobytes())

    # Function to reduce background noise and extract heart sound
    def process_file(self, filename):
        file_path = os.path.join(self.input_folder, filename)
        
        if not os.path.exists(file_path):
            print(f"File {filename} does not exist in {self.input_folder}.")
            return

        # Load the audio file
        sound = AudioSegment.from_wav(file_path)
        
        # Convert to raw data and get sample rate
        samples = np.array(sound.get_array_of_samples())
        sample_rate = sound.frame_rate
        
        # Apply bandpass filter to isolate heart sounds
        filtered_data = self.bandpass_filter(samples, self.lowcut, self.highcut, sample_rate)
        
        # Normalize the filtered data
        filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)

        # Save the filtered audio back as the same .wav file
        self.save_wave(file_path, filtered_data, sample_rate)
        print(f"Processed and overwritten {filename}")
