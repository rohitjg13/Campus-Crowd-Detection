import serial
import wave
import struct

ser = serial.Serial("/dev/cu.usbserial-10", 115200, timeout=1)
wav_file = wave.open("recorded_audio.wav", "wb")
wav_file.setnchannels(1)  # Mono
wav_file.setsampwidth(2)  # 16-bit PCM
wav_file.setframerate(8000)  # Ensure playback at 8kHz

print("🎙️ Recording... Press Ctrl+C to stop.")

try:
    while True:
        low_byte = ser.read(1)
        high_byte = ser.read(1)
        if low_byte and high_byte:
            sample = struct.unpack('<H', low_byte + high_byte)[0]

            # Convert 10-bit (0-1023) to 16-bit (-32768 to 32767)
            sample = int((sample - 512) * 32)

            wav_file.writeframes(struct.pack('<h', sample))

except KeyboardInterrupt:
    print("\n📁 Saved as 'recorded_audio.wav'")
    wav_file.close()
    ser.close()