from context import CanBusMonitor
from time import sleep
import os
from instrument_logger import InstrumentLogger

os.system("sudo rm *.csv")
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")



try:         
    csm = CanBusMonitor('can0', 250000)
    logger = InstrumentLogger()
    logger.addinstrument(csm)
    csm.start()
    sleep(3)

    logger.start()
    sleep(10)
    logger.stop()
    os.system("sudo /sbin/ip link set can0 down")
            
except KeyboardInterrupt:
    print("closing can connection")
    csm.stop()
    os.system("sudo /sbin/ip link set can0 down")

