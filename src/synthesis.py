
from TTS.api import TTS
import torch
import os

class Synthesizer:
    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        self.model_name = model_name
        self.tts = None
    
    def load_model(self):
        """Lazy load the model to save resources if just managing files."""
        if not self.tts:
            print(f"⏳ Loading TTS model: {self.model_name}...")
            # Check for GPU (MPS on Mac)
            gpu = False
            if torch.backends.mps.is_available():
                gpu = True
                print("✓ Using MPS (Apple Silicon) acceleration")
            
            self.tts = TTS(self.model_name, progress_bar=True, gpu=gpu)
            
    def speak(self, text: str, output_path: str, reference_audio_path: str = None, language: str = "en"):
        """Synthesize speech to a file."""
        self.load_model()
        
        if reference_audio_path and os.path.exists(reference_audio_path):
            print(f"🗣️ Synthesizing with reference: {os.path.basename(reference_audio_path)}")
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio_path,
                language=language
            )
        else:
            print("ℹ️ No reference audio provided, using default/random speaker.")
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                language=language
            )
        
        return output_path
