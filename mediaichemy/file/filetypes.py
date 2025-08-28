from .file import File
from .utils import get_next_available_path
import json
from typing import Optional, Union, Literal
import os
import subprocess
from pathlib import Path
from PIL import Image
from mutagen.mp3 import MP3
import logging
import io
from runware.types import IFrameImage
logger = logging.getLogger(__name__)


class JSONFile(File):
    def __init__(self, path):
        super().__init__(path, extensions=[".json"])

    def load(self) -> dict:
        self.validate_file()
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded JSON file: {self.path}")
        return data

    def save(self) -> None:
        os.makedirs(self.dir, exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        logger.debug(f"Saved JSON file: {self.path}")


class VideoFile(File):
    def __init__(self, path):
        super().__init__(path, extensions=[".mp4", ".avi", ".mov", ".mkv", ".webm"])

    def get_duration(self) -> float:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                self.path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration = float(result.stdout.strip())
        return duration


class ImageFile(File):
    def __init__(self, path):
        super().__init__(path, extensions=[".jpg", ".jpeg", ".png", ".gif", ".bmp"])

    def save(self, data: Image.Image) -> None:
        os.makedirs(self.dir, exist_ok=True)
        data.save(self.path, format='JPEG')
        logger.debug(f"Saved JPEG file: {self.path}")

    def load(self) -> Image.Image:
        image_data = Image.open(self.path)
        logger.debug(f"Loaded JPEG file: {self.path}")
        return image_data

    def to_bytes(self, format: str = 'JPEG') -> bytes:
        """Convert PIL Image to bytes."""
        buffer = io.BytesIO()
        self.data.save(buffer, format=format)
        return buffer.getvalue()

    def to_base64(self, format: str = 'JPEG') -> str:
        """Convert image to base64 string."""
        import base64
        image_bytes = self.to_bytes(format=format)
        return base64.b64encode(image_bytes).decode('utf-8')

    def to_data_uri(self, format: str = 'JPEG') -> str:
        """Convert image to data URI string."""
        base64_string = self.to_base64(format=format)
        mime_type = f"image/{format.lower()}"
        return f"data:{mime_type};base64,{base64_string}"

    def to_iframe_image(self, frame: Optional[Union[Literal["first", "last"], int]] = 'first'
                        ) -> IFrameImage:
        # Fix: Call the method with () and use data URI format
        return IFrameImage(
            inputImage=self.to_data_uri(),  # Changed from self.to_bytes to self.to_data_uri()
            frame=frame
        )


class AudioFile(File):
    def __init__(self, path):
        # Convert WAV to MP3 if needed
        if path.lower().endswith('.wav'):
            path = self._convert_to_mp3(path)

        super().__init__(path, extensions=[".mp3", ".wav", ".m4a", ".flac", ".ogg"])

    def get_duration(self) -> float:
        audio = MP3(self.path)
        return audio.info.length

    def _convert_to_mp3(self, wav_path: str) -> str:
        """Convert WAV to MP3."""
        mp3_path = Path(wav_path).with_suffix('.mp3')
        mp3_path = get_next_available_path(mp3_path)
        subprocess.run(['ffmpeg', '-i',
                        wav_path, '-y', str(mp3_path)],
                       check=True, capture_output=True)
        os.remove(wav_path)
        return str(mp3_path)


class SubtitleFile(File):
    def __init__(self, path):
        super().__init__(path, extensions=[".ass", ".srt", ".vtt"])
