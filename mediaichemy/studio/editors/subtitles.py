import subprocess
import re
import logging
from mediaichemy.file import VideoFile, SubtitleFile
from .editor import Editor
import pysubs2
from pydantic.dataclasses import dataclass
from mediaichemy.media.parameters import SubtitleParameters

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
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
        return [s.strip() for s in re.split(r'(?<=[!.,:?])(?=\s|\n|")+', text) if s.strip()]

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
    ALIGNMENTS_MAP = {
        "bottom_left": pysubs2.Alignment.BOTTOM_LEFT,
        "bottom_center": pysubs2.Alignment.BOTTOM_CENTER,
        "bottom_right": pysubs2.Alignment.BOTTOM_RIGHT,
        "middle_left": pysubs2.Alignment.MIDDLE_LEFT,
        "middle_center": pysubs2.Alignment.MIDDLE_CENTER,
        "middle_right": pysubs2.Alignment.MIDDLE_RIGHT,
        "top_left": pysubs2.Alignment.TOP_LEFT,
        "top_center": pysubs2.Alignment.TOP_CENTER,
        "top_right": pysubs2.Alignment.TOP_RIGHT,
    }

    def __init__(self,
                 entries: list[SubtitleEntry],
                 video: VideoFile,
                 params: SubtitleParameters = SubtitleParameters()):
        self.entries = entries
        self.params = params
        self.video = video

    def create_styled_subtitle_templates_for_positions(self) -> list[pysubs2.SSAFile]:
        positions = self._get_alignment_positions()
        subtitle_templates = []

        for position in positions:
            subtitle_file = self._create_subtitle_file_for_position(position)
            subtitle_templates.append(subtitle_file)

        return subtitle_templates

    def _get_alignment_positions(self) -> list[pysubs2.Alignment]:
        return [self.ALIGNMENTS_MAP[align_str]
                for align_str in self.params.subtitle_positions]

    def _create_subtitle_file_for_position(self, position: pysubs2.Alignment) -> pysubs2.SSAFile:
        subtitle_file = pysubs2.SSAFile()
        style = subtitle_file.styles["Default"]

        style.bold = False
        style.italic = False
        style.underline = False
        style.strikeout = False

        style.scalex = 100
        style.scaley = 100
        style.spacing = 0
        style.angle = 0

        style.borderstyle = 1
        style.outline = 0.3
        style.shadow = 1.0

        style.marginl = 10
        style.marginr = 10
        style.marginv = 70
        style.outline = 0.3
        style.shadow = 1.0

        style.fontname = self.params.subtitle_fontname
        style.fontsize = self.params.subtitle_fontsize
        style.primarycolor = self._hex_to_pysubs_color(self.params.subtitle_color)
        style.outlinecolor = self._hex_to_pysubs_color(self.params.subtitle_outline_color)
        style.alignment = position

        return subtitle_file

    def _hex_to_pysubs_color(self, hex_color: str) -> pysubs2.Color:
        h = hex_color.lstrip('#')
        r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        a = 0
        if len(h) >= 8:
            hex_alpha = int(h[6:8], 16)
            a = 255 - hex_alpha
        return pysubs2.Color(r, g, b, a)

    def make_files(self, subtitle_entries: list[SubtitleEntry]) -> list[str]:
        templates = self.create_styled_subtitle_templates_for_positions()
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
        return self.file.get_duration() - self.params.narration_silence_tail

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
