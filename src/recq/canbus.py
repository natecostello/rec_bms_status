import can
import time
import queue
from threading import Thread

# For documentation of IDs see http://www.rec-bms.com/datasheet/UserManual9R_SMA.pdf
CHARGE_DISCHARGE_LIMITS_ID =        0x351
SOC_SOH_ID =                        0x355
BATTERY_VOLT_CURRENT_TEMP_ID =      0x356
ALARM_WARNING_ID =                  0x35A
MANUFACTURER_ID =                   0x35E
CHEM_HWVERS_CAPACITY_SWVERS_ID =    0x35F
# Unknown =                         0x370
MIN_MAX_CELL_VOLT_TEMP_ID =         0x373
# Unknown =                         0x374
# Unknown =                         0x375
# Unknown =                         0x376
# Unknown =                         0x377
RATED_CAPACITY =                    0x379
# Unknown =                         0x380

class CanBusMonitor:

    def __init__(self, interface='can0', bitrate=250000):
        self.canInterface = interface
        self.bitrate = bitrate

        self.charge_voltage_limit = 0
        self.charge_current_limit = 0
        self.discharge_current_limit = 0
        self.discharge_voltage_limit = 0
        self.state_of_charge = 0
        self.state_of_health = 0
        self.state_of_charge_hi_res = 0
        self.battery_voltage = 0
        self.battery_current = 0
        self.battery_temperature = 0
        self.min_cell_voltage = 0
        self.max_cell_voltage = 0
        self.min_temperature = 0
        self.max_temperature = 0
        self.rated_capacity = 0
        self.remaining_capacity = 0
        self.warningBytes = 0
        self.alarmBytes = 0
        self.warningBits = ''
        self.alarmBits = ''

    def can_rx_task(self):
        while True:
            message = self.bus.recv()
            self.translateMessageAndUpdate(message)


    def translateMessageAndUpdate(self, message):
        if message.arbitration_id == CHARGE_DISCHARGE_LIMITS_ID:
            self.charge_voltage_limit = 0.1 * int.from_bytes(message.data[0:2], 'little')
            self.charge_current_limit = 0.1 * int.from_bytes(message.data[2:4], 'little')
            self.discharge_current_limit = 0.1 * int.from_bytes(message.data[4:6], 'little')
            self.discharge_voltage_limit = 0.1 * int.from_bytes(message.data[6:8], 'little')
            
        if message.arbitration_id == SOC_SOH_ID:
            self.state_of_charge = int.from_bytes(message.data[0:2], 'little')
            self.state_of_health = int.from_bytes(message.data[2:4], 'little')
            self.state_of_charge_hi_res = 0.01 * int.from_bytes(message.data[4:6], 'little')
                
        if message.arbitration_id == BATTERY_VOLT_CURRENT_TEMP_ID:
            self.battery_voltage = 0.01 * int.from_bytes(message.data[0:2], 'little')
            self.battery_current = 0.1 * int.from_bytes(message.data[2:4], 'little')
            self.battery_temperature = 0.1 * int.from_bytes(message.data[4:6], 'little')
            
        if message.arbitration_id == MIN_MAX_CELL_VOLT_TEMP_ID:
            self.min_cell_voltage = 0.001 * int.from_bytes(message.data[0:2], 'little')
            self.max_cell_voltage = 0.001 * int.from_bytes(message.data[2:4], 'little')
            self.min_temperature = int.from_bytes(message.data[4:6], 'little')
            self.max_temperature = int.from_bytes(message.data[6:8], 'little')
            
        if message.arbitration_id == RATED_CAPACITY:
            self.rated_capacity = int.from_bytes(message.data[0:2], 'little')
            if self.rated_capacity > 250:
                self.rated_capacity += 1
            
        if message.arbitration_id == CHEM_HWVERS_CAPACITY_SWVERS_ID:
            self.remaining_capacity = int.from_bytes(message.data[4:6], 'little')

        if message.arbitration_id == ALARM_WARNING_ID:
            self.alarmBytes = message.data[0:4]
            bits = ''
            for byte in self.alarmBytes:
                bits += '{0:0>8b}'.format(byte) + ' '
            self.alarmBits = bits[:-1]

            self.warningBytes = message.data[4:8]
            bits = ''
            for byte in self.warningBytes:
                bits += '{0:0>8b}'.format(byte) + ' '
            self.warningBits = bits[:-1]

            
    def start(self):
        
        self.bus = can.interface.Bus(channel=self.canInterface, bustype='socketcan', bitrate=self.bitrate)

        rx = Thread(target = self.can_rx_task)

        
        rx.daemon=True
        rx.start()




    




