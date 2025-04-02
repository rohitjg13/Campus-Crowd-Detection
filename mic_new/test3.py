import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import numpy as np
import wave
import datetime
import os
import threading

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize ADS1115
ADS1115 = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1

# Audio recording parameters
SAMPLE_RATE = 500  # Sample rate in Hz
RECORDING_TIME = 5  # Recording time in seconds (EXACT)
RECORDING_FILE = f"recording1.wav"

# Global variables for recording
samples = []
is_recording = False

def sample_collector():
    """Thread function to collect samples as fast as possible"""
    global samples, is_recording
    
    start_time = time.time()
    while is_recording and (time.time() - start_time) < RECORDING_TIME:
        # Read the analog value and add to samples
        analog = ADS1115.read_adc(0, gain=GAIN)
        samples.append(analog)
        
        # Print progress indicator
        elapsed = time.time() - start_time
        if int(elapsed * 2) != int((elapsed - 0.1) * 2):  # Update roughly twice per second
            print(f"Recording: {elapsed:.1f}s / {RECORDING_TIME:.1f}s")

def record_audio():
    """Main recording function that guarantees exact duration"""
    global samples, is_recording
    
    # Reset samples list
    samples = []
    
    # Start recording
    print(f"Starting {RECORDING_TIME}-second recording...")
    is_recording = True
    
    # Start collector thread for sampling
    collector_thread = threading.Thread(target=sample_collector)
    collector_thread.start()
    
    # Wait for exactly RECORDING_TIME seconds
    start_time = time.time()
    time.sleep(RECORDING_TIME)
    
    # Stop recording
    is_recording = False
    collector_thread.join()
    
    # Calculate actual time and real sample rate
    actual_time = time.time() - start_time
    actual_sample_rate = len(samples) / actual_time
    
    print(f"Recording complete!")
    print(f"Collected {len(samples)} samples in {actual_time:.2f} seconds")
    print(f"Effective sample rate: {actual_sample_rate:.1f} Hz")
    
    return samples

def save_wav(samples, filename, sample_rate):
    # Convert to numpy array for processing
    samples_array = np.array(samples)
    
    # Center around zero by subtracting the mean
    samples_array = samples_array - np.mean(samples_array)
    
    # Normalize to 16-bit range (-32768 to 32767)
    if np.max(np.abs(samples_array)) > 0:
        samples_array = samples_array * 32767 / np.max(np.abs(samples_array))
    
    # Convert to 16-bit integers
    samples_array = samples_array.astype(np.int16)
    
    # Create WAV file with the actual sample rate
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes = 16 bits
        wf.setframerate(int(sample_rate))
        wf.writeframes(samples_array.tobytes())
    
    duration = len(samples_array) / sample_rate
    file_size = os.path.getsize(filename) / 1024
    print(f"Audio saved to {os.path.abspath(filename)}")
    print(f"Duration: {duration:.2f} seconds, Size: {file_size:.1f} KB")

try:
    print("=== ADS1115 Microphone Recording Tool ===")
    print(f"Target recording time: {RECORDING_TIME} seconds")
    print("Press Enter to start recording or Ctrl+C to quit")
    input()
    
    # Record audio
    audio_samples = record_audio()
    
    # Calculate actual sample rate
    actual_rate = len(audio_samples) / RECORDING_TIME
    
    # Save the WAV file with the actual sample rate
    save_wav(audio_samples, RECORDING_FILE, actual_rate)
    
except KeyboardInterrupt:
    print("\nRecording canceled!")
finally:
    is_recording = False
    GPIO.cleanup()
    print("GPIO cleaned up. Exiting.")
