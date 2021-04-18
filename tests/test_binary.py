from rec_binary import RECBinaryStatusMonitor
import time

try:
    bsm = BinaryMonitor()
    header = '{0: >3s} {1: >3s} {2: >4s} {3: >3s}'.format(
        ' IR', ' CE', 'SYS+', 'CNT')
    print(header)
    while True:
        state = '{0: >3d} {1: >3d} {2: >4d} {3: >3d}'.format(
            bsm.internalRelay, bsm.chargeEnable, bsm.sysPlus, bsm.contactor)
        
        print(state)
        print(header, end="\r")
        time.sleep(1)
except KeyboardInterrupt:
    print("keyboard interrupt")
