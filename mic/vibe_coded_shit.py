import Adafruit_ADS1x15
import numpy as np
import librosa
import time
adc = Adafruit_ADS1x15.ADS1115(busnum=1)
# Setup ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2/3  # Adjust gain as per signal strength
SAMPLERATE = 16000  # Target audio sampling rate (16 kHz)
DURATION = 2  # Capture 2 seconds of audio

def capture_audio(duration, samplerate):
    num_samples = duration * samplerate  # Total samples to collect
    audio_signal = []

    print("Recording...")
    start_time = time.time()
    
    while len(audio_signal) < num_samples:
        value = adc.read_adc(0, gain=GAIN)  # Read from A0
        audio_signal.append(value)

        # Ensure real-time sampling at 16kHz
        while (time.time() - start_time) < (len(audio_signal) / samplerate):
            pass

    print("Recording finished.")
    
    return np.array(audio_signal, dtype=np.float32)

# Capture 2 seconds of audio
raw_audio = capture_audio(DURATION, SAMPLERATE)
