from os import system
from cv import *
from mfcc import load_audio, extract_mfcc, data, DURATION
from record import record_to_wav

MIN_CROWD = 0
MAX_CROWD = 20


def main():
    record_to_wav()
    for i in range(1, 4):
        AUDIO_FILE = f"mic{i}_recording.wav"
        audio_data, sr = load_audio(AUDIO_FILE, DURATION)
        mfcc_data = extract_mfcc(audio_data, sr)
        data((capture_cv_crowd() - MIN_CROWD) / (MAX_CROWD - MIN_CROWD), mfcc_data)


if __name__ == "__main__":
    system("mkdir /tmp/ccd")
    main()
    system("rm -rf /tmp/ccd")
