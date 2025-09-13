from piper import PiperVoice
import wave
import subprocess
from pathlib import Path
from mediaichemy.file import AudioFile


class VoiceAI:
    @staticmethod
    def _download_piper_voice(narration_voice_name: str) -> Path:
        voices_dir = Path("voices")
        voices_dir.mkdir(exist_ok=True)
        subprocess.run(["python3", "-m",
                        "piper.download_voices",
                        narration_voice_name,
                        "--download-dir", str(voices_dir)], check=True)
        voice_path = voices_dir / f"{narration_voice_name}.onnx"
        return voice_path

    def synthesize_speech(self,
                          text: str,
                          output_path: str,
                          narration_voice_name: str) -> AudioFile:
        voice_path = self._download_piper_voice(narration_voice_name)
        voice = PiperVoice.load(voice_path)
        with wave.open(output_path, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
        return AudioFile(output_path)
