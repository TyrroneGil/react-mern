import os
from pydub import AudioSegment

class AudioProcessor:
    def __init__(self, input_folder, target_duration_ms=30000, target_dBFS=-20.0):
        self.input_folder = input_folder
        self.target_duration_ms = target_duration_ms
        self.target_dBFS = target_dBFS

    # Function to normalize the audio volume
    def match_target_amplitude(self, sound):
        change_in_dBFS = self.target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    # Function to loop the audio until it reaches the target duration
    def loop_audio_to_duration(self, sound):
        loops_needed = int(self.target_duration_ms / len(sound)) + 1
        extended_sound = sound * loops_needed  # Loop the sound
        return extended_sound[:self.target_duration_ms]  # Trim to exact length

    # Function to process a single audio file and overwrite it
    def process_file(self, filename):
        file_path = os.path.join(self.input_folder, filename)
        
        if not os.path.exists(file_path):
            print(f"File {filename} does not exist in {self.input_folder}.")
            return

        sound = AudioSegment.from_wav(file_path)

        # Normalize the volume
        normalized_sound = self.match_target_amplitude(sound)

        # Adjust the duration
        if len(normalized_sound) > self.target_duration_ms:
            # If the file is longer than the target duration, truncate it
            final_sound = normalized_sound[:self.target_duration_ms]
        else:
            # If the file is shorter, loop the sound to fill the time
            final_sound = self.loop_audio_to_duration(normalized_sound)

        # Overwrite the original file
        final_sound.export(file_path, format="wav")
        print(f"Processed and overwritten {filename}")

# Example usage
# Target volume in dBFS
# audio_processor = AudioProcessor(input_folder, output_folder, target_duration_ms, target_dBFS)
# audio_processor.process_all_files()
