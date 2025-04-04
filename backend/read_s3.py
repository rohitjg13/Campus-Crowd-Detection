import serial
import wave
import struct
import time

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
timestamp = int(time.time())

# Create three WAV files, one for each microphone
filenames = [f"mic1_{timestamp}.wav", f"mic2_{timestamp}.wav", f"mic3_{timestamp}.wav"]
wav_files = []

for filename in filenames:
    wav_file = wave.open(filename, "wb")
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit PCM
    wav_file.setframerate(8000)  # 8kHz sample rate
    wav_files.append(wav_file)

print(f"🎙️ Recording... Saving to {', '.join(filenames)}. Press Ctrl+C to stop.")

try:
    while True:
        # Read 6 bytes (2 bytes per microphone)
        data = ser.read(6)
        
        if len(data) == 6:
            # Process each microphone's data
            for i in range(3):
                low_byte = data[i*2]
                high_byte = data[i*2+1]
                
                sample = struct.unpack('<H', bytes([low_byte, high_byte]))[0]
                # Convert 10-bit (0-1023) to 16-bit (-32768 to 32767)
                sample = int((sample - 512) * 32)
                
                try:
                    wav_files[i].writeframes(struct.pack('<h', sample))
                except:
                    pass
                    
except KeyboardInterrupt:
    print(f"\n📁 Recording stopped. Files saved.")
    for wav_file in wav_files:
        wav_file.close()
    ser.close()
