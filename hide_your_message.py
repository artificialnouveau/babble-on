import numpy as np
import librosa
import soundfile as sf

def modulate_and_merge(audio_path, message_path, output_path):
    # Load audio files
    audio, sr = librosa.load(audio_path, sr=None)
    message, sr_msg = librosa.load(message_path, sr=None)

    # Modulate the message to frequencies higher than 20kHz
    # First, take the Fourier transform of the message
    message_fft = np.fft.rfft(message)
    
    # Then, shift the frequencies by 20000 Hz
    shift_amount = 20000 // (sr_msg // 2)  # Convert to bin index
    message_fft_shifted = np.roll(message_fft, shift_amount)
    
    # Set the lower frequencies to zero
    message_fft_shifted[:shift_amount] = 0
    
    # Then, do the inverse Fourier transform to get the time domain signal
    message_shifted = np.fft.irfft(message_fft_shifted)

    # Resize the message to match the audio length
    if len(message_shifted) < len(audio):
        message_shifted = np.pad(message_shifted, (0, len(audio) - len(message_shifted)))
    else:
        message_shifted = message_shifted[:len(audio)]

    # Add the shifted message to the audio
    audio_with_message = audio + message_shifted

    # Save the output audio
    sf.write(output_path, audio_with_message, sr)

# Run the function
modulate_and_merge('babbleon.wav', 'message.wav', 'output.wav')

def demodulate(audio_path, output_path):
    # Load the audio file
    audio, sr = librosa.load(audio_path, sr=None)

    # Take the Fourier transform of the audio
    audio_fft = np.fft.rfft(audio)

    # Shift the frequencies back down
    shift_amount = 20000 // (sr // 2)  # Convert to bin index
    audio_fft_shifted = np.roll(audio_fft, -shift_amount)
    
    # Set the higher frequencies to zero
    audio_fft_shifted[-shift_amount:] = 0
    
    # Do the inverse Fourier transform to get the time domain signal
    message = np.fft.irfft(audio_fft_shifted)

    # Save the output audio
    sf.write(output_path, message, sr)

# Run the function
demodulate('output.wav', 'extracted_message.wav')

def phase_invert_remove(audio_path, remix_path, output_path):
    # Load the audio files
    audio, sr = librosa.load(audio_path, sr=None)
    remix, sr_remix = librosa.load(remix_path, sr=None)

    # Make sure the audio files are the same length
    if len(audio) < len(remix):
        remix = remix[:len(audio)]
    elif len(audio) > len(remix):
        audio = audio[:len(remix)]

    # Invert the phase of the remix
    remix_inverted = -remix

    # Add the inverted remix to the audio
    message = audio + remix_inverted

    # Save the output audio
    sf.write(output_path, message, sr)

# Run the function
phase_invert_remove('output.wav', 'babbleon.wav', 'message_recovered.wav')


def mask_message(audio_path, message_path, output_path, mask_volume=0.01):
    # Load audio files
    audio, sr = librosa.load(audio_path, sr=None)
    message, sr_msg = librosa.load(message_path, sr=None)

    # Resize the message to match the audio length
    if len(message) < len(audio):
        message = np.pad(message, (0, len(audio) - len(message)))
    else:
        message = message[:len(audio)]

    # Reduce the volume of the message
    message_masked = message * mask_volume

    # Add the masked message to the audio
    audio_with_message = audio + message_masked

    # Save the output audio
    sf.write(output_path, audio_with_message, sr)

# Run the function
mask_message('babbleon.wav', 'message.wav', 'output_masked.wav')


def unmask_message(output_masked_path, remix_path, output_path):
    # Load the audio files
    output_masked, sr = librosa.load(output_masked_path, sr=None)
    remix, sr_remix = librosa.load(remix_path, sr=None)

    # Make sure the audio files are the same length
    if len(output_masked) < len(remix):
        remix = remix[:len(output_masked)]
    elif len(output_masked) > len(remix):
        output_masked = output_masked[:len(remix)]

    # Subtract the remix from the output_masked
    message = output_masked - remix

    # Save the output audio
    sf.write(output_path, message, sr)

# Run the function
unmask_message('output_masked.wav', 'final_remix.wav', 'message_recovered.wav')

