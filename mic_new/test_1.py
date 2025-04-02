import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize ADS1115
ADS1115 = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1

# Create figure for plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
xs = deque(maxlen=100)  # x points (time)
ys = deque(maxlen=100)  # y points (analog readings)
line, = ax.plot([], [], lw=2)

# Initialize plot data
for i in range(100):
    xs.append(i)
    ys.append(0)

# Set up plot parameters
ax.set_ylim(0, 32768)  # ADS1115 range (16-bit ADC)
ax.set_xlim(0, 100)
ax.set_title('MAX9814 Microphone Real-time Data')
ax.set_xlabel('Samples')
ax.set_ylabel('Analog Reading')
ax.grid(True)

# Function to update the plot
def update_plot(frame):
    analog = ADS1115.read_adc(0, gain=GAIN)
    ys.append(analog)
    line.set_data(range(len(ys)), ys)
    return line,

print('MAX9814 Microphone Module with Live Plot')
print('[Press CTRL + C to end the script!]')

try:
    # Set up animation
    ani = animation.FuncAnimation(
        fig, update_plot, interval=2, blit=True)
    plt.show()
    
except KeyboardInterrupt:
    print('\nScript end!')
finally:
    GPIO.cleanup()
    plt.close('all')
