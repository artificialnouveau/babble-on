# Babble On

A babble tape is an audio recording typically used in acoustic studies and research, especially in the area of speech privacy and noise masking. It contains a mix of indistinct voices or background noise, often referred to as "babble noise." In offices or public spaces, a babble tape can be used to create a consistent background noise level to help mask conversations, thus ensuring speech privacy. It is less distracting and more natural-sounding than white noise, and it helps to prevent eavesdropping by making individual conversations less intelligible. This encrypted audio environment aims to create an ambiant and private soundscape, while ensuring the integrity and confidentiality of sound content.

The objective of this proposal is to develop an acoustic approach to an "Encrypted Soundscape," a secure auditory environment that ensures private conversations, confidential interactions, and sensitive acoustic data remain protected from unauthorized access or eavesdropping.

# Audio Processing with Python

This repository contains a series of Python functions for manipulating audio files. Using the powerful librosa and soundfile libraries, you can remix an audio file, hide a 'message' inside it, modulate the 'message' to frequencies higher than 20kHz, remove the remix from the modulated file to recover the 'message', or mask the 'message' inside the remix.

[Sample of the produced babble tape](https://user-images.githubusercontent.com/46301511/235486598-da609584-7974-4b94-aef0-743e615e144e.mov)


## Requirements

This project requires the following Python libraries:

- `numpy`
- `librosa`
- `soundfile`
- `scipy`

You can install these libraries with pip:

```
pip install numpy librosa soundfile scipy
```

## Functions

### remix_audio

This function takes an audio file, breaks it up into segments based on onset detection, randomly reorders the segments, and overlays multiple versions of the remixed audio with different panning. It also applies a bit of reverb to the output. The output is a 'remixed' version of the input audio.

### modulate_and_merge

This function takes two audio files, modulates the frequency of the 'message' file to be higher than 20kHz (a range generally inaudible to humans), and adds it to the 'audio' file. This effectively hides the 'message' inside the 'audio'.

### demodulate

This function takes an audio file (presumably one that has had a 'message' modulated and merged into it) and shifts the frequencies back down to the audible range, effectively extracting the 'message'.

### phase_invert_remove

This function removes a 'remix' audio from an 'output' audio by inverting the phase of the 'remix' and adding it to the 'output'. This effectively cancels out the 'remix' and leaves just the 'message'.

### mask_message

This function adds a 'message' audio to a 'remix' audio in such a way that it is masked by the louder 'remix'. This is achieved by reducing the volume of the 'message' before adding it to the 'remix'.

### unmask_message

This function attempts to extract a 'message' that has been masked inside an 'output_masked' audio by subtracting the 'remix' audio from it. This is only possible if the 'remix' audio has not been altered after being merged with the 'message'.

## Note

These functions are provided as is and may not work as expected in all circumstances, due to limitations in audio file formats, playback equipment, and the complexity of real-world sounds. In particular, the modulation/demodulation functions assume there is no significant content in the audio above 20kHz, which may not be true in many cases. Similarly, the phase inversion function assumes that the 'remix' has not been modified in any way after being added to the 'output', and that there is no additional noise or sounds in the 'output' that could interfere with the phase cancellation. Finally, the masking/unmasking functions work best when the 'message' is significantly quieter than the 'remix', but this could also make the 'message' completely inaudible and irrecoverable.
