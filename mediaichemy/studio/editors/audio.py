from .editor import Editor
from mediaichemy.file import AudioFile
import subprocess
import random


class AudioEditor(Editor):
    @property
    def file_type(self):
        return AudioFile

    @Editor.edit_file
    def add_silence_tail(self, duration: int):
        command = [
            "ffmpeg",
            "-y",
            "-i", self.file.path,
            "-f", "lavfi",
            "-t", str(duration),
            "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
            "-map", "[out]",
            self.working_file.path
        ]
        subprocess.run(command, check=True)

    @Editor.edit_file
    def extract_section(self,
                        start: int,
                        duration: int):
        command = [
            "ffmpeg",
            "-y",
            "-i", self.file.path,
            "-ss", str(start),
            "-t", str(duration),
            "-c", "copy",
            self.working_file.path
        ]
        subprocess.run(command, check=True)

    @Editor.edit_file
    def mix_with(self,
                 audio: AudioFile,
                 relative_volume: float):

        if not audio:
            raise ValueError("No MP3 file provided to mix with.")
        if not (0.0 <= relative_volume <= 2.0):
            raise ValueError("relative_volume must be between 0 and 2.")

        original_volume = 2.0 - relative_volume
        new_volume = relative_volume
        command = [
            "ffmpeg",
            "-y",
            "-i", self.file.path,
            "-i", audio.path,
            "-filter_complex", (f"[0:a]volume={original_volume}"
                                f"[a0];[1:a]volume={new_volume}"
                                "[a1];[a0][a1]amix=inputs=2:duration=longest:dropout_transition=2"),
            "-c:a", "libmp3lame",
            self.working_file.path
            ]
        subprocess.run(command, check=True)

    def extract_random_section(self,
                               duration: int):
        total_duration = self.file.get_duration()
        if duration > total_duration:
            raise ValueError(
                f"Specified duration ({duration}s) is longer than the MP3 file's total duration ({total_duration}s).")
        random_start = random.randint(0, int(total_duration - duration))
        self.extract_section(start=random_start,
                             duration=duration)
