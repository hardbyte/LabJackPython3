#!/usr/bin/env python3
'''

Hardware setup assumed for this test:
    One LED between FIO0 and GND
    Short circuit between DAC0 and AIN0

Based on http://labjack.com/support/labjackpython
http://labjack.com/support/u6

'''
import time
from pprint import pprint

from labjack import U6

DAC0_REGISTER = 5000
AIN0_REGISTER = 0
FIO0_STATE = 6000
FIO0_DIR = 6100

def say_hello(device):

    device.debug = False

    deviceconfig = device.configU6()

    print("{0[DeviceName]} Labjack found with serial number: {0[SerialNumber]}.".format(deviceconfig))

    ioconfig = device.configIO()
    pprint(ioconfig)

    v = 1.5
    print('Setting the voltage on DAC0 to {}V'.format(v))
    device.writeRegister(DAC0_REGISTER, v)
    ain0_result = device.readRegister(AIN0_REGISTER)
    print('Reading the voltage from AIN0: {}'.format(ain0_result))
    dac0_result = device.readRegister(DAC0_REGISTER)
    print('Reading the voltage from DAC0: {}'.format(dac0_result))
    print('Setting the voltage on DAC0 to 0V')
    device.writeRegister(DAC0_REGISTER, 0)
    ain0_result = device.readRegister(AIN0_REGISTER)
    print('Reading the voltage from AIN0: {}'.format(ain0_result))
    dac0_result = device.readRegister(DAC0_REGISTER)
    print('Reading the voltage from DAC0: {}'.format(dac0_result))



    print('Digital output on FIO0 to light the LED')
    device.writeRegister(FIO0_STATE, 1)
    time.sleep(2)
    device.writeRegister(FIO0_STATE, 0)

    # Digital input with FIO0
    print('FIO0 currently has dir={}, state={}'.format(
        device.readRegister(FIO0_DIR), device.readRegister(FIO0_STATE)))
    print('Set FIO0 to digital input')
    # Setting the direction seems broken?
    #device.writeRegister(FIO0_DIR, 0)
    # But even when not configured as an input we can read its state
    # Should be 0 if LED connected, otherwise 1
    print('The state of FIO0: {}'.format(device.readRegister(FIO0_STATE)))

    #device.writeRegister(FIO0_DIR, 1)

    print('Speed test. Sending a square signal on DAC0, and receiving on AIN0')

    voltage_data = []
    timing_data = []

    start, end = time.time(), 0

    while end - start < 2:
        begin = time.time()
        # Set the output to 1.5V
        device.writeRegister(DAC0_REGISTER, 1.5)

        voltage_data.append(device.readRegister(AIN0_REGISTER))
        
        # Set the output to 0V
        device.writeRegister(DAC0_REGISTER, 0)

        end = time.time()

        timing_data.append(end - begin)

    def avg(lst):
        return sum(lst)/len(lst)

    print('Done. Avg Voltage = {}. Avg Time = {}'.format(avg(voltage_data), avg(timing_data)))


if __name__ == "__main__":
    device = U6()
    try:
        say_hello(device) 
    finally:
        print('Closing device')
        device.close()

