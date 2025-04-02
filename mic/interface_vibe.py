import struct
import time
import wave
import Adafruit_ADS1x15 as ADS
import board
import busio
import numpy as np
from smbus import SMBus  # For direct SMBus access

# Parameters
SAMPLE_RATE = 3000  # Hz - adjust based on your needs
DURATION = 3  # seconds
NUM_SAMPLES = SAMPLE_RATE * DURATION
CHANNELS = 3  # Number of microphones

# Create the ADC object using the I2C bus
# Using ADS1115 for higher resolution (16-bit) compared to ADS1015 (12-bit)
ads = ADS.ADS1115(busnum=1, address=0x48)  # Use your device's address (0x48-0x4B)

print(f"Recording for {DURATION} seconds...")
print(f"Target sample rate: {SAMPLE_RATE} Hz")

# Create arrays to store the samples
data = np.zeros((CHANNELS, NUM_SAMPLES), dtype=np.int16)

# Calculate delay between samples to achieve target sample rate
delay = 1.0 / SAMPLE_RATE
start_time = time.monotonic()

# Calculate voltage conversion factor
# ADS1115 with gain of 1 has a range of ±4.096V
# But most likely your microphones use a smaller range (0-3.3V typically)
full_scale_voltage = 4.096
scale_factor = 32767 / 3.3  # Scaling from typical 3.3V range to 16-bit signed int

for i in range(NUM_SAMPLES):
    # Read from each microphone and convert to voltage
    # For the older library, we need to use read_adc methods
    raw_value0 = ads.read_adc(0, gain=GAIN)  # Channel 0
    raw_value1 = ads.read_adc(1, gain=GAIN)  # Channel 1
    raw_value2 = ads.read_adc(2, gain=GAIN)  # Channel 2
    
    # Convert raw ADC values to voltage
    voltage0 = raw_value0 * (full_scale_voltage / 32767)
    voltage1 = raw_value1 * (full_scale_voltage / 32767)
    voltage2 = raw_value2 * (full_scale_voltage / 32767)
    
    # Scale and center around 0 for audio
    data[0, i] = int((voltage0 - 1.65) * scale_factor)
    data[1, i] = int((voltage1 - 1.65) * scale_factor)
    data[2, i] = int((voltage2 - 1.65) * scale_factor)
    
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
with wave.open(filename, "w") as wf:
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
