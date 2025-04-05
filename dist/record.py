from mfcc import SAMPLERATE, DURATION
import serial
import struct
import time
import wave


def record_from_mic(mic_number):
    """
    Record audio from a specific microphone for a set duration

    Args:
        mic_number: Which microphone to record from (1, 2, or 3)
        duration: Recording duration in seconds

    Returns:
        Filename of the saved recording
    """
    ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
    # Tell Arduino which mic to use
    ser.write(str(mic_number).encode())
    time.sleep(0.1)  # Small delay to ensure command is received

    # Generate filename with timestamp and mic number
    filename = f"/tmp/ccd/mic{mic_number}_recording.wav"

    # Setup WAV file
    wav_file = wave.open(filename, "wb")
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit PCM
    wav_file.setframerate(SAMPLERATE)  # Sample rate

    print(f"🎙️ Recording from Mic {mic_number} for {DURATION} seconds...")

    # Calculate end time
    end_time = time.time() + DURATION

    # Record until duration is reached
    while time.time() < end_time:
        low_byte = ser.read(1)
        high_byte = ser.read(1)
        if low_byte and high_byte:
            sample = struct.unpack("<H", low_byte + high_byte)[0]
            # Convert 10-bit (0-1023) to 16-bit (-32768 to 32767)
            sample = int((sample - 512) * 32)
            try:
                wav_file.writeframes(struct.pack("<h", sample))
            except:
                pass

    # Close the WAV file
    wav_file.close()
    print(f"✅ Saved recording as '{filename}'")
    return filename


def record_to_wav():
    ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
    try:
        # Record from each microphone sequentially
        print("Starting sequential recording from all microphones...")

        # Record from microphone 1
        file1 = record_from_mic(1)

        # Record from microphone 2
        file2 = record_from_mic(2)

        # Record from microphone 3
        file3 = record_from_mic(3)

        print("\n🎉 All recordings completed!")
        print(f"Microphone 1: {file1}")
        print(f"Microphone 2: {file2}")
        print(f"Microphone 3: {file3}")

    except KeyboardInterrupt:
        print("\n⚠️ Recording interrupted")

    finally:
        # Close serial connection
        ser.close()
        print("Serial connection closed")
