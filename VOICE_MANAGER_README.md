# Voice Management System Guide

A powerful CLI tool to manage, record, and synthesize custom voices using Coqui TTS.

## Features
- **Voice Database**: Organize multiple voice profiles.
- **Audio Recorder**: Built-in tool to record your voice.
- **Refinement**: Automatically merges multiple recordings to improve voice quality.
- **Synthesis**: Generate speech using your custom voices.

## Quick Start

### 1. Create a Voice Profile
```bash
python -m src.cli new "Suryan" --desc "My personal voice clone"
```

### 2. Record Audio
Record 5 seconds of audio (repeat this 3-5 times for better results):
```bash
python -m src.cli record "Suryan" --duration 5
```
*   **Tip**: Read different sentences each time to cover more phonemes.
*   **Auto-Refine**: The system automatically merges your new recording with previous ones to create a master reference file (`voices/suryan/processed/combined.wav`).

### 3. Generate Speech
```bash
python -m src.cli speak "Suryan" "Hello! This is my cloned voice speaking." --out output.wav
```

### 4. Manage Voices
List all available voices:
```bash
python -m src.cli list
```

## Directory Structure
Your voices are stored in the `voices/` directory:
```
voices/
└── suryan/
    ├── metadata.json       # Voice details
    ├── audio/              # Raw recordings (recording_1.wav, ...)
    └── processed/          # Combined master reference (combined.wav)
```

## Advanced Usage

### Importing Existing Audio
If you already have audio files, you don't need to use the record command.
1.  Create the voice: `python -m src.cli new "Celebrity"`
2.  Copy .wav files to `voices/celebrity/audio/`
3.  Run refinement manually:
    ```bash
    python -m src.cli refine "Celebrity"
    ```

### Troubleshooting
*   **No Reference Audio**: If `speak` fails, ensure you have recorded at least one sample or manually added files to the `audio/` folder.
*   **Recording Errors**: Ensure your microphone is accessible and `portaudio` is installed (`brew install portaudio`).
