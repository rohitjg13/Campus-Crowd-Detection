import time
import smbus
import wave
import numpy as np

bus = smbus.SMBus(1)
ADDR = 0x48  
DEVICE_REG_CONFIG = 0x01
DEVICE_REG_CONVERSION = 0x00

CONFIG_OS_START = 0x8000
CONFIG_MUX_AIN0P_GNDN = 0x4000
CONFIG_FSR_4V096 = 0x0200
CONFIG_MODE_SINGLE_SHOT = 0x0100
CONFIG_DATA_RATE_1600SPS = 0x0080
CONFIG_COMP_QUE_DISABLE = 0x0003

def read_adc():
    config = (CONFIG_OS_START | CONFIG_MUX_AIN0P_GNDN | CONFIG_FSR_4V096 |
              CONFIG_MODE_SINGLE_SHOT | CONFIG_DATA_RATE_1600SPS | CONFIG_COMP_QUE_DISABLE)
    bus.write_word_data(ADDR, DEVICE_REG_CONFIG, ((config >> 8) & 0xFF) | ((config & 0xFF) << 8))
    time.sleep(1 / 1600.0)  
    result = bus.read_word_data(ADDR, DEVICE_REG_CONVERSION)
    return ((result & 0xFF) << 8) | ((result >> 8) & 0xFF)

# Recording Parameters
sample_rate = 16000  
audio_data = []

print("Recording... Press Ctrl+C to stop.")
try:
    while True:
        audio_data.append(read_adc())

except KeyboardInterrupt:
    print("\nRecording stopped. Saving file...")

    # Convert to NumPy array (16-bit PCM)
    audio_data = np.array(audio_data, dtype=np.int16)

    # Save as WAV file
    wav_file = "recorded_audio.wav"
    with wave.open(wav_file, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"WAV file saved as {wav_file}")
