from mediaichemy import file

EO_PATH = 'tests/_resources/expected_outputs/'

image = file.ImageFile(f'{EO_PATH}image/image.jpg')
narration = file.AudioFile(f'{EO_PATH}narration/narration.mp3')
narration_with_background = file.AudioFile(f'{EO_PATH}narrationwithbackground/narration.mp3')
video = file.VideoFile(f'{EO_PATH}video/video.mp4')
video_from_image = file.VideoFile(f'{EO_PATH}videofromimage/video.mp4')
narrated_video = file.VideoFile(f'{EO_PATH}narratedvideo/video.mp4')

subtitled_videos_path = f'{EO_PATH}subtitlednarratedvideo/subtitlednarratedvideo/'
subtitled_videos = [
    file.VideoFile(f'{subtitled_videos_path}video_2.mp4'),
    file.VideoFile(f'{subtitled_videos_path}video_5.mp4'),
    file.VideoFile(f'{subtitled_videos_path}video_8.mp4')
]
