import smbus
import time
import numpy as np
from scipy.io.wavfile import write

bus = smbus.SMBus(1)
ADS1115_ADDR = 0x48
CONVERSION_REG = 0x00
CONFIG_REG = 0x01
CHANNELS = {"MIC1": 0x4000, "MIC2": 0x5000, "MIC3": 0x6000}
BASE_CONFIG = 0x8483
sample_rate = 44100  

def read_adc(channel):
    config = BASE_CONFIG | CHANNELS[channel]
    bus.write_word_data(ADS1115_ADDR, CONFIG_REG, (config >> 8) | ((config & 0xFF) << 8))
    time.sleep(0.001)  
    data = bus.read_word_data(ADS1115_ADDR, CONVERSION_REG)
    value = ((data & 0xFF) << 8) | (data >> 8)  
    if value > 32767:  # Convert to signed 16-bit
        value -= 65536
    return value  

samples_mic1, samples_mic2, samples_mic3 = [], [], []

print("Recording... Press Ctrl + C to stop.")
try:
    while True:
        samples_mic1.append(read_adc("MIC1"))
        samples_mic2.append(read_adc("MIC2"))
        samples_mic3.append(read_adc("MIC3"))
except KeyboardInterrupt:
    print("\nRecording stopped. Saving audio...")

    # Convert list to numpy array and normalize
    audio_data = np.column_stack((samples_mic1, samples_mic2, samples_mic3))
    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)  # Normalize to PCM 16-bit

    write("multi_mic_audio.wav", sample_rate, audio_data)
    print("Audio saved as multi_mic_audio.wav")
