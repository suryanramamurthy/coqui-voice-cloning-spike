
import argparse
import sys
from pathlib import Path
from src.manager import VoiceManager
from src.synthesis import Synthesizer
from src.recorder import AudioRecorder

def main():
    parser = argparse.ArgumentParser(description="Voice Cloning Management System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: NEW
    parser_new = subparsers.add_parser("new", help="Create a new voice profile")
    parser_new.add_argument("name", type=str, help="Name of the voice")
    parser_new.add_argument("--desc", type=str, default="", help="Description")

    # Command: RECORD
    parser_rec = subparsers.add_parser("record", help="Record audio samples")
    parser_rec.add_argument("voice", type=str, help="Name of the voice")
    parser_rec.add_argument("--duration", type=int, default=5, help="Duration in seconds")
    
    # Command: REFINE
    parser_refine = subparsers.add_parser("refine", help="Process recordings into a master reference")
    parser_refine.add_argument("voice", type=str, help="Name of the voice")

    # Command: LIST
    parser_list = subparsers.add_parser("list", help="List all voice profiles")

    # Command: SPEAK
    parser_speak = subparsers.add_parser("speak", help="Generate speech")
    parser_speak.add_argument("voice", type=str, help="Name of the voice to use")
    parser_speak.add_argument("text", type=str, help="Text to speak")
    parser_speak.add_argument("--lang", type=str, default="en", help="Language code (en, es, fr, etc.)")
    parser_speak.add_argument("--out", type=str, default="output.wav", help="Output filename")

    args = parser.parse_args()
    
    manager = VoiceManager()
    
    if args.command == "new":
        manager.create_voice(args.name, args.desc)
        
    elif args.command == "record":
        path = manager.get_voice_path(args.voice)
        if not path:
            print(f"Error: Voice '{args.voice}' does not exist. Create it first.")
            return
            
        output_path = manager.create_new_recording_path(args.voice)
        recorder = AudioRecorder()
        if recorder.record(args.duration, output_path):
            # Auto-refine after recording
            manager.process_audio(args.voice)
            
    elif args.command == "refine":
        manager.process_audio(args.voice)
        
    elif args.command == "list":
        voices = manager.list_voices()
        if not voices:
            print("No voices found. Create one with 'new <name>'")
        else:
            print("\nAvailable Voices:")
            print(f"{'Name':<20} {'ID':<20} {'Description'}")
            print("-" * 60)
            for v in voices:
                print(f"{v['name']:<20} {v['id']:<20} {v['description']}")
            print("-" * 60)
            
    elif args.command == "speak":
        # Check if voice exists and has audio
        ref_audio = manager.get_reference_audio(args.voice)
        if not ref_audio:
            print(f"❌ Error: Voice '{args.voice}' has no reference audio!")
            print(f"   Please record audio for this voice first (feature coming soon).")
            print(f"   Or manually add .wav files to voices/{manager._sanitize_name(args.voice)}/audio/")
            return

        synthesizer = Synthesizer()
        output = synthesizer.speak(
            text=args.text, 
            output_path=args.out, 
            reference_audio_path=ref_audio, 
            language=args.lang
        )
        print(f"✓ Generated audio: {output}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
