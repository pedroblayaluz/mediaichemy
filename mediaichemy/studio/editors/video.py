
import subprocess
import os
from math import ceil

from mediaichemy.file import VideoFile, ImageFile
from mediaichemy.ai import VideoAI
from mediaichemy.studio.editors.editor import Editor

from logging import getLogger
logger = getLogger(__name__)


class VideoEditor(Editor):
    @property
    def file_type(self):
        return VideoFile

    @Editor.edit_file
    def add_audio_track_to_video(self, audio):
        # Use ffmpeg to combine audio and video
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-i", self.file.path,  # Input video
            "-i", audio.path,  # Input audio
            "-map", "0",  # Map all streams from the video
            "-map", "1:a",  # Map only the audio stream from the audio file
            "-c:v", "copy",  # Copy the video stream without re-encoding
            "-shortest",  # Ensure the output duration matches the shortest input
            self.working_file.path
        ]
        subprocess.run(command, check=True)

    @Editor.edit_file
    def apply_boomerang(self):
        command = [
            'ffmpeg',
            '-y',
            '-ss', '0',
            '-an',
            '-i', self.file.path,
            '-filter_complex', "[0]split[b][c];[c]reverse[r];[b][r]concat",
            self.working_file.path
        ]
        subprocess.run(command, check=True)

    def _create_concat_list(self,
                            output_path: str,
                            file_paths: list[str]) -> str:
        with open(output_path, "w") as f:
            for path in file_paths:
                f.write(f"file '{os.path.abspath(path)}'\n")
        return output_path

    def _run_ffmpeg_concat(self, concat_list_path: str, output_path: str) -> None:
        """Run ffmpeg to concatenate videos listed in the concat file."""
        command = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_list_path,
            '-c', 'copy',
            output_path
        ]
        subprocess.run(command, check=True)
        os.remove(concat_list_path)

    @Editor.edit_file
    def concat_with_videos(self, videos_to_add):
        concat_list_path = os.path.join(self.file.dir, "concat_list.txt")
        file_paths = [self.file.path] + [video.path for video in videos_to_add]

        # Create concat list and run ffmpeg
        self._create_concat_list(concat_list_path, file_paths)
        self._run_ffmpeg_concat(concat_list_path, self.working_file.path)

    @Editor.edit_file
    def repeat_video(self, n: int):
        if n <= 0:
            raise ValueError("Number of repetitions must be greater than 0.")

        # Create concat list with repeated entries
        concat_list_path = os.path.join(self.file.dir, "concat_list.txt")
        file_paths = [self.file.path] * n

        # Create concat list and run ffmpeg
        self._create_concat_list(concat_list_path, file_paths)
        self._run_ffmpeg_concat(concat_list_path, self.working_file.path)

    @Editor.edit_file
    def trim_video(self, duration: int) -> str:
        command = [
            'ffmpeg',
            '-i', self.file.path,
            '-t', str(duration),
            '-c', 'copy',
            '-y',
            self.working_file.path
        ]
        subprocess.run(command, check=True)

    def extract_last_frame(self) -> ImageFile:
        output_path = self.file.path.replace(".mp4", "_lastframe.jpg")
        command = [
            "ffmpeg",
            "-y",
            "-sseof", "-3",
            "-i", self.file.path,
            "-vsync", "0",
            "-q:v", "0",
            "-update", "true",
            output_path
        ]
        subprocess.run(command, check=True)
        return ImageFile(output_path)

    @staticmethod
    def create_video_from_image(image: ImageFile, duration: int) -> VideoFile:
        video_path = image.path.replace(".jpg", "_video.mp4")
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-loop", "1",  # Loop the image
            "-i", image.path,  # Input image
            "-c:v", "libx264",  # Use H.264 codec
            "-t", str(duration),  # Set the duration
            "-pix_fmt", "yuv420p",
            video_path
        ]
        subprocess.run(command, check=True)

        return VideoFile(video_path)

    def loop_to_duration(self, target_duration: float):
        if target_duration <= 0:
            raise ValueError("Target duration must be greater than 0 seconds.")

        self.apply_boomerang()
        n_repeat = ceil(target_duration / self.file.get_duration())
        if n_repeat > 1:
            self.repeat_video(n_repeat)
        self.trim_video(duration=target_duration)

    @Editor.edit_file
    async def ai_generate_to_duration(self, target_duration: float, prompt: str = None,
                                      video_model: str = 'bytedance:1@1'):
        if target_duration <= 0:
            raise ValueError("Target duration must be greater than 0 seconds.")

        if not prompt:
            logger.warning("No prompt provided for AI video generation.")

        current_video = self.file
        videos_to_add = []

        while sum([v.get_duration() for v in [self.file] + videos_to_add]) < target_duration:
            n = len(videos_to_add)
            n_path = self.file.path.replace(".mp4", f"_ai_extension{n}.mp4")
            lastframe = self.extract_last_frame() if current_video == self.file else \
                VideoEditor(current_video).extract_last_frame()
            video_continue, _ = await VideoAI().create(
                prompt=prompt,
                output_path=n_path,
                frameImage=lastframe.path,
                video_model=video_model
            )

            videos_to_add.append(video_continue)
            current_video = video_continue

        if videos_to_add:
            self.concat_with_videos(videos_to_add)
        self.trim_video(duration=target_duration)
