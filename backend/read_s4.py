import serial
import wave
import struct
import time
import threading

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

# Generate a unique filename using timestamp
filename = f"mic_recording_{int(time.time())}.wav"
wav_file = wave.open(filename, "wb")
wav_file.setnchannels(1)  # Mono
wav_file.setsampwidth(2)  # 16-bit PCM
wav_file.setframerate(5885)  # Sample rate

current_mic = 1
running = True

# Send initial microphone selection
ser.write(str(current_mic).encode())

def input_thread():
    global current_mic, running
    print(f"🎙️ Recording from Mic {current_mic}... Saving to {filename}.")
    print("Enter 1, 2, or 3 to switch microphones. Press q to quit.")
    
    while running:
        cmd = input()
        if cmd in ['1', '2', '3']:
            current_mic = int(cmd)
            ser.write(cmd.encode())
            print(f"Switched to Mic {current_mic}")
        elif cmd.lower() == 'q':
            running = False
            print("Stopping recording...")

# Start input thread
threading.Thread(target=input_thread, daemon=True).start()

try:
    while running:
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
    running = False

print(f"\n📁 Saved as '{filename}'")
wav_file.close()
ser.close()
