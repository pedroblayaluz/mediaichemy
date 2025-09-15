# 🧪 mediaichemy: AI-powered content creation

`mediaichemy` is a Python library for generating **cheap and cost effective** multimedia content using AI. It intelligently selects models and workflows to minimize costs while delivering high-quality results.

## Usage ovewview

`mediaichemy` offers a simple yet powerful approach to content creation:

- [**Media:**](#media) Choose a specific media type and edit its parameters to create the content you want.
- [**MediaCreator**](#mediacreator) Use AI to generate content ideas for you and create them.

Both approaches use the same underlying Media system, with MediaCreator adding an AI layer that handles the creative decisions for you. All content creation automatically optimizes for cost-effectiveness by choosing the best-performing, lowest-cost AI models.

## What's Inside

**🚀 [Getting Started](#getting-started)**

**🔑 [Setting up API keys](#setting-up-api-keys)**

**🎬 [Media](#media)**

   - [Single media examples](#single-media-examples)

   - [Multi media examples](#multi-media-examples)

**🧠 [Using the MediaCreator](#using-the-mediacreator)**

   - [Specific media type](#using-mediacreator-with-a-specific-media-type)
   - [Automatic media type](#letting-mediacreator-pick-the-best-media-type)

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

## Media

Each Media type creates a specific form of content using AI and editing tools.

### Single Media Examples
Media created using a single AI source.

#### Image
```python
from mediaichemy.media.single import Image
from mediaichemy.media.parameters import ImageParameters

image_params = ImageParameters(
    image_prompt="A cat on a skateboard",
    image_model="rundiffusion:110@101"
)
image = Image(params=image_params)
```

#### Video
```python
from mediaichemy.media.single import Video
from mediaichemy.media.parameters import VideoParameters

video_params = VideoParameters(
    video_prompt="A dog running in the park",
    video_model="bytedance:1@1",
    duration=10.0,
    width=1088,
    height=1920
)
video = Video(params=video_params)
```

#### Narration
```python
from mediaichemy.media.single import Narration
from mediaichemy.media.parameters import NarrationParameters

narration_params = NarrationParameters(
    narration_text="Welcome to the show!",
    narration_voice_name="en_US-amy-medium",
    narration_silence_tail=5,
    narration_speed=1.0
)
narration = Narration(params=narration_params)
```

### Multi Media Examples
Media created combining multiple AI sources.

#### Video from Image
```python
from mediaichemy.media.multi import VideoFromImage
from mediaichemy.media.parameters import VideoFromImageParameters

video_from_image_params = VideoFromImageParameters(
    video_prompt="A sunrise over mountains",
    image_model="rundiffusion:110@101",
    video_model="bytedance:1@1",
    duration=6,
    width=1088,
    height=1920
)
video_from_image = VideoFromImage(params=video_from_image_params)
```

#### Narration with Background
```python
from mediaichemy.media.multi import NarrationWithBackground
from mediaichemy.media.parameters import NarrationWithBackgroundParameters

narration_bg_params = NarrationWithBackgroundParameters(
    narration_text="Relax and breathe.",
    narration_voice_name="en_US-amy-medium",
    narration_silence_tail=5,
    narration_speed=1.0,
    background_relative_volume=0.5,
    background_youtube_urls=["https://youtube.com/example"]
)
narration_bg = NarrationWithBackground(params=narration_bg_params)
```

#### Narrated Video
```python
from mediaichemy.media.multi import NarratedVideo
from mediaichemy.media.parameters import NarratedVideoParameters

narrated_video_params = NarratedVideoParameters(
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
)
narrated_video = NarratedVideo(params=narrated_video_params)
```

#### Subtitled Narrated Video
```python
from mediaichemy.media.multi import SubtitledNarratedVideo
from mediaichemy.media.parameters import SubtitledNarratedVideoParameters

subtitled_narrated_video_params = SubtitledNarratedVideoParameters(
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
)
subtitled_narrated_video = SubtitledNarratedVideo(params=subtitled_narrated_video_params)
```

## Using the MediaCreator

By using `MediaCreator`, you let AI create ideas for you. You can use it to generate content for a specific media type or let it pick the best type for you automatically based on your prompt.

### MediaCreator

#### Using MediaCreator with a specific media type

```python
from mediaichemy.creator import MediaCreator
from mediaichemy.media.multi import SubtitledNarratedVideo

creator = MediaCreator(media_type=SubtitledNarratedVideo)
media = await creator.create(
    user_prompt="Create a short, inspiring narrated video about the beauty of rainforests, with subtitles."
)
# media is an instance of SubtitledNarratedVideo
```

#### Letting MediaCreator pick the best media type

```python
from mediaichemy.creator import MediaCreator

creator = MediaCreator()  # No media_type specified
media = await creator.create(
    user_prompt="Create a TikTok post that explains quantum entanglement in a fun and visual way."
)
# media will be an instance of the most appropriate media type (e.g., SubtitledNarratedVideo)
```
