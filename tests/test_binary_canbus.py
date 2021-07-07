from context import CanBusMonitor, BinaryMonitor
from time import sleep
import os
from instrument_logger import InstrumentLogger

os.system("sudo rm *.csv")
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")



try:         
    csm = CanBusMonitor('can0', 250000)
    bsm = BinaryMonitor()
    logger = InstrumentLogger()
    logger.filenameprefix = 'testing'
    logger.addinstrument(bsm)
    logger.addinstrument(csm)
    csm.start()
    sleep(3)
    logger.start()
    sleep(60)
    logger.stop()
    csm.stop()

    os.system("sudo /sbin/ip link set can0 down")
            
except KeyboardInterrupt:
    print("closing can connection")
    csm.stop()
    os.system("sudo /sbin/ip link set can0 down")