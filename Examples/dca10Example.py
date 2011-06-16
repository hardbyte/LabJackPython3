"""
An example showing how to work with a DCA-10 Motor Controller. More info on the DCA-10 here:

http://labjack.com/support/dca-10/datasheet

See the dca10.py for more information on the DCA10 class.
"""
import dca10
from time import sleep
from time import time


r = input("Do you have an encoder to connect to the LabJack? [y/N] ")

ea = False
if r.lower().strip().startswith('y'):
    ea = True

print("Opening device, and configuring it for the DCA-10...", end=' ')
d = dca10.DCA10(encoderAttached = ea)
print("Done\n")

print("Before we begin, please insure that the DCA-10 is wired to the LabJack as follows:")
print(d.wiringDescription())

r = input("Press enter key when ready.")

print("Starting motor at 50%...", end=' ')
d.startMotor(0.50)
print("Done")

sleep(3)

print("Changing motor direction...", end=' ')
d.toggleDirection()
print("Done")

sleep(3)

print("Reading current usage...", end=' ')
usage = d.readCurrent()
print("Done")

print("The current drawn by the DCA-10 is %0.4f Amps" % usage)

sleep(3)

print("Increasing motor speed to 100%...", end=' ')
d.startMotor(1)
print("Done")

sleep(3)

if ea:
    print("Measuring RPM...", end=' ')
    a = int(time())
    s = d.readEncoder()
    sleep(2)
    f = d.readEncoder()
    b = int(time())
    
    cps = float(f-s)/float(b-a)
    cpm = cps * 60
    print("Done")
    
    print("Motor spinning at %s CPM (%s Counts Per Second)." % (cpm, cps))
    
    print("Decreasing motor speed to 50%...", end=' ')
    d.startMotor(0.50)
    print("Done")
    
    sleep(3)
    
    print("Measuring RPM...", end=' ')
    a = int(time())
    s = d.readEncoder()
    sleep(2)
    f = d.readEncoder()
    b = int(time())
    
    cps = float(f-s)/float(b-a)
    cpm = cps * 60
    print("Done")
    
    print("Motor spinning at %s CPM (%s Counts Per Second)." % (cpm, cps))
    
    sleep(3)

print("Stopping Motor...", end=' ')
d.stopMotor()
print("Done")

