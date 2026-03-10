import os
from pydub import AudioSegment
from pydub.silence import detect_silence

class AudioProcessor:
    def __init__(self, input_folder, target_duration_ms=30000, target_dBFS=-20.0, silence_threshold=-50.0, silence_chunk_ms=1000):
        self.input_folder = input_folder
        self.target_duration_ms = target_duration_ms
        self.target_dBFS = target_dBFS
        self.silence_threshold = silence_threshold
        self.silence_chunk_ms = silence_chunk_ms

    # Function to normalize the audio volume
    def match_target_amplitude(self, sound):
        change_in_dBFS = self.target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    # Function to loop the audio until it reaches the target duration
    def loop_audio_to_duration(self, sound):
        loops_needed = int(self.target_duration_ms / len(sound)) + 1
        extended_sound = sound * loops_needed  # Loop the sound
        return extended_sound[:self.target_duration_ms]  # Trim to exact length

    # Function to remove silence from the audio
    def trim_silence(self, sound):
        silence_ranges = detect_silence(sound, min_silence_len=self.silence_chunk_ms, silence_thresh=self.silence_threshold)

        # If no silence is detected, return the original sound
        if not silence_ranges:
            return sound
        
        # Remove silence based on detected ranges
        trimmed_sound = sound[silence_ranges[0][0]:silence_ranges[-1][1]]
        return trimmed_sound

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

        # Remove silence from the audio
        trimmed_sound = self.trim_silence(sound)

        # Normalize the volume
        normalized_sound = self.match_target_amplitude(trimmed_sound)

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

        return new_file_path

    # Function to process all files in the folder
    def process_all_files(self):
        for filename in os.listdir(self.input_folder):
            self.process_file(filename)

# Example usage
# audio_processor = AudioProcessor(input_folder="path_to_folder")
# audio_processor.process_all_files()
