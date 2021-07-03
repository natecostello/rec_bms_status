import can
from can.listener import Listener
from can.notifier import Notifier
from instrument_logger import Instrument

import time
import queue
from threading import Thread, setprofile

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

KELVN_TO_C = 273 # rounded

#TODO: Implement Instrument
#TODO: Add latest decyphering

class CanBusMonitor(Listener, Instrument):

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

    @property
    def name(self) -> str:
        """Required for Instrument"""
        return "rec-q-can"


    @property
    def allmeasurements(self) -> 'dict':
        """Required for Instrument"""
        all_meas = {}
        for param in self.parameters:
            all_meas[param] = self.getmeasurement(param)
        return all_meas
    
    @property
    def parameters(self) -> 'list[str]':
        """Required for Instrument"""
        return [
            self.name + '.CVL.V', 
            self.name + '.CCL.A', 
            self.name + '.DVL.V',
            self.name + '.DCL.A',
            self.name + '.SOC.%',
            self.name + '.SOH.%',
            self.name + '.SOC_HR.%',
            self.name + 'Battery Voltage.V',
            self.name + 'Battery Current.A',
            self.name + 'Battery Temp.C',
            self.name + 'Min Cell Voltage.V',
            self.name + 'Max Cell Voltage.V',
            self.name + 'Min Temperature.C',
            self.name + 'Max Temperature.C',
            self.name + 'Rated Capacity.AH',
            self.name + 'Remaining Capacity.AH',
            self.name + 'Warning Bits.binary',
            self.name + 'Alarm Bits.binary']
    
    def getmeasurement(self, name: str) -> str:
        """Required for Instrument"""
        if (name == self.name + '.CVL.V'):
            return str(self.charge_voltage_limit)
        if (name == self.name + '.CCL.A'):
            return str(self.charge_current_limit)
        if (name == self.name + '.DVL.V'):
            return str(self.discharge_voltage_limit)
        if (name == self.name + '.DCL.A'):
            return str(self.discharge_current_limit)
        if (name == self.name + '.SOC.%'):
            return str(self.state_of_charge)
        if (name == self.name + '.SOH.%'):
            return str(self.state_of_health)
        if (name == self.name + '.SOC_HR.%'):
            return str(self.state_of_charge_hi_res)
        if (name == self.name + 'Battery Voltage.V'):
            return str(self.battery_voltage)
        if (name == self.name + 'Battery Current.A'):
            return str(self.battery_current)
        if (name == self.name + 'Battery Temp.C'):
            return str(self.battery_temperature)
        if (name == self.name + 'Min Cell Voltage.V'):
            return str(self.min_cell_voltage)
        if (name == self.name + 'Max Cell Voltage.V'):
            return str(self.max_cell_voltage)
        if (name == self.name + 'Min Temperature.C'):
            return str(self.min_temperature)
        if (name == self.name + 'Max Temperature.C'):
            return str(self.max_temperature)
        if (name == self.name + 'Rated Capacity.AH'):
            return str(self.rated_capacity)
        if (name == self.name + 'Remaining Capacity.AH'):
            return str(self.remaining_capacity)
        if (name == self.name + 'Warning Bits.binary'):
            return str(self.warningBits)
        if (name == self.name + 'Alarm Bits.binary'):
            return str(self.alarmBits)


    def on_message_received(self, msg):
        """Requiremed method for Listener"""
        self.translateMessageAndUpdate(msg)

    def __call__(self, msg):
        """method for Listener"""
        self.on_message_received(msg)

    # def can_rx_task(self):
    #     while True:
    #         message = self.bus.recv()
    #         self.translateMessageAndUpdate(message)


    def translateMessageAndUpdate(self, message):
        if message.arbitration_id == CHARGE_DISCHARGE_LIMITS_ID:
            self.charge_voltage_limit = round(0.1 * int.from_bytes(message.data[0:2], 'little'), 1)
            self.charge_current_limit = round(0.1 * int.from_bytes(message.data[2:4], 'little'), 1)
            self.discharge_current_limit = round(0.1 * int.from_bytes(message.data[4:6], 'little'), 1)
            self.discharge_voltage_limit = round(0.1 * int.from_bytes(message.data[6:8], 'little'), 1)
            
        if message.arbitration_id == SOC_SOH_ID:
            self.state_of_charge = int.from_bytes(message.data[0:2], 'little')
            self.state_of_health = int.from_bytes(message.data[2:4], 'little')
            self.state_of_charge_hi_res = round(0.01 * int.from_bytes(message.data[4:6], 'little'), 2)
                
        if message.arbitration_id == BATTERY_VOLT_CURRENT_TEMP_ID:
            self.battery_voltage = round(0.01 * int.from_bytes(message.data[0:2], 'little'), 2)
            self.battery_current = round(0.1 * int.from_bytes(message.data[2:4], 'little'), 1)
            self.battery_temperature = round(0.1 * int.from_bytes(message.data[4:6], 'little'), 1)
            
        if message.arbitration_id == MIN_MAX_CELL_VOLT_TEMP_ID:
            self.min_cell_voltage = round(0.001 * int.from_bytes(message.data[0:2], 'little'), 3)
            self.max_cell_voltage = round(0.001 * int.from_bytes(message.data[2:4], 'little'), 3)
            self.min_temperature = int.from_bytes(message.data[4:6], 'little') - KELVN_TO_C
            self.max_temperature = int.from_bytes(message.data[6:8], 'little') - KELVN_TO_C
            
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
        self.notifier = Notifier(self.bus, [self])
        # self.notifier.add_bus(self.bus)
        # self.notifier.add_listener(self)

        # rx = Thread(target = self.can_rx_task)
        # rx.daemon=True
        # rx.start()
    
    def stop(self):
        self.notifier.remove_listener(self) #this order avoids infinite recuss
        self.notifier.stop()
        self.bus.shutdown()




    




