from mediaichemy import file

MOCKS_PATH = 'tests/_resources/mocks/'
image = file.ImageFile(f'{MOCKS_PATH}image.jpg')
speech = file.AudioFile(f'{MOCKS_PATH}speech.mp3')
video = file.VideoFile(f'{MOCKS_PATH}video.mp4')
