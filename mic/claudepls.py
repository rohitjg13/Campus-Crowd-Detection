import smbus
import time
import struct
import wave
import numpy as np

# ADS1115 constants
ADS1115_ADDRESS = 0x48
ADS1115_CONVERSION_REGISTER = 0x00
ADS1115_CONFIG_REGISTER = 0x01

# Config register values
# Bit 15: Start a single conversion (1)
# Bits 14-12: Input multiplexer, AIN0 to GND (100)
# Bits 11-9: Gain amplifier, +/-4.096V (001)
# Bit 8: Single shot mode (1)
# Bits 7-5: Data rate, 860 SPS (111)
# Bit 4: Traditional comparator (0)
# Bit 3: Active low comparator polarity (0)
# Bit 2: Non-latching comparator (0)
# Bits 1-0: Disable comparator (11)
CONFIG_VALUE = 0x8593

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use 1 for newer Raspberry Pi, 0 for older ones

def read_ads1115():
    """
    Read voltage from ADS1115 on channel 0
    Returns voltage in volts
    """
    # Write config value to start conversion
    bus.write_word_data(ADS1115_ADDRESS, ADS1115_CONFIG_REGISTER, CONFIG_VALUE)
    
    # Wait for conversion to complete
    time.sleep(0.001)
    
    # Read the conversion result
    result = bus.read_word_data(ADS1115_ADDRESS, ADS1115_CONVERSION_REGISTER)
    
    # Convert the result
    # ADS1115 sends the data in big-endian but smbus expects little-endian
    result = ((result & 0xFF) << 8) | (result >> 8)
    
    # Convert to voltage (with gain of 1, full range is +/-4.096V)
    if result > 0x7FFF:
        result = result - 0x10000
    voltage = result * 4.096 / 32768
    
    return voltage

def record_audio(duration=10, sample_rate=860):
    """
    Record audio for specified duration at given sample rate
    Returns samples as numpy array normalized to 16-bit range
    """
    samples = []
    num_samples = int(duration * sample_rate)
    
    print(f"Recording {duration} seconds of audio at {sample_rate} Hz...")
    start_time = time.time()
    
    for i in range(num_samples):
        if i % sample_rate == 0:
            seconds_elapsed = i // sample_rate
            print(f"{seconds_elapsed} seconds elapsed...")
        
        # Read voltage and store
        voltage = read_ads1115()
        samples.append(voltage)
        
        # Wait until next sample time
        next_sample_time = start_time + (i + 1) / sample_rate
        while time.time() < next_sample_time:
            pass
    
    print("Recording complete!")
    
    # Convert to numpy array for easy manipulation
    samples = np.array(samples)
    
    # Normalize to 16-bit range (-32768 to 32767)
    # First center around 0 by removing mean
    samples = samples - np.mean(samples)
    # Scale to use full 16-bit range, if there's any variation in the signal
    if np.max(samples) - np.min(samples) > 0:
        samples = samples / np.max(np.abs(samples)) * 32767
    
    return samples.astype(np.int16)

def save_to_wav(samples, filename="audio_recording.wav", sample_rate=860):
    """
    Save samples to WAV file
    """
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())
    print(f"Audio saved to {filename}")

# Main function
if __name__ == "__main__":
    # Record audio
    sample_rate = 400  # Maximum sample rate for ADS1115
    duration = 10  # 10 seconds as requested
    
    samples = record_audio(duration, sample_rate)
    
    # Save to WAV file
    save_to_wav(samples, "max9814_recording.wav", sample_rate)
    
    # Print some statistics
    print(f"Recorded {len(samples)} samples")
    print(f"Min value: {np.min(samples)}")
    print(f"Max value: {np.max(samples)}")
