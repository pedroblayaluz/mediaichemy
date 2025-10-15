# 🧪 mediaichemy: cost-effective AI powered content creation

`mediaichemy` is a Python library for generating **cheap and cost effective** multimedia content using AI. It intelligently selects models and workflows to minimize costs while delivering high-quality results.

The library relies on:
- [Runware](https://runware.ai) for image and video generation
- [OpenRouter](https://openrouter.ai) for general AI and text completions
- [Piper TTS](https://github.com/OHF-Voice/piper1-gpl?tab=readme-ov-file): text-to-speech synthesis
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
1. Install mediaichemy directly from PyPI:

```bash
pip install mediaichemy
```

2. Set up API keys for OpenRouter and Runware (see below).


## Setting up API keys

#### 1. Create an [OpenRouter Account](https://openrouter.ai/signup)
- Obtain an [Openrouter API key](https://openrouter.ai/keys)
#### 2. Create a [Runware Account](https://runware.ai)
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

Each `Media` type creates a specific form of content using AI and editing tools to craft it.

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
image = await Image(params=image_params).create()
```
<img src="tests/examples/image/skateboard_cat.png" width="400" alt="Skateboard Cat">


#### Video
```python
from mediaichemy.media.single import Video
from mediaichemy.media.parameters import VideoParameters

video_params = VideoParameters(
    video_prompt="A dog floating in outer space",
    video_model="bytedance:1@1",
    width=1088,
    height=1920
)
video = await Video(params=video_params).create()
```

https://github.com/user-attachments/assets/da8a297b-3808-49e1-b635-7358339a0d49


#### Narration
```python
from mediaichemy.media.single import Narration
from mediaichemy.media.parameters import NarrationParameters

narration_params = NarrationParameters(
    narration_text=("A student asked the master, "
                    "What is the sound of one hand clapping? "
                    "The master simply held up his hand."),
    narration_voice_name="en_US-joe-medium",
    narration_silence_tail=5,
    narration_speed=1.0
)
narration = await Narration(params=narration_params).create()
```
<audio src="tests/examples/narration/koan.mp3" controls></audio>
### Multi Media Examples
Media created combining multiple AI sources.

#### Image Video
A video created by first creating an image, then animating it.
Enabling more customization on the starter image.

```python
from mediaichemy.media.multi import ImageVideo
from mediaichemy.media.parameters import ImageVideoParameters

image_video_params = ImageVideoParameters(
    video_prompt="A hyper realistic pink mantis wearing a tuxedo.",
    image_model="rundiffusion:110@101",
    video_model="bytedance:1@1",
    width=1088,
    height=1920
)
image_video = await ImageVideo(params=image_video_params).create()
```
https://github.com/user-attachments/assets/515ea7ee-2084-44eb-a4b8-90cb4602e4a7

#### Storyline Video
```python
from mediaichemy.media.multi import StorylineVideo
from mediaichemy.media.parameters import StorylineVideoParameters

storyline_video_params = StorylineVideoParameters(
    video_prompt="A forest in the rain",
    image_model="rundiffusion:110@101",
    video_model="bytedance:1@1",
    width=1088,
    height=1920,
    narration_text="Listen to the rain.",
    narration_voice_name="en_US-joe-medium",
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
storyline_video = await StorylineVideo(params=storyline_video_params).create()
```
https://github.com/user-attachments/assets/16e9170f-eab2-442a-a8d5-87204acbd662
## Using the MediaCreator

By using `MediaCreator`, you let AI create ideas for you. You can use it to generate content for a specific media type or let it pick the best type for you automatically based on your prompt.

### MediaCreator

#### Using MediaCreator with a specific media type

```python
from mediaichemy.creator import MediaCreator
from mediaichemy.media import StorylineVideo

creator = MediaCreator(
    creator_model='anthropic/claude-sonnet-4.5',
    media_type=StorylineVideo)

media = await creator.create(user_prompt=(
    "Create a short video telling a zen koan."
    "The video features a hyperrealistic detailed natural setting."),
    narration_voice_name='en_US-joe-medium')
```
https://github.com/user-attachments/assets/4dbaf275-0070-4117-a816-f5c775d39c91



#### Letting MediaCreator pick the best media type

```python
from mediaichemy.creator import MediaCreator

creator = MediaCreator()  # No media_type specified
media = await creator.create(
    user_prompt="Create an image of a dog wearing a space helmet."
)
```
<img src="tests/examples/image/astro_dog.jpg" width="400" alt="Astro Dog">
