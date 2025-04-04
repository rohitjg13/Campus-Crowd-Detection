import time
import cv_annotation
import extract_mfcc

while True:
    min_crowd = 0
    max_crowd = 20
    p = (cv_annotation.process() - min_crowd) / (max_crowd - min_crowd)
    extract_mfcc.data(p)
    time.sleep(5)