import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import numpy as np
import wave
import datetime
import os

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize ADS1115
ADS1115 = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1

# Audio recording parameters
SAMPLE_RATE = 500  # Sample rate in Hz (reduced to match ADS1115 capabilities)
RECORDING_TIME = 5  # Recording time in seconds
RECORDING_FILE = f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

def record_audio():
    print(f"Recording {RECORDING_TIME} seconds of audio...")
    print("Please wait...")
    
    # Calculate total samples needed
    total_samples = RECORDING_TIME * SAMPLE_RATE
    samples = []
    
    # Record exact number of samples with precise timing
    start_time = time.time()
    for i in range(total_samples):
        # Read the analog value
        analog = ADS1115.read_adc(0, gain=GAIN)
        samples.append(analog)
        
        # Calculate next sample time
        next_sample_time = start_time + (i + 1) * (1.0 / SAMPLE_RATE)
        
        # Wait until next sample time
        current_time = time.time()
        if current_time < next_sample_time:
            time.sleep(next_sample_time - current_time)
        
        # Print progress every half second
        if i % (SAMPLE_RATE // 2) == 0:
            print(f"Recording: {i/SAMPLE_RATE:.1f}s / {RECORDING_TIME}s")
    
    # Calculate actual recording time
    actual_time = time.time() - start_time
    print(f"Recording complete! Collected {len(samples)} samples in {actual_time:.2f} seconds")
    
    return samples

def save_wav(samples, filename):
    # Convert to numpy array for processing
    samples_array = np.array(samples)
    
    # Center around zero by subtracting the mean
    samples_array = samples_array - np.mean(samples_array)
    
    # Normalize to 16-bit range (-32768 to 32767)
    if np.max(np.abs(samples_array)) > 0:
        samples_array = samples_array * 32767 / np.max(np.abs(samples_array))
    
    # Convert to 16-bit integers
    samples_array = samples_array.astype(np.int16)
    
    # Create WAV file
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes = 16 bits
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(samples_array.tobytes())
    
    file_size = os.path.getsize(filename) / 1024
    print(f"Audio saved to {os.path.abspath(filename)} ({file_size:.1f} KB)")

try:
    print("=== ADS1115 Microphone Recording Tool ===")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Recording time: {RECORDING_TIME} seconds")
    print("Press Enter to start recording or Ctrl+C to quit")
    input()
    
    # Record audio
    audio_samples = record_audio()
    
    # Save the WAV file
    save_wav(audio_samples, RECORDING_FILE)
    
except KeyboardInterrupt:
    print("\nRecording canceled!")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Exiting.")
