from mediaichemy.file import utils, AudioFile, VideoFile

from mediaichemy.ai import (ImageAI,
                            VideoAI,
                            VideoFromImageAI,
                            VoiceAI,
                            ChatAI)
from mediaichemy.studio.editors import (AudioEditor,
                                        VideoEditor,
                                        SubtitleEditor)
from mediaichemy.studio.sources.platforms import YoutubeVideoList
from mediaichemy.studio.captions import CaptionMaker


class StudioFacade:
    def __init__(self,
                 params):
        self.params = params

    async def create_image(self, directory: str = None):
        output_path = utils.get_next_available_path(directory + 'image.jpg')
        return await ImageAI().create(prompt=self.params.image_prompt,
                                      output_path=output_path,
                                      **self.params.__dict__)

    async def create_video(self, directory: str = None):
        output_path = utils.get_next_available_path(directory + 'video.mp4')
        return await VideoAI().create(prompt=self.params.video_prompt,
                                      output_path=output_path,
                                      **self.params.__dict__)

    async def create_video_from_image(self, directory: str = None):
        image_path = utils.get_next_available_path(directory + 'image.jpg')
        video_path = utils.get_next_available_path(directory + 'video.mp4')
        return await VideoFromImageAI().create(prompt=self.params.video_prompt,
                                               image_output_path=image_path,
                                               video_output_path=video_path,
                                               **self.params.__dict__)

    def create_media_agent(self,
                           system_prompt):
        chat_ai = ChatAI()
        agent = chat_ai.create_agent(output_type=self.params,
                                     system_prompt=system_prompt)
        return agent

    def create_narration(self, directory: str = None):
        output_path = utils.get_next_available_path(directory + 'narration.wav')
        narration = VoiceAI().synthesize_speech(text=self.params.narration_text,
                                                voice_name=self.params.voice_name,
                                                output_path=output_path)
        AudioEditor(narration).add_silence_tail(duration=self.params.silence_tail)
        return narration

    async def create_captions(self, directory: str = None):
        caption_maker = CaptionMaker(parameters=self.params)
        self.captions = await caption_maker.create_captions_from_parameters()
        captions_str = self.captions.to_string()
        output_path = utils.get_next_available_path(directory + 'captions.txt')
        with open(output_path, 'w') as f:
            f.write(captions_str)
        return self.captions

    def download_youtube_mp3(self, directory: str = None):
        output_path = utils.get_next_available_path(directory + 'youtube.mp3')
        yt_videos = YoutubeVideoList(self.params.youtube_urls)
        return yt_videos.download_random_from_list(output_path=output_path)

    def mix_audio_with_random_background_section(self, original_audio: AudioFile, background: AudioFile):
        AudioEditor(background).extract_random_section(duration=original_audio.get_duration())
        AudioEditor(original_audio).mix_with(audio=background,
                                             relative_volume=self.params.relative_volume)
        background.delete()
        return original_audio

    def loop_to_duration(self, video: VideoFile, target_duration: float):
        return VideoEditor(video).loop_to_duration(target_duration)

    def add_audio_track_to_video(self, video: VideoFile, audio: AudioFile):
        return VideoEditor(video).add_audio_track_to_video(audio)

    def produce_subtitled_videos(self,
                                 video: VideoFile):
        sub_editor = SubtitleEditor(video,
                                    text=self.params.narration_text,
                                    params=self.params)
        subtitled_videos = sub_editor.add_text_to_video()
        return subtitled_videos
