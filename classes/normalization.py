import os
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

class AudioProcessor:
    def __init__(self, input_folder, target_duration_ms=30000, target_dBFS=-20.0):
        self.input_folder = input_folder
        self.target_duration_ms = target_duration_ms
        self.target_dBFS = target_dBFS

    # Function to normalize the audio volume and prevent clipping
    def match_target_amplitude(self, sound):
        print(f"Original dBFS: {sound.dBFS}")
        
        # Apply compression to reduce dynamic range and normalize peaks to prevent clipping
        compressed_sound = compress_dynamic_range(sound)
        normalized_sound = normalize(compressed_sound)
        
        # Calculate the difference between current loudness and target loudness
        change_in_dBFS = self.target_dBFS - normalized_sound.dBFS
        
        # Apply gain based on the calculated difference
        adjusted_sound = normalized_sound.apply_gain(change_in_dBFS)
        
        print(f"New dBFS after adjustment: {adjusted_sound.dBFS}")
        return adjusted_sound

    # Function to loop the audio until it reaches the target duration
    def loop_audio_to_duration(self, sound):
        loops_needed = int(self.target_duration_ms / len(sound)) + 1
        extended_sound = sound * loops_needed  # Loop the sound
        return extended_sound[:self.target_duration_ms]  # Trim to exact length

    # Function to process a single audio file and convert to wav if necessary
    def process_file(self, filename):
        file_path = os.path.join(self.input_folder, filename)
        file_name, file_ext = os.path.splitext(filename)

        if not os.path.exists(file_path):
            print(f"File {filename} does not exist in {self.input_folder}.")
            return

        try:
            # Check if the file is already a .wav file; if not, convert it to .wav
            if file_ext.lower() != ".wav":
                print(f"Converting {filename} to WAV format.")
                sound = AudioSegment.from_file(file_path)  # Load file in its original format
                file_name_wav = f"{file_name}.wav"
                new_file_path = os.path.join(self.input_folder, file_name_wav)
                sound.export(new_file_path, format="wav")  # Convert to .wav
                print(f"Converted {filename} to {file_name_wav}")
            else:
                print(f"Loading WAV file: {file_path}")
                sound = AudioSegment.from_wav(file_path)
                new_file_path = file_path

            # Normalize the volume with clipping prevention and compression
            normalized_sound = self.match_target_amplitude(sound)

            # Adjust the duration
            if len(normalized_sound) > self.target_duration_ms:
                # If the file is longer than the target duration, truncate it
                final_sound = normalized_sound[:self.target_duration_ms]
            else:
                # If the file is shorter, loop the sound to fill the time
                final_sound = self.loop_audio_to_duration(normalized_sound)

            # Overwrite the original file (or the new .wav file if conversion occurred)
            final_sound.export(new_file_path, format="wav")
            print(f"Processed and saved {filename} as {file_name_wav if file_ext.lower() != '.wav' else filename}")

            # Return the new file name (with .wav extension)
            return file_name_wav if file_ext.lower() != ".wav" else filename

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            return

# Example usage
# audio_processor = AudioProcessor(input_folder="path_to_folder")
# processed_filename = audio_processor.process_file("example.mp3")
