import secrets
import subprocess
from mediaichemy.file import AudioFile, utils
from mediaichemy.studio.editors.subtitles import SubtitleEntry
from youtube_transcript_api import YouTubeTranscriptApi
import re
import logging
logger = logging.getLogger(__name__)


class YoutubeVideo:
    def __init__(self, url: str):
        self.url = url
        self.id = self.extract_id()
        self.ytt_api = YouTubeTranscriptApi()

    def extract_id(self) -> str:
        youtube_patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',  # Standard and short URLs
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',                    # Embedded videos
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'                         # Old style
        ]
        for pattern in youtube_patterns:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)

        raise ValueError(f"Could not extract video ID from URL: {self.url}")

    def download(self, output_path) -> AudioFile:
        output_path = utils.get_next_available_path(output_path)
        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            self.url
        ]
        result = subprocess.run(command, check=True,
                                capture_output=True,
                                text=True
                                )
        logger.debug(f"Downloaded audio from {self.url} to {output_path}")
        if "ERROR" in result.stderr:
            error = ("Error downloading background music."
                     " If you are using a VPN consider disabling it."
                     f" Error details: {result.stderr}")
            logger.error(error)
            raise ValueError(error)
        return AudioFile(output_path)

    def check_available_transcripts(self, print_transcripts=False):
        transcript_list = self.ytt_api.list(self.id)
        auto_generated_transcripts = [transcript.language_code
                                      for transcript in transcript_list if transcript.is_generated]
        user_generated_transcripts = [transcript.language_code
                                      for transcript in transcript_list if not transcript.is_generated]
        transcripts = {'auto_generated': auto_generated_transcripts, 'user_generated': user_generated_transcripts}
        if print_transcripts:
            print(transcripts)
        return transcripts

    def get_transcript(self, language='en'):
        transcript = self.ytt_api.fetch(self.id,
                                        languages=[language])
        return transcript

    def _get_subtitles_from_transcript(self, transcript) -> list[SubtitleEntry]:
        """Convert YouTube transcript snippets to SubtitleEntry objects."""
        subtitles = []
        for snippet in transcript.snippets:
            subtitle = SubtitleEntry(
                start=snippet.start,
                end=snippet.start + snippet.duration,
                text=snippet.text
            )
            subtitles.append(subtitle)
        return subtitles

    def get_subtitles(self, language: str = None) -> list[SubtitleEntry]:
        """Get subtitles as a list of SubtitleEntry objects."""
        transcripts = self.check_available_transcripts()
        user_generated = transcripts.get('user_generated', None)

        if user_generated:
            language = user_generated[0]
        else:
            logger.warning("No user-generated transcripts available. "
                           "Using auto-generated transcripts instead.")
            language = transcripts.get('auto_generated', None)[0]

        transcript = self.get_transcript(language=language)
        subtitles = self._get_subtitles_from_transcript(transcript)

        return subtitles


class YoutubeVideoList:
    def __init__(self, urls: list):
        self.videos = [YoutubeVideo(url) for url in urls]

    def select_random_video(self) -> str:
        selected_url = secrets.choice(self.videos)
        return selected_url

    def download_random_from_list(self, output_path) -> AudioFile:
        youtube_video = self.select_random_video()
        video = youtube_video.download(output_path)
        return video
