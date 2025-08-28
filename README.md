# mediaichemy: AI-Powered Multimedia Content Creation

⚗️🧪🧫 **mediaichemy** is a Python library for automating the creation, editing, and composition of multimedia content (images, audio, video). It provides modular tools and formulas for building AI-driven media workflows, including file handling, editing, and integration with multiple AI providers.

## Features

- 🤖 Generate and edit images, videos, and audio using AI
- ⚙️ Modular, extensible architecture for customizable workflows
- 👾 Support for multiple AI providers
- Automated media composition and editing
- Unified interface for single and multi-modal media generation

[🧪 Full documentation →](https://mediaichemy.github.io/)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/mediaichemy.git
   cd mediaichemy
   ```
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Set up API keys for supported providers (see below).

## AI Providers

Currently supported providers:

- **Text:** OpenRouter
- **Image:** Runware
- **Video:** MiniMax
- **Speech:** ElevenLabs

These providers were chosen for their flexibility, cost-effectiveness, and popularity. `mediaichemy` is modular, so more providers can be added easily.

### Registration & API Keys

1. Create accounts with each provider.
2. Obtain API keys from their dashboards.
3. Configure API keys as environment variables:
   - `OPENROUTER_API_KEY="your_openrouter_api_key"`
   - `RUNWARE_API_KEY="your_runware_api_key"`
   - `MINIMAX_API_KEY="your_minimax_api_key"`
   - `ELEVENLABS_API_KEY="your_elevenlabs_api_key"`
4. **Alternative:** Use a `configs.toml` file:
   ```toml
   [ai.text.openrouter]
   api_key = "your_openrouter_api_key"

   [ai.image.runware]
   api_key = "your_runware_api_key"

   [ai.video.minimax]
   api_key = "your_minimax_api_key"

   [ai.speech.elevenlabs]
   api_key = "your_elevenlabs_api_key"
   ```

## How to Use

### Single Media

The library provides a unified interface for generating individual media types using AI providers. For example, to generate an image:

```python
from mediaichemy.media_sources.ai.visual import generate_image

# Generate an image using a prompt
image = await generate_image(
    prompt="futuristic cityscape, sunset, vibrant colors, high detail",
    output_path="output/image.jpg"
)

print(f"Image saved at: {image.path}")
```
See more examples in the [documentation](https://mediaichemy.github.io/).

### Multimedia Workflows

The library supports complex workflows for creating multimedia content by combining multiple AI-generated media types and applying audio/video edits. You can use the formulas in `mediaichemy.formulas` or compose your own using the modular editors and sources.

Content can be customized by adding configurations to a `configs.toml` in your working directory.

```python
from mediaichemy.formulas.composite_video import create_composite_video

# Example: Create a composite video from images, audio, and subtitles
result = await create_composite_video(
    images=["input1.jpg", "input2.jpg"],
    audio="narration.mp3",
    subtitles="captions.srt",
    output_path="output/video.mp4"
)

print(f"Composite video created: {result.path}")
```

## Contributing

Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.