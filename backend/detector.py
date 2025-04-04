import time
import cv_annotation
import extract_mfcc

while True:
    p = 1 if cv_annotation.process() > 20 else 0
    extract_mfcc.data(p)
    time.sleep(5)