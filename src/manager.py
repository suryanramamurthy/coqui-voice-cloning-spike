
import os
import json
import shutil
import glob
import wave
import numpy as np
from scipy.io import wavfile
from pathlib import Path
from typing import List, Optional, Dict

class VoiceManager:
    def __init__(self, base_dir: str = "voices"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
    def create_new_recording_path(self, voice_name: str) -> str:
        """Generate a path for a new recording file."""
        voice_id = self._sanitize_name(voice_name)
        audio_dir = self.base_dir / voice_id / "audio"
        count = len(list(audio_dir.glob("*.wav")))
        return str(audio_dir / f"recording_{count + 1}.wav")
        
    def _trim_silence(self, audio: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """Trim silence from start and end of audio array."""
        magnitude = np.abs(audio)
        if np.max(magnitude) < threshold:
            return audio
            
        # Find start and end points
        is_speech = magnitude > (np.max(magnitude) * threshold)
        indices = np.where(is_speech)[0]
        
        if len(indices) == 0:
            return audio
            
        start = indices[0]
        end = indices[-1]
        
        # Add a small buffer (0.1s at 22050Hz is ~2200 samples)
        buffer = 2000
        start = max(0, start - buffer)
        end = min(len(audio), end + buffer)
        
        return audio[start:end]

    def process_audio(self, voice_name: str) -> bool:
        """
        Refinement Logic:
        Merge all .wav files in the audio directory into a single 'combined.wav'.
        Trims silence from each clip before merging to avoid "glitchy" reference.
        """
        voice_id = self._sanitize_name(voice_name)
        voice_dir = self.base_dir / voice_id
        audio_dir = voice_dir / "audio"
        processed_dir = voice_dir / "processed"
        
        wav_files = sorted(list(audio_dir.glob("*.wav")))
        if not wav_files:
            return False
            
        outfile = processed_dir / "combined.wav"
        
        try:
            combined_audio = []
            sample_rate = 0
            
            for wav_path in wav_files:
                sr, audio = wavfile.read(str(wav_path))
                sample_rate = sr
                
                # Normalize to float usually helpful, but keeping int16 is fine if consistent
                # Trim silence
                trimmed = self._trim_silence(audio)
                combined_audio.append(trimmed)
                
                # Add a tiny bit of silence between clips (0.2s)
                silence_len = int(sr * 0.2)
                combined_audio.append(np.zeros(silence_len, dtype=audio.dtype))
            
            if not combined_audio:
                return False
                
            # Concatenate
            final_audio = np.concatenate(combined_audio)
            
            # Write
            wavfile.write(outfile, sample_rate, final_audio)
            
            print(f"✓ Refinement complete: Merged {len(wav_files)} samples into {outfile}")
            return True
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return False

    def create_voice(self, name: str, description: str = "") -> bool:
        """Create a new voice profile directory structure."""
        voice_id = self._sanitize_name(name)
        voice_dir = self.base_dir / voice_id
        
        if voice_dir.exists():
            print(f"Error: Voice '{name}' already exists.")
            return False
            
        # Create directories
        (voice_dir / "audio").mkdir(parents=True)
        (voice_dir / "processed").mkdir(parents=True)
        
        # Create metadata
        metadata = {
            "name": name,
            "id": voice_id,
            "description": description,
            "created_at": str(os.path.getctime(voice_dir) if voice_dir.exists() else 0), # Placeholder or use datetime
            "base_model": "xtts_v2"
        }
        
        self._save_metadata(voice_id, metadata)
        print(f"✓ Voice profile '{name}' created at {voice_dir}")
        return True

    def list_voices(self) -> List[Dict]:
        """List all available voice profiles."""
        voices = []
        if not self.base_dir.exists():
            return voices
            
        for voice_dir in self.base_dir.iterdir():
            if voice_dir.is_dir() and (voice_dir / "metadata.json").exists():
                try:
                    with open(voice_dir / "metadata.json", 'r') as f:
                        voices.append(json.load(f))
                except Exception as e:
                    print(f"Warning: Could not read metadata for {voice_dir.name}: {e}")
        return voices

    def get_voice_path(self, voice_name: str) -> Optional[Path]:
        """Get the path to a voice directory by name or ID."""
        voice_id = self._sanitize_name(voice_name)
        path = self.base_dir / voice_id
        return path if path.exists() else None
        
    def get_reference_audio(self, voice_name: str) -> Optional[str]:
        """
        Get the best reference audio for inference.
        Prioritizes 'processed/combined.wav' -> 'audio/recording_0.wav' -> Any wav in audio.
        """
        path = self.get_voice_path(voice_name)
        if not path:
            return None
            
        # 1. Check for processed/combined master file
        combined = path / "processed" / "combined.wav"
        if combined.exists():
            return str(combined)
            
        # 2. Check for any raw recording
        audio_dir = path / "audio"
        wavs = list(audio_dir.glob("*.wav"))
        if wavs:
            # Sort to get deterministic result, e.g., the latest or first
            wavs.sort() 
            return str(wavs[0])
            
        return None

    def _sanitize_name(self, name: str) -> str:
        """Convert display name to filesystem-safe ID."""
        return "".join(c for c in name.lower() if c.isalnum() or c in ('_', '-')).strip()

    def _save_metadata(self, voice_id: str, metadata: Dict):
        with open(self.base_dir / voice_id / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=4)
