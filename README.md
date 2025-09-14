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
