import time
import board
import busio
import numpy as np
import wave
import struct
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Parameters
SAMPLE_RATE = 3000  # Hz - adjust based on your needs
DURATION = 3  # seconds
NUM_SAMPLES = SAMPLE_RATE * DURATION
CHANNELS = 3  # Number of microphones

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
# Using ADS1115 for higher resolution (16-bit) compared to ADS1015 (12-bit)
ads = ADS.ADS1115(i2c)

# Set the gain - adjust based on your microphone output range
# Options: 2/3, 1, 2, 4, 8, 16
ads.gain = 1

# Create analog inputs for the three microphones
mic1 = AnalogIn(ads, ADS.P0)
mic2 = AnalogIn(ads, ADS.P1)
mic3 = AnalogIn(ads, ADS.P2)

# Create arrays to store the samples
data = np.zeros((CHANNELS, NUM_SAMPLES), dtype=np.int16)

# Set the data rate (samples per second)
# ADS1115 supports up to ~860 SPS max
ads.data_rate = 860

print(f"Recording for {DURATION} seconds...")
print(f"Target sample rate: {SAMPLE_RATE} Hz")

# Calculate delay between samples to achieve target sample rate
# Note: Due to overhead, actual rate may be lower
delay = 1.0 / SAMPLE_RATE

start_time = time.monotonic()
for i in range(NUM_SAMPLES):
    # Read from each microphone and convert voltage to 16-bit PCM
    # Scale factor converts voltage (typically 0-3.3V) to 16-bit range (-32768 to 32767)
    scale_factor = 32767 / 3.3  # Adjust if your reference voltage is different

    # Read and scale each microphone value
    data[0, i] = int((mic1.voltage - 1.65) * scale_factor)  # Offset by 1.65V (half of 3.3V) to center at 0
    data[1, i] = int((mic2.voltage - 1.65) * scale_factor)
    data[2, i] = int((mic3.voltage - 1.65) * scale_factor)

    # Wait for next sample time
    next_sample_time = start_time + ((i + 1) * delay)
    current_time = time.monotonic()
    if current_time < next_sample_time:
        time.sleep(next_sample_time - current_time)

# Calculate actual sample rate achieved
actual_duration = time.monotonic() - start_time
actual_sample_rate = NUM_SAMPLES / actual_duration
print(f"Recording complete!")
print(f"Actual sample rate: {actual_sample_rate:.2f} Hz")
print(f"Actual duration: {actual_duration:.2f} seconds")

# Save to WAV file
filename = "microphone_recording.wav"
with wave.open(filename, 'w') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 2 bytes for 16-bit samples
    wf.setframerate(int(actual_sample_rate))

    # Interleave the channels
    interleaved = np.empty(CHANNELS * NUM_SAMPLES, dtype=np.int16)
    for i in range(CHANNELS):
        interleaved[i::CHANNELS] = data[i]

    # Write the interleaved data
    wf.writeframes(interleaved.tobytes())

print(f"Recording saved to {filename}")