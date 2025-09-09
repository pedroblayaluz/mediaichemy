import random
import os


def load_prompt_file(filename):
    """Load prompt text from a file"""
    with open(filename, 'r') as file:
        return file.read()


def load_random_prompt(directory='prompts'):
    try:
        prompt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        if not prompt_files:
            return None, "No prompt files found"
        filename = random.choice(prompt_files)
        with open(os.path.join(directory, filename), 'r') as file:
            prompt = file.read()
        return prompt
    except FileNotFoundError:
        return None, f"Directory '{directory}' not found"
