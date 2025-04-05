from datetime import datetime
import librosa
import pandas as pd
from os import system


DURATION = 5
SAMPLERATE = 5885
N_MFCC = 13
FRAME_LENGTH = 0.025
HOP_LENGTH = 0.010


def load_audio(file_path, duration, sr=SAMPLERATE):
    y, sr = librosa.load(file_path, sr=sr, duration=duration)
    return y, sr


def extract_mfcc(audio, samplerate, n_mfcc=13):
    mfccs = librosa.feature.mfcc(
        y=audio,
        sr=samplerate,
        n_mfcc=n_mfcc,
        n_fft=int(FRAME_LENGTH * samplerate),
        hop_length=int(HOP_LENGTH * samplerate),
    )
    return mfccs.T


def save_mfcc_to_csv(
    time, mfcc_data, location_id, crowd_density=0.5, filename="mfcc_dataset.csv"
):
    num_frames, num_coeffs = mfcc_data.shape
    mfcc_flattened = mfcc_data.flatten().tolist()
    current_time = time

    headers = ["Date", "Day", "Time", "Location_ID", "Crowd_Density"]
    for frame in range(num_frames):
        for coef in range(num_coeffs):
            headers.append(f"MFCC_{frame+1}_{coef+1}")

    date_str = datetime.now().strftime("%Y-%m-%d")
    day_of_week = datetime.now().strftime("%A")
    row = [
        date_str,
        day_of_week,
        current_time,
        location_id,
        crowd_density,
    ] + mfcc_flattened

    file_exists = False
    try:
        with open(filename, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, "a", newline="") as csvfile:
        writer = pd.DataFrame([row], columns=headers)
        if file_exists:
            try:
                pd.read_csv(filename)
            except:
                backup_exists = False
                try:
                    with open("backup_mfcc_dataset.csv"):
                        backup_exists = True
                except FileNotFoundError:
                    pass
                if backup_exists:
                    system("cp backup_mfcc_dataset.csv mfcc_dataset.csv")
                else:
                    system("rm mfcc_dataset.csv")
                    file_exists = False
        writer.to_csv(csvfile, header=not file_exists, index=False)

    print(f"MFCC data saved to {filename}")


def data(inp, mfcc_data):
    location_ids = ["location_1", "location_2", "location_3"]
    start_time = datetime.strptime("09:00", "%H:%M")
    for i in range(200):
        crowd_density = inp
        current_time = (start_time + pd.Timedelta(minutes=i * 5)).strftime("%I:%M %p")
        print(f"Current time: {current_time}, Crowd Density: {crowd_density}")
        for location_id in location_ids:
            save_mfcc_to_csv(
                current_time,
                mfcc_data,
                location_id,
                crowd_density,
            )
