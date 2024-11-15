import numpy as np
import sounddevice as sd
import soundfile as sf

CHANNEL = 1 #default mono

def overlay_audio(audio1, audio2):
    if (len(audio1) < len(audio2)):
        audio1, audio2 = audio2, audio1
    
    audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)), 'constant')
    
    mixed_data = audio1 + audio2
    mixed_data = np.clip(mixed_data, -1.0, 1.0)
    return mixed_data

def create_spectrogram(encode_text):
    # only alphabet letters allowed
    encode_text = encode_text.upper()
    spect_data = np.empty((0, 2))

    for letter in encode_text:
        # letter_data, _ = sf.read(f'audio/spect_{letter}.wav')
        letter_data, _ = sf.read(f'audio/Coagula10.wav')
        spect_data = np.concatenate((spect_data, letter_data), axis=0)

    if CHANNEL == 1:
        spect_data = spect_data[:, 0]
    return spect_data

def main():
    background_audio = 'audio/Hungry.wav'   
    background_data, sample_rate = sf.read(background_audio)
    background_data = background_data[:, 0]

    print('Input string to encode:')
    encode_text = input()

    print(sample_rate)
    spect_data = create_spectrogram(encode_text)
    mixed_data = overlay_audio(background_data * 0.9, spect_data * 0.0005)

    sf.write(f'audio/spectogram1_{encode_text}.wav', mixed_data, sample_rate)

if __name__ == "__main__":
    main()

# test: abcdefghijklmnopqrstuvwxyz