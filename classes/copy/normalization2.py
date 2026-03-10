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

    # Function to process a single audio file and convert to wav if necessary
    def process_file(self, filename):
        file_path = os.path.join(self.input_folder, filename)
        file_name, file_ext = os.path.splitext(filename)

        if not os.path.exists(file_path):
            print(f"File {filename} does not exist in {self.input_folder}.")
            return

        # Load the audio file, converting to WAV if necessary
        if file_ext.lower() != ".wav":
            sound = AudioSegment.from_file(file_path)
            new_file_path = os.path.join(self.input_folder, file_name + ".wav")
            print(f"Converting {filename} to WAV format as {file_name}.wav")
        else:
            sound = AudioSegment.from_wav(file_path)
            new_file_path = file_path

        # Normalize the volume
        normalized_sound = self.match_target_amplitude(sound)

        # Adjust the duration
        if len(normalized_sound) > self.target_duration_ms:
            # If the file is longer than the target duration, truncate it
            final_sound = normalized_sound[:self.target_duration_ms]
        else:
            # If the file is shorter, loop the sound to fill the time
            final_sound = self.loop_audio_to_duration(normalized_sound)

        # Save the processed file as a WAV file
        final_sound.export(new_file_path, format="wav")
        print(f"Processed and saved {filename} as {new_file_path}")

    # Function to process all files in the folder
    def process_all_files(self):
        for filename in os.listdir(self.input_folder):
            self.process_file(filename)

# Example usage
# audio_processor = AudioProcessor(input_folder="path_to_folder")
# audio_processor.process_all_files()
