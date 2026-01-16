#!/usr/bin/env python3
"""
Coqui TTS Voice Cloning Demo

This script demonstrates various capabilities of Coqui TTS:
1. Basic text-to-speech
2. Voice cloning from a reference audio file
3. Using multilingual models

Requirements:
- Python 3.10+
- TTS library (pip install TTS)
"""

import os
from pathlib import Path
from TTS.api import TTS

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def demo_basic_tts():
    """Demo 1: Basic English TTS using VITS model"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Text-to-Speech")
    print("="*60)
    
    # Initialize TTS with a fast English model
    tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True)
    
    # Sample text
    text = "Hello! This is a demonstration of Coqui TTS. The voice you're hearing is generated entirely by AI."
    
    # Generate speech
    output_path = OUTPUT_DIR / "demo1_basic_tts.wav"
    tts.tts_to_file(text=text, file_path=str(output_path))
    
    print(f"✓ Audio generated: {output_path}")
    print(f"  Text: '{text}'")


def demo_voice_cloning():
    """Demo 2: Voice cloning using XTTS model
    
    Note: For voice cloning, you need a reference audio file.
    Place your reference audio (WAV format, 5-30 seconds) in the project directory.
    """
    print("\n" + "="*60)
    print("DEMO 2: Voice Cloning with XTTS")
    print("="*60)
    
    # Check for reference audio
    reference_audio = "reference_voice.wav"
    
    if not os.path.exists(reference_audio):
        print(f"⚠ Reference audio not found: {reference_audio}")
        print(f"  To test voice cloning:")
        print(f"  1. Record a 5-30 second audio sample")
        print(f"  2. Save it as 'reference_voice.wav' in this directory")
        print(f"  3. Run this script again")
        return
    
    # Initialize XTTS model (supports voice cloning)
    print("Loading XTTS model (this may take a moment)...")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)
    
    # Sample text for cloning
    text = "This is an example of voice cloning. The model is attempting to replicate the voice from the reference audio."
    
    # Generate speech with voice cloning
    output_path = OUTPUT_DIR / "demo2_voice_cloning.wav"
    tts.tts_to_file(
        text=text,
        file_path=str(output_path),
        speaker_wav=reference_audio,
        language="en"
    )
    
    print(f"✓ Cloned voice audio generated: {output_path}")
    print(f"  Text: '{text}'")
    print(f"  Reference: {reference_audio}")


def demo_multilingual():
    """Demo 3: Multilingual TTS with voice cloning"""
    print("\n" + "="*60)
    print("DEMO 3: Multilingual Voice Synthesis")
    print("="*60)
    
    # Initialize XTTS model
    print("Loading multilingual XTTS model...")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)
    
    # Multilingual examples
    examples = [
        ("en", "This is English text being synthesized."),
        ("es", "Este es un ejemplo en español."),
        ("fr", "Ceci est un exemple en français."),
        ("de", "Dies ist ein Beispiel auf Deutsch."),
    ]
    
    for lang, text in examples:
        output_path = OUTPUT_DIR / f"demo3_multilingual_{lang}.wav"
        
        # For multilingual, we can use a reference voice or let it use default
        reference_audio = "reference_voice.wav" if os.path.exists("reference_voice.wav") else None
        
        if reference_audio:
            tts.tts_to_file(
                text=text,
                file_path=str(output_path),
                speaker_wav=reference_audio,
                language=lang
            )
        else:
            # Use built-in speaker
            tts.tts_to_file(
                text=text,
                file_path=str(output_path),
                language=lang
            )
        
        print(f"✓ Generated {lang.upper()} audio: {output_path}")


def list_available_models():
    """List some popular models available in Coqui TTS"""
    print("\n" + "="*60)
    print("POPULAR COQUI TTS MODELS")
    print("="*60)
    
    models = {
        "Voice Cloning": [
            "tts_models/multilingual/multi-dataset/xtts_v2",
            "tts_models/multilingual/multi-dataset/your_tts",
        ],
        "Fast English": [
            "tts_models/en/ljspeech/vits",
            "tts_models/en/ljspeech/fast_pitch",
        ],
        "Multi-speaker": [
            "tts_models/en/vctk/vits",
        ],
        "Multilingual": [
            "tts_models/multilingual/multi-dataset/bark",
        ]
    }
    
    for category, model_list in models.items():
        print(f"\n{category}:")
        for model in model_list:
            print(f"  • {model}")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("COQUI TTS VOICE CLONING DEMO")
    print("="*60)
    print("\nThis demo will showcase Coqui TTS capabilities.")
    print(f"All output files will be saved to: {OUTPUT_DIR.absolute()}\n")
    
    # List available models
    list_available_models()
    
    # Run demos
    try:
        # Demo 1: Basic TTS
        demo_basic_tts()
        
        # Demo 2: Voice cloning (if reference audio available)
        demo_voice_cloning()
        
        # Demo 3: Multilingual (commented out by default as it's slow)
        # Uncomment the line below to try multilingual synthesis
        # demo_multilingual()
        
        print("\n" + "="*60)
        print("DEMO COMPLETE!")
        print("="*60)
        print(f"\n✓ Check the '{OUTPUT_DIR}' folder for generated audio files")
        print("\nNext Steps:")
        print("  1. Listen to the generated audio files")
        print("  2. Add your own reference_voice.wav for voice cloning")
        print("  3. Modify the text in the script to synthesize your own content")
        print("  4. Uncomment demo_multilingual() to try other languages")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure you're using Python 3.10+")
        print("  2. Make sure TTS is installed: pip install TTS")
        print("  3. Check that you have internet connection (models download on first use)")


if __name__ == "__main__":
    main()
