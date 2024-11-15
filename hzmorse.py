import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.fft import fft, fftfreq

RATE = 44100 # hz, number of samples taken per second
FREQ = 100

DOT = 0.1
DASH = 0.3
SPACE = 0.1
C_SPACE = 0.1 # (+2)
W_SPACE = 0.3 # (+4)

morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
    'Z': '--..', ' ': '/'
}

def overlay_audio(audio1, audio2):
    if (len(audio1) < len(audio2)):
        audio1, audio2 = audio2, audio1
    
    audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)), 'constant')
    
    mixed_data = audio1 + audio2
    mixed_data = np.clip(mixed_data, -1.0, 1.0)
    return mixed_data

def generate_tone(duration):
    t = np.linspace(0, duration, int(duration * RATE))
    tone = np.sin(FREQ * 2 * np.pi * t)

    return tone.astype(np.float32)

def create_morse(encode_text):
    morse_text = ' '.join(morse_code_dict[char] for char in encode_text.upper())
    morse_data = np.array([])

    for char in morse_text:
        if char == '.':
            morse_data = np.concatenate((morse_data, generate_tone(DOT)))
        elif char == '-':
            morse_data = np.concatenate((morse_data, generate_tone(DASH)))
        elif char == ' ':
            morse_data = np.concatenate((morse_data, np.zeros(int(RATE * C_SPACE))))
        elif char == '/':
            morse_data = np.concatenate((morse_data, np.zeros(int(RATE * W_SPACE))))

        morse_data = np.concatenate((morse_data, np.zeros(int(RATE * SPACE))))

    return morse_data 
     


def main():
    # background_audio = 'audio/PinkPanther30.wav'   
    # background_data, sample_rate = sf.read(background_audio)

    print('Input string to encode:')
    encode_text = input()

    morse_data = create_morse(encode_text)
    # sd.play(morse_data, samplerate=RATE, blocksize=2048)
    # mixed_data = overlay_audio(background_data * 0.9, morse_data * 0.1)

    # try: 
    #     while True:
    #         True        
    # except KeyboardInterrupt:
    #     print("Exiting gracefully...")

    sf.write(f'audio/morse{FREQ}_{encode_text}.wav', morse_data, RATE)

if __name__ == "__main__":
    main()