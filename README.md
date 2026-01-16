# Coqui TTS Voice Cloning Spike

This project demonstrates voice cloning capabilities using Coqui TTS on macOS (M3 Pro).

## Setup

### 1. System Dependencies
- **espeak-ng**: Required for text-to-phoneme conversion
  ```bash
  # Install on macOS
  brew install espeak-ng
  ```

### 2. Environment
- Python 3.11+ (required for compatibility)
- Virtual environment already configured

### 3. Installation
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install TTS sounddevice scipy numpy
```

## Voice Management System (NEW)
**[--> Go to Voice Manager Guide](VOICE_MANAGER_README.md)**

We have upgraded the project with a full CLI system to manage multiple voices, record audio, and refine clones.

```bash
# Quick Example
python -m src.cli new "MyClone"
python -m src.cli record "MyClone"
python -m src.cli speak "MyClone" "Hello world"
```

## Project Structure

```
coqui_voice_cloning_spike/
├── venv/                          # Virtual environment
├── src/                           # Source code (manager, synthesizer, recorder)
├── voices/                        # Database of voice profiles
├── voice_cloning_demo.py          # Original demo script
├── VOICE_MANAGER_README.md        # Guide for new system
└── output/                        # Generated output
```

## Quick Start

### Run the Demo
```bash
# Activate virtual environment
source venv/bin/activate

# Run demo script
python voice_cloning_demo.py
```

### What the Demo Does

1. **Basic TTS**: Generates speech from text using a pre-trained English model
2. **Voice Cloning**: Clones your voice from a reference audio (if provided)
3. **Multilingual**: Synthesizes speech in multiple languages

## Voice Cloning

To test voice cloning with your own voice:

1. Record a 5-30 second audio sample of yourself speaking clearly
2. Save it as `reference_voice.wav` in this directory
3. Run the demo script again

The XTTS model will attempt to replicate your voice characteristics.

## Available Models

### Voice Cloning Models
- `tts_models/multilingual/multi-dataset/xtts_v2` - Best for voice cloning
- `tts_models/multilingual/multi-dataset/your_tts` - Alternative multi-speaker model

### Fast English Models
- `tts_models/en/ljspeech/vits` - Fast, high-quality English
- `tts_models/en/ljspeech/fast_pitch` - Very fast synthesis

### Multilingual Models
- `tts_models/multilingual/multi-dataset/bark` - Supports many languages

## Usage Examples

### Basic Python Usage
```python
from TTS.api import TTS

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/vits")

# Generate speech
tts.tts_to_file(
    text="Hello, this is a test!",
    file_path="output.wav"
)
```

### Voice Cloning
```python
from TTS.api import TTS

# Initialize XTTS model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Clone voice
tts.tts_to_file(
    text="This will sound like the reference voice.",
    file_path="cloned_output.wav",
    speaker_wav="reference_voice.wav",
    language="en"
)
```

### Command Line
```bash
# List all available models
tts --list_models

# Generate speech from command line
tts --model_name "tts_models/en/ljspeech/vits" \
    --text "Hello from the command line!" \
    --out_path output.wav

# Voice cloning from CLI
tts --model_name "tts_models/multilingual/multi-dataset/xtts_v2" \
    --text "Clone my voice!" \
    --speaker_wav reference_voice.wav \
    --language_idx en \
    --out_path cloned.wav
```

## Supported Languages (XTTS v2)

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Polish (pl)
- Turkish (tr)
- Russian (ru)
- Dutch (nl)
- Czech (cs)
- Arabic (ar)
- Chinese (zh-cn)
- Japanese (ja)
- Hungarian (hu)
- Korean (ko)
- Hindi (hi)

## Performance Notes

### M3 Pro Performance
- Model loading: 5-15 seconds (first time downloads models)
- Basic TTS: ~1-2 seconds per sentence
- Voice cloning: ~3-5 seconds per sentence

### Optimization Tips
- Models are cached after first download
- Use smaller models (e.g., `vits`) for faster inference
- XTTS models are larger but provide better quality and voice cloning

## Troubleshooting

### Python Version Error
If you see errors about type hints (`|` operator), you need Python 3.10+:
```bash
# Check your Python version
python3.11 --version

# Recreate venv with correct version
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install TTS
```

### Model Download Issues
- Ensure you have a stable internet connection
- Models download automatically on first use
- Cache location: `~/.local/share/tts/`

### Audio Quality
- Use high-quality reference audio (WAV format, 22050 Hz or higher)
- Reference should be 5-30 seconds long
- Clear speech without background noise works best

## Next Steps

1. Test the basic demo
2. Record your own voice sample
3. Experiment with different models
4. Try multilingual synthesis
5. Integrate into your own applications

## Resources

- [Coqui TTS Documentation](https://docs.coqui.ai/)
- [GitHub Repository](https://github.com/coqui-ai/TTS)
- [Model Zoo](https://github.com/coqui-ai/TTS/wiki/Released-Models)

## License

Coqui TTS is released under the Mozilla Public License 2.0.
