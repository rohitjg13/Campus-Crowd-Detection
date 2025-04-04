from os import system
from picamzero import Camera
from ultralytics import YOLO
import librosa
import numpy as np
import pandas as pd
from datetime import datetime
import random

model = YOLO("yolov8x.pt")
camera = Camera()
system("mkdir /tmp/cv")

def capture_cv_crowd():
    system("mkdir /tmp/cv")
    camera.take_photo("/tmp/cv/process.jpg")
    results = model.predict("/tmp/cv/process.jpg")
    system("rm /tmp/cv/process.jpg")
    result = results[0]
    probability_threshold = 0.75 # TODO: tweak probability threshold with representative images
    people = 0
    for box in result.boxes:
        if (box.cls[0] == 0 and box.conf[0] > probability_threshold):
            people += 1
    return people


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

def save_mfcc_to_csv(time ,mfcc_data, location_id, crowd_density=0.5, filename="mfcc_dataset.csv"):
    num_frames, num_coeffs = mfcc_data.shape
    mfcc_flattened = mfcc_data.flatten().tolist()
    current_time = time
    
    headers = ["Date", "Day", "Time", "Location_ID", "Crowd_Density"]
    for frame in range(num_frames):
        for coef in range(num_coeffs):
            headers.append(f"MFCC_{frame+1}_{coef+1}")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    day_of_week = datetime.now().strftime("%A")
    row = [date_str, day_of_week, current_time, location_id, crowd_density] + mfcc_flattened
    
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

location_ids = ["location_1", "location_2", "location_3"]
start_time = datetime.strptime("09:00", "%H:%M")

def data(inp):
    for i in range(200):
        crowd_density = inp
        current_time = (start_time + pd.Timedelta(minutes=i * 5)).strftime("%I:%M %p")
        print(f"Current time: {current_time}, Crowd Density: {crowd_density}")
        for location_id in location_ids:
            save_mfcc_to_csv(current_time, mfcc_data, location_id, crowd_density, filename="mfcc_dataset.csv")
if __name__ == "__main__":
    
