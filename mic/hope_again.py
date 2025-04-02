import time   # Used for sleep function
import sys    # Used for print function
import smbus  # I2C

################################################################################
# Variables

bus = smbus.SMBus(1)  # The 1 means use port I2C1

# Address for the device 
addr = 0x48  # ADDR tied to GND

# Registers in the ADS1115
DEVICE_REG_CONVERSION = 0x00
DEVICE_REG_CONFIG = 0x01

# Configuration register fields
CONFIG_OS = 0X8000
CONFIG_OS_START = 0X8000
CONFIG_OS_PERFORMING_CONVERSION = 0X0000
CONFIG_MUX_AIN0P_GNDN = 0X4000 
CONFIG_MODE_SINGLE_SHOT = 0X0100
CONFIG_FSR_4V096 = 0X0200
CONFIG_DATA_RATE_128SPS = 0X0080
CONFIG_COMP_MODE_TRADITIONAL = 0X0000
CONFIG_COMP_POL_ACTIVE_LOW = 0X0000
CONFIG_COMP_LAT_NON_LATCHING = 0X0000
CONFIG_COMP_QUE_DISABLE = 0X0003

################################################################################
# Functions

def swap(a):
    return ((a & 0xff00) >> 8) | ((a & 0x00ff) << 8)

def readAdc(channel):
    if channel not in range(4):
        return -1

    config = (
        CONFIG_OS_START +
        CONFIG_MUX_AIN0P_GNDN +
        (channel << 12) +
        CONFIG_FSR_4V096 +
        CONFIG_MODE_SINGLE_SHOT +
        CONFIG_DATA_RATE_128SPS +
        CONFIG_COMP_MODE_TRADITIONAL +
        CONFIG_COMP_POL_ACTIVE_LOW +
        CONFIG_COMP_LAT_NON_LATCHING +
        CONFIG_COMP_QUE_DISABLE
    )
    
    bus.write_word_data(addr, DEVICE_REG_CONFIG, swap(config))
    
    while True:
        status = swap(bus.read_word_data(addr, DEVICE_REG_CONFIG))
        if (status & CONFIG_OS) != CONFIG_OS_PERFORMING_CONVERSION:
            break
    
    result = swap(bus.read_word_data(addr, DEVICE_REG_CONVERSION))
    return result

if __name__ == '__main__':
    print("==========================================================")
    print("Raspberry Pi 3 B")
    print("ADS1115 4-channel 16-bit I2C A2D converter demo")
    print("Updated for Python 3")
    print("==========================================================")
    time.sleep(3)
    
    try:
        while True:
            s = "(Ctrl-C to exit) ADC Result: "
            for i in range(4):
                val = readAdc(i)
                s += f"{i}: {val:05d}  "
            print(s)
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.exit(0)
