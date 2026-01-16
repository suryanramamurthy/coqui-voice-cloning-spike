
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import sys
from pathlib import Path

class AudioRecorder:
    def __init__(self, sample_rate=22050):
        self.fs = sample_rate  # XTTS performs best with 22050 or 24000
        
    def list_devices(self):
        print("\nAvailable Audio Devices:")
        print(sd.query_devices())
        
    def record(self, duration_sec: int, output_path: str):
        """Record audio for a fixed duration."""
        print(f"\n🎙️  Recording for {duration_sec} seconds...")
        print("   (Speak clearly and normally)")
        
        try:
            # Record
            recording = sd.rec(int(duration_sec * self.fs), samplerate=self.fs, channels=1)
            
            # Show progress bar
            for _ in range(duration_sec):
                time.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()
            print("\n")
            
            sd.wait()  # Wait until recording is finished
            
            # Save raw file
            # Scale to 16-bit integer for WAV compatibility if needed, 
            # or scipy handles float32 (-1.0 to 1.0) usually fine.
            # Best practice for compatibility: convert to int16.
            recording_int16 = (recording * 32767).astype(np.int16)
            
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            write(output_path, self.fs, recording_int16)
            print(f"✓ Saved recording to: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Recording failed: {e}")
            return False
