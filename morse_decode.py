import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.fft import fft, fftfreq

RATE = 44100 # hz, number of samples taken per second
FREQ = 440

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
    t = np.linspace(0, duration, (duration * RATE) // MORSE_DIV)
    tone = np.sin(FREQ * 2 * np.pi * t)

    return tone.astype(np.float32)

def decode_morse(morse_data, sample_rate):
    morse_sequence = ""
    tone_detected = False
    current_signal = []
    
    for i in range(0, len(morse_data), int(sample_rate * DOT)):
        segment = morse_data[i:i + int(sample_rate * DOT)]
        yf = fft(segment, n=len(segment))
        xf = fftfreq(len(segment), 1 / sample_rate)

        magnitude = np.abs(yf)
        
        peak_index = np.argmax(magnitude[:len(magnitude) // 2])
        peak_freq = xf[peak_index]

        if peak_freq > FREQ:
            morse_sequence += '.'
        else:
            morse_sequence += ' '
          

    morse_sequence = morse_sequence.replace('...', '-')
    morse_sequence = morse_sequence.replace('  ', '/')
    morse_sequence = morse_sequence.replace(' ', '')
    morse_sequence = morse_sequence.replace('/', ' ')

    print(morse_sequence)
     

def main():
    morse_audio = 'audio/morse440_hello world.wav'   
    morse_data, sample_rate = sf.read(morse_audio)

    decode_morse(morse_data.flatten(), sample_rate=sample_rate)
    # sd.play(morse_data, samplerate=RATE, blocksize=2048)
    
    # try: 
    #     while True:
    #         True        
    # except KeyboardInterrupt:
    #     print("Exiting gracefully...")

    # mixed_data = overlay_audio(background_data * 0.9, spect_data * 0.1)

    # sf.write(f'audio/morse{FREQ}_{encode_text}.wav', morse_data, RATE)

if __name__ == "__main__":
    main()