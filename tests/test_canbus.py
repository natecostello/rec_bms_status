from context import CanBusMonitor
import time
import os

os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")

try:         
    csm = CanBusMonitor('can0', 250000)
    csm.start()

    while True:
        print(csm.charge_current_limit)
        print(csm.min_cell_voltage)
        print(csm.alarmBits)
        print(csm.warningBits)
        time.sleep(2)
        
except KeyboardInterrupt:
    print("closing can connection")
    csm.stop()
    os.system("sudo /sbin/ip link set can0 down")

