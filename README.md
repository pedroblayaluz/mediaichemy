# mediaichemy: AI-Powered Multimedia Content Creation

⚗️🧪🧫 **mediaichemy** is a Python library for generating and editing multimedia content using AI.
 
  
    
            






## Getting Started

<img src="logo.png" width="200px" align="right" alt="mediaichemy logo">
1. Clone the repository:

```bash
git clone https://github.com/your-repo/mediaichemy.git
cd mediaichemy

```

2. Install dependencies:

```bash
pip install -e .
```

3. Set up API keys for OpenRouter and Runware (see below).


## Setting up API keys

#### 1. Create an [OpenRouter Account](https://openrouter.ai/signup)
- Obtain an [Openrouter API key](https://openrouter.ai/keys)
#### 3. Create a [Runware Account](https://runware.ai)
- Obtain a [Runware API key](https://my.runware.ai/keys)

#### 3. Configure your API keys as environment variables:

Linux/macOS (Terminal):
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
export RUNWARE_API_KEY="your_runware_api_key"
```

Windows (Command Prompt):
```cmd
set OPENROUTER_API_KEY=your_openrouter_api_key
set RUNWARE_API_KEY=your_runware_api_key
```

Windows (PowerShell)
```powershell
$env:OPENROUTER_API_KEY="your_openrouter_api_key"
$env:RUNWARE_API_KEY="your_runware_api_key"
```

#### Option 2: Use a .env File

Create a file named `.env` in your project root with the following content:
```
OPENROUTER_API_KEY=your_openrouter_api_key
RUNWARE_API_KEY=your_runware_api_key
```

## Media Type Instantiation Examples

You can instantiate each media type with all its parameters like this:

```python
from mediaichemy.media.single import Image, Video, Narration
from mediaichemy.media.multi import VideoFromImage, NarrationWithBackground, NarratedVideo, SubtitledNarratedVideo

# Image
image = Image(params=Image.params_class(
    image_prompt="A cat on a skateboard",
    image_model="rundiffusion:110@101"
))

# Video
video = Video(params=Video.params_class(
    video_prompt="A dog running in the park",
    video_model="bytedance:1@1",
    duration=10.0,
    width=1088,
    height=1920
))

# Narration
narration = Narration(params=Narration.params_class(
    narration_text="Welcome to the show!",
    narration_voice_name="en_US-amy-medium",
    narration_silence_tail=5,
    narration_speed=1.0
))

# Video from Image
video_from_image = VideoFromImage(params=VideoFromImage.params_class(
    video_prompt="A sunrise over mountains",
    image_model="rundiffusion:110@101",
    video_model="bytedance:1@1",
    duration=6,
    width=1088,
    height=1920
))

# Narration with Background
narration_bg = NarrationWithBackground(params=NarrationWithBackground.params_class(
    narration_text="Relax and breathe.",
    narration_voice_name="en_US-amy-medium",
    narration_silence_tail=5,
    narration_speed=1.0,
    background_relative_volume=0.5,
    background_youtube_urls=["https://youtube.com/example"]
))

# Narrated Video
narrated_video = NarratedVideo(params=NarratedVideo.params_class(
    video_prompt="A city at night",
    image_model="rundiffusion:110@101",
    video_model="bytedance:1@1",
    duration=6,
    width=1088,
    height=1920,
    narration_text="The city never sleeps.",
    narration_voice_name="en_US-amy-medium",
    narration_silence_tail=5,
    narration_speed=1.0,
    background_relative_volume=0.5,
    background_youtube_urls=[]
))

# Subtitled Narrated Video
subtitled_narrated_video = SubtitledNarratedVideo(params=SubtitledNarratedVideo.params_class(
    video_prompt="A forest in the rain",
    image_model="rundiffusion:110@101",
    video_model="bytedance:1@1",
    duration=6,
    width=1088,
    height=1920,
    narration_text="Listen to the rain.",
    narration_voice_name="en_US-amy-medium",
    narration_silence_tail=5,
    narration_speed=1.0,
    background_relative_volume=0.5,
    background_youtube_urls=[],
    subtitle_fontname="Arial",
    subtitle_fontsize=18,
    subtitle_color="#FFEE00C7",
    subtitle_outline_color="#000000",
    subtitle_positions=["bottom_center", "top_center", "middle_center"]
))
```
