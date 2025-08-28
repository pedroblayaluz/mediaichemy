import subprocess
import re
import logging
from mediaichemy.file import VideoFile, SubtitleFile
from .editor import Editor
import pysubs2
from dataclasses import dataclass
from mediaichemy.media.parameters import SubtitleParameters

logger = logging.getLogger(__name__)


@dataclass
class SubtitleEntry:
    """Represents a single subtitle with timing information."""
    start: float
    end: float
    text: str


class SubtitleTimingEngine:
    """Handles timing calculations and subtitle entry generation."""
    def __init__(self, text: str, duration: float):
        self.text = text
        self.duration = duration

    @staticmethod
    def split_into_sentences(text: str) -> list[str]:
        return [s.strip() for s in re.split(r'(?<=[.,!?]) +', text) if s.strip()]

    def make_entries(self) -> list[SubtitleEntry]:
        """Generate timed subtitle entries for the given duration."""
        if self.duration <= 0:
            raise ValueError("Duration must be greater than 0.")

        sentences = self.split_into_sentences(self.text)
        char_time = self.duration / len(self.text)

        entries = []
        current_time = 0.0

        for sentence in sentences:
            end_time = current_time + (char_time * len(sentence))
            entries.append(SubtitleEntry(
                start=current_time,
                end=end_time,
                text=sentence
            ))
            current_time = end_time

        logger.debug(f"Generated {len(entries)} subtitle entries")
        return entries


class SubtitlesASSMaker:
    def __init__(self,
                 entries: list[SubtitleEntry],
                 video: VideoFile,
                 params: SubtitleParameters = SubtitleParameters()):
        self.entries = entries
        self.params = params
        self.video = video

    def create_styled_subtitle_templates(self) -> list[SubtitleFile]:
        style_params = self.params
        alignment_values = [style_params.alignments_map[align_str] for align_str in style_params.alignments]

        subtitle_templates = []

        for alignment in alignment_values:
            subtitle_file = pysubs2.SSAFile()
            style = subtitle_file.styles["Default"]

            # Apply all style parameters
            style.fontname = style_params.fontname
            style.fontsize = style_params.fontsize

            # Handle color conversions
            style.primarycolor = pysubs2.Color(*map(int, style_params.primarycolor.split(',')))
            style.secondarycolor = pysubs2.Color(*map(int, style_params.secondarycolor.split(',')))
            style.outlinecolor = pysubs2.Color(*map(int, style_params.outlinecolor.split(',')))
            style.backcolor = pysubs2.Color(*map(int, style_params.backcolor.split(',')))

            # Style properties and other settings
            style.bold = style_params.bold
            style.italic = style_params.italic
            style.underline = style_params.underline
            style.strikeout = style_params.strikeout
            style.scalex = style_params.scalex
            style.scaley = style_params.scaley
            style.spacing = style_params.spacing
            style.angle = style_params.angle
            style.borderstyle = style_params.borderstyle
            style.outline = style_params.outline
            style.shadow = style_params.shadow
            style.alignment = alignment
            style.margin_l = style_params.margin_l
            style.margin_r = style_params.margin_r
            style.margin_v = style_params.margin_v

            subtitle_templates.append(subtitle_file)

        return subtitle_templates

    def make_files(self, subtitle_entries: list[SubtitleEntry]) -> list[str]:
        templates = self.create_styled_subtitle_templates()
        files = []
        for sub in templates:

            for entry in subtitle_entries:
                sub.append(
                    pysubs2.SSAEvent(
                        start=entry.start * 1000,
                        end=entry.end * 1000,
                        text=entry.text
                    )
                )

            # Save the .ass file
            sub_file_path = self.video.path.replace(".mp4", f'_{sub.styles["Default"].alignment}.ass')
            sub.save(sub_file_path)
            file = SubtitleFile(sub_file_path)
            files.append(file)
            logger.info(f"Subtitle file created at: {file.path}")

        return files


class SubtitleEditor(Editor):
    def __init__(self,
                 file: VideoFile,
                 text: str = '',
                 params: SubtitleParameters = SubtitleParameters()):
        super().__init__(file)
        self.text = text
        self.params = params

    @property
    def file_type(self):
        return VideoFile

    def add_text_to_video(self, output_path: str = None):
        entries = self.create_timed_entries()
        ass_files = self.create_subtitle_files(entries)
        subtitled_videos = self.add_subtitles(subtitles=ass_files)
        logger.info("Text successfully added to the video as subtitles.")
        return subtitled_videos

    @property
    def subtitle_duration(self):
        return self.file.get_duration() - self.params.silence_tail

    def create_timed_entries(self) -> list[SubtitleEntry]:
        timing_engine = SubtitleTimingEngine(text=self.text,
                                             duration=self.subtitle_duration)
        return timing_engine.make_entries()

    def create_subtitle_files(self, entries: list[SubtitleEntry]) -> list[SubtitleFile]:
        subtitle_maker = SubtitlesASSMaker(entries=entries,
                                           video=self.file,
                                           params=self.params)
        return subtitle_maker.make_files(subtitle_entries=entries)

    def add_subtitles(self,
                      subtitles: list[dict[str, float | str]]):
        subtitled_videos = []
        for subtitle in subtitles:
            temp_output_path = subtitle.path.replace(".ass", ".mp4")
            try:
                # Use ffmpeg to add subtitles to the video
                command = [
                    "ffmpeg",
                    "-y",
                    "-i", self.file.path,
                    "-vf", f"subtitles={subtitle.path}",
                    "-c:a", "copy",
                    temp_output_path
                ]
                subprocess.run(command, check=True)
                logger.info(f"Subtitles added successfully. Output saved to: {temp_output_path}")
                subtitled_videos.append(VideoFile(temp_output_path))
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to add subtitles to video: {e}")
                raise
            finally:
                subtitle.delete()
        return subtitled_videos
