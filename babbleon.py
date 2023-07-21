import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.generators import WhiteNoise
from pydub.playback import play
from pydub.effects import reverb

def remix_audio(audio_path, number_of_versions):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Slide up audio based on onset segments
    onset_frames = librosa.onset.onset_detect(y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    segments = []
    for i in range(len(onset_times) - 1):
        start = onset_times[i]
        end = onset_times[i+1]
        start_sample = int(start * sr)
        end_sample = int(end * sr)
        segment = y[start_sample:end_sample]
        segments.append(segment)
        
    # Create multiple versions of the randomized combined segmented audio
    mixed = []
    for i in range(number_of_versions):
        np.random.shuffle(segments)
        mixed_segment = np.concatenate(segments)
        mixed.append(mixed_segment)
    
    # Combine the different versions into one and apply panning
    # Convert to stereo
    stereo_mix = []
    for mix in mixed:
        audio_segment = AudioSegment(mix.tobytes(), frame_rate=sr, sample_width=mix.dtype.itemsize, channels=1)
        pan_value = np.random.uniform(-1, 1)  # random panning
        audio_segment = audio_segment.pan(pan_value)  # pan audio
        stereo_mix.append(audio_segment)
    
    # Overlay the different versions
    overlay_audio = stereo_mix[0]
    for i in range(1, len(stereo_mix)):
        overlay_audio = overlay_audio.overlay(stereo_mix[i])
    
    # Add a bit of reverb to the recording
    overlay_audio = reverb(overlay_audio)
    
    # Export the final remix
    overlay_audio.export("babbleon.wav", format="wav")

# Run the function
remix_audio('your_audio_file_path.wav', 3)
