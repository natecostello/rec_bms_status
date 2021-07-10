from context import CanBusMonitor, BinaryMonitor
from time import sleep
import os
from instrument_logger import InstrumentLogger
import can
from can.notifier import Notifier


os.system("sudo rm *.csv")
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")


try:
    print("initializing insturments and logger")
    csm = CanBusMonitor()
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)         
    notifier = Notifier(bus, [csm])

    bsm = BinaryMonitor()
    
    logger = InstrumentLogger()
    logger.filenameprefix = 'testing'
    logger.addinstrument(bsm)
    logger.addinstrument(csm)
    
    print("logging for 60 seconds")
    sleep(3)
    logger.start()
    sleep(60)
    logger.stop()

    print("closing can connection")
    notifier.stop()
    bus.shutdown()
    os.system("sudo /sbin/ip link set can0 down")
            
except KeyboardInterrupt:
    print("closing can connection due to keyboard interrupt")
    notifier.stop()
    bus.shutdown()
    os.system("sudo /sbin/ip link set can0 down")