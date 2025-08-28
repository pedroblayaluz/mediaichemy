from mediaichemy.media.multi.multi import MultiMedia
from mediaichemy.media.parameters import NarrationWithBackgroundParameters


class NarrationWithBackground(MultiMedia):
    def __init__(self,
                 params: NarrationWithBackgroundParameters = NarrationWithBackgroundParameters()):
        super().__init__(params=params)

    async def create(self):
        narration = self.create_narration_with_background()
        return self.unpack(narration), None

    def create_narration_with_background(self):
        narration = self.studio.create_narration(self.output_dir)
        background = self.studio.download_youtube_mp3(self.output_dir)
        narration = self.studio.mix_audio_with_random_background_section(narration, background)
        return narration
