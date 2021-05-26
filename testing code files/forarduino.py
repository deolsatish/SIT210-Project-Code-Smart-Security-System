from smbus import SMBus
import time

addr=0x8
bus=SMBus(1) #/dev/ic2-1
#bus.write_byte(addr,0x0)
#bus.write_byte(addr,0x1)
def LIGHT(): # swicthing the light on using arduino
    bus.write_byte(addr,0x1)
    time.sleep(2);
    bus.write_byte(addr,0x0)        
    number = bus.read_byte(addr);
    
LIGHT()