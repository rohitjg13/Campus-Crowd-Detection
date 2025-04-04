import serial
import wave
import struct
import time  # Import time module

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

# Generate a unique filename using timestamp
filename = f"actual_hehe_{int(time.time())}.wav"
wav_file = wave.open(filename, "wb")

wav_file.setnchannels(1)  # Mono
wav_file.setsampwidth(2)  # 16-bit PCM
wav_file.setframerate(5885)  # 8kHz sample rate

print(f"🎙️ Recording... Saving to {filename}. Press Ctrl+C to stop.")

try:
    while True:
        low_byte = ser.read(1)
        high_byte = ser.read(1)
        if low_byte and high_byte:
            sample = struct.unpack('<H', low_byte + high_byte)[0]

            # Convert 10-bit (0-1023) to 16-bit (-32768 to 32767)
            sample = int((sample - 512) * 32)
            try:
                wav_file.writeframes(struct.pack('<h', sample))
            except:
                pass

except KeyboardInterrupt:
    print(f"\n📁 Saved as '{filename}'")
    wav_file.close()
    ser.close()
