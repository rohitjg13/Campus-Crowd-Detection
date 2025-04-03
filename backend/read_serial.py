import serial
import wave
import struct
import time

SERIAL_PORT = "/dev/cu.usbserial-10"
BAUD_RATE = 115200
SAMPLE_RATE = 8000

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

wav_file = wave.open("recorded_audio.wav", "wb")
wav_file.setnchannels(1)  # Mono
wav_file.setsampwidth(2)  # 16-bit audio
wav_file.setframerate(SAMPLE_RATE)

print("🎤 Recording... Press CTRL+C to stop.")

try:
    while True:
        # Read 2 bytes (16-bit ADC)
        low_byte = ser.read(1)
        high_byte = ser.read(1)
        if low_byte and high_byte:
            sample = struct.unpack('<H', low_byte + high_byte)[0]
            sample = sample - 512  # Normalize to center
            wav_file.writeframes(struct.pack('<h', sample))

except KeyboardInterrupt:
    print("\n📁 Recording saved as 'recorded_audio.wav'")
    wav_file.close()
    ser.close()