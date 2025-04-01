import librosa
import numpy as np
import pandas as pd
from datetime import datetime

AUDIO_FILE = "backend/test_audio/input.wav"
DURATION = 2
SAMPLERATE = 16000
N_MFCC = 13
FRAME_LENGTH = 0.025
HOP_LENGTH = 0.010

def load_audio(file_path, duration, sr=SAMPLERATE):
    y, sr = librosa.load(file_path, sr=sr, duration=duration)
    return y, sr

def extract_mfcc(audio, samplerate, n_mfcc=13):
    mfccs = librosa.feature.mfcc(y=audio, sr=samplerate, n_mfcc=n_mfcc,
                                 n_fft=int(FRAME_LENGTH * samplerate),
                                 hop_length=int(HOP_LENGTH * samplerate))
    return mfccs.T

def save_mfcc_to_csv(mfcc_data, location_id, filename="mfcc_dataset.csv"):
    num_frames, num_coeffs = mfcc_data.shape
    mfcc_flattened = mfcc_data.flatten().tolist()
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    day_of_week = now.strftime("%A")
    current_time = now.strftime("%I:%M %p")
    
    headers = ["Date", "Day", "Time", "Location_ID"]
    for frame in range(num_frames):
        for coef in range(num_coeffs):
            headers.append(f"MFCC_{frame+1}_{coef+1}")
    headers.append("Crowd_Density")
    
    crowd_density = 0.5  # Replace with actual measurement
    
    row = [date_str, day_of_week, current_time, location_id] + mfcc_flattened + [crowd_density]
    
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, 'a', newline='') as csvfile:
        writer = pd.DataFrame([row], columns=headers)
        writer.to_csv(csvfile, header=not file_exists, index=False)
    
    print(f"MFCC data saved to {filename}")

audio_data, sr = load_audio(AUDIO_FILE, DURATION)
mfcc_data = extract_mfcc(audio_data, sr)

location_id = "location_1"  # Replace with actual location identifier
save_mfcc_to_csv(mfcc_data, location_id)

print(f"MFCC shape: {mfcc_data.shape}")