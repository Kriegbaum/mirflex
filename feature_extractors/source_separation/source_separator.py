import demucs.separate
import os
import shutil
import time
from pydub import AudioSegment


def separate_audio(audio_path, output_dir="/proj/mirflex/files/temp/"):
    # Perform the separation :
    demucs.separate.main(['--out', f'{output_dir}', f'{audio_path}'])

    # Move files from the subdirectory to the specified output_dir
    subdirectory = os.path.join(output_dir, 'htdemucs', os.path.splitext(os.path.basename(audio_path))[0])  # Extract file name without extension
    for stem in ["vocals", "drums", "bass", "other"]:
        stem_file_wav = os.path.join(subdirectory, f"{stem}.wav")
        stem_file_mp3 = os.path.join(output_dir, f"{stem}.mp3")
        
        # Convert WAV to MP3
        audio_segment = AudioSegment.from_wav(stem_file_wav)
        print("Converting ", stem_file_wav, "to", stem_file_mp3)
        audio_segment.export(stem_file_mp3, format="mp3")
        
        # Remove the WAV file
        os.remove(stem_file_wav)

    # Remove the empty subdirectory
    os.rmdir(subdirectory)

    prediction = {
        "raw": audio_path,
        "vocals": os.path.join(output_dir, "vocals.mp3"),
        "drums": os.path.join(output_dir, "drums.mp3"),
        "bass": os.path.join(output_dir, "bass.mp3"),
        "other": os.path.join(output_dir, "other.mp3")
    }

    return prediction
