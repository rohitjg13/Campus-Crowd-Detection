import librosa
import numpy as np
from datetime import datetime

AUDIO_FILE = "test_audio/output.wav" 
DURATION = 2  # 2 seconds to read
SAMPLERATE = 16000  # 16 kHz
N_MFCC = 13  # 13 MFCCs per frame
FRAME_LENGTH = 0.025  # 25ms frame size
HOP_LENGTH = 0.010  # 10ms hop length

def load_audio(file_path, duration, sr=SAMPLERATE):
    y, sr = librosa.load(file_path, sr=sr, duration=duration)
    return y, sr

def extract_mfcc(audio, samplerate, n_mfcc=13):
    mfccs = librosa.feature.mfcc(y=audio, sr=samplerate, n_mfcc=n_mfcc,
                                 n_fft=int(FRAME_LENGTH * samplerate),
                                 hop_length=int(HOP_LENGTH * samplerate))
    return mfccs.T

def save_mfcc_to_txt(mfcc_data, filename="mfcc_raw_data.txt"):
    """Save the MFCC data to a text file for inspection"""
    with open(filename, 'w') as f:
        f.write(f"MFCC Shape: {mfcc_data.shape}\n\n")
        f.write("MFCC Data (each row is a frame, each column is a coefficient):\n")
        np.savetxt(f, mfcc_data, fmt='%.6f', delimiter=',')
    print(f"Raw MFCC data saved to {filename}")

audio_data, sr = load_audio(AUDIO_FILE, DURATION)
mfcc_data = extract_mfcc(audio_data, sr)

save_mfcc_to_txt(mfcc_data)

num_frames, num_coeffs = mfcc_data.shape
print(f"MFCC shape: {mfcc_data.shape} (frames × coefficients)")

mfcc_flattened = mfcc_data.flatten().tolist()

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
day_of_week = now.strftime("%A")
current_time = now.strftime("%I:%M %p")