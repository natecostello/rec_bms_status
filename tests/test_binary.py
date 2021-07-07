from context import BinaryMonitor
from time import sleep
from instrument_logger import InstrumentLogger

try:
    bsm = BinaryMonitor()
    # header = '{0: >3s} {1: >3s} {2: >4s} {3: >3s}'.format(
    #     ' IR', ' CE', 'SYS+', 'CNT')
    # print(header)
    # while True:
    #     state = '{0: >3d} {1: >3d} {2: >4d} {3: >3d}'.format(
    #         bsm.internalRelay, bsm.chargeEnable, bsm.sysPlus, bsm.contactor)
        
    #     print(state)
    #     print(header, end="\r")
    #     time.sleep(1)
    logger = InstrumentLogger()
    logger.addinstrument(bsm)
    # csm.start()
    sleep(3)

    logger.start()
    sleep(10)
    logger.stop()

except KeyboardInterrupt:
    print("keyboard interrupt")
