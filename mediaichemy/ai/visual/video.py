import asyncio
from runware import IVideoInference
from mediaichemy.file import VideoFile
from mediaichemy.ai.visual.visual import VisualAI, filter_params_for
from mediaichemy.ai.visual.image import ImageAI


class VideoAI(VisualAI):
    @filter_params_for(IVideoInference.__init__)
    async def _create_video_inference(self, prompt, **kwargs) -> IVideoInference:
        print(kwargs)
        """Create IVideoInference object with filtered parameters."""
        return IVideoInference(
            positivePrompt=prompt,
            **kwargs
        )

    async def create(self,
                     prompt,
                     output_path,
                     **kwargs) -> VideoFile:
        client = await self._get_runware_client()
        kwargs = self._set_defaults(**kwargs)
        kwargs['model'] = kwargs.pop('video_model')
        inference_object = await self._create_video_inference(prompt, **kwargs)
        try:
            timeout = 600
            videos = await asyncio.wait_for(
                client.videoInference(requestVideo=inference_object),
                timeout=timeout  # Timeout in seconds
            )
            ivideo = videos[0]
            video = self.download(ivideo.videoURL, output_path)
            return VideoFile(video), ivideo.cost
        except asyncio.TimeoutError:
            raise TimeoutError(f"Video generation timed out after {timeout} seconds")


class VideoFromImageAI(VisualAI):
    async def create(self,
                     prompt,
                     image_output_path,
                     video_output_path,
                     **kwargs) -> VideoFile:
        image, image_cost = await ImageAI().create(
            prompt=prompt,
            output_path=image_output_path,
            **kwargs
        )
        video, video_cost = await VideoAI().create(
            prompt=prompt,
            output_path=video_output_path,
            frameImages=[image.to_iframe_image()],
            **kwargs
        )
        image.delete()
        total_cost = image_cost + video_cost
        return video, total_cost
