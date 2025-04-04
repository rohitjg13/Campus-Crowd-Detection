import serial
import wave
import struct
import time

# Open serial connection
ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

# Generate a unique filename using timestamp
filename = f"actual_hehe_{int(time.time())}.wav"

# Set up the WAV file
wav_file = wave.open(filename, "wb")
wav_file.setnchannels(1)  # Mono
wav_file.setsampwidth(2)  # 16-bit PCM
wav_file.setframerate(5885)  # 8kHz sample rate

# Recording duration in seconds
RECORD_DURATION = 5

print(f"🎙️ Recording for {RECORD_DURATION} seconds... Saving to {filename}.")

# Get the start time
start_time = time.time()
samples_recorded = 0

try:
    # Record until 5 seconds have passed
    while time.time() - start_time < RECORD_DURATION:
        low_byte = ser.read(1)
        high_byte = ser.read(1)
        
        if low_byte and high_byte:
            sample = struct.unpack('<H', low_byte + high_byte)[0]
            # Convert 10-bit (0-1023) to 16-bit (-32768 to 32767)
            sample = int((sample - 512) * 32)
            
            try:
                wav_file.writeframes(struct.pack('<h', sample))
                samples_recorded += 1
            except:
                pass
    
    # Calculate actual sample rate achieved
    actual_duration = time.time() - start_time
    actual_sample_rate = samples_recorded / actual_duration
    
    print(f"\n📁 Recording complete!")
    print(f"⏱️ Duration: {actual_duration:.2f} seconds")
    print(f"📊 Samples recorded: {samples_recorded}")
    print(f"📈 Actual sample rate: {actual_sample_rate:.2f} Hz")
    print(f"📁 Saved as '{filename}'")

except KeyboardInterrupt:
    # Allow manual interruption if needed
    print(f"\n⚠️ Recording interrupted!")

finally:
    # Always close files and connections properly
    wav_file.close()
    ser.close()
