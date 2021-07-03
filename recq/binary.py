from gpiozero import DigitalInputDevice
from instrument_logger import Instrument

class BinaryMonitor(Instrument):

    def __init__(self, internalRelayPin=25, chargeEnablePin=18, sysPlusPin=23, contactorPin=24):
        self._internalRelay = DigitalInputDevice(internalRelayPin)
        self._chargeEnable = DigitalInputDevice(chargeEnablePin)
        self._sysPlus = DigitalInputDevice(sysPlusPin)
        self._contactor = DigitalInputDevice(contactorPin)


    @property
    def internalRelay(self) -> int:
        """Returns 1 if the REC Internal Relay is ON/Closed, else 0"""
        return self._internalRelay.value

    @property
    def chargeEnable(self) -> int:
        """Returns 1 if the REC Charge Enable is ON, else 0"""
        return self._chargeEnable.value

    @property
    def sysPlus(self) -> int:
        """Returns 1 if Pre-Charge is active, else 0"""
        return self._sysPlus.value

    @property
    def contactor(self) -> int:
        """Returns 1 if the Main Contactor is Energized/Closed via the REC, else 0"""
        return self._contactor.value

    @property
    def name(self) -> str:
        """See Instrument"""
        return 'rec-q-binary'

    @property
    def allmeasurements(self) -> 'dict':
        """See Instrument"""
        all_meas = {}
        for param in self.parameters:
            all_meas[param] = self.getmeasurement(param)
        return all_meas

    @property
    def parameters(self) -> 'list[str]':
        """See Instrument"""
        return [
            self.name + '.internal_relay.binary', 
            self.name + '.charge_enable.binary', 
            self.name + '.system_plus.binary',
            self.name + '.contactor.binary']
        
    def getmeasurement(self, name: str) -> str:
        """See Instrument"""
        if (name == self.name + '.internal_relay.binary'):
            return str(self.internalRelay)
        if (name == self.name + '.charge_enable.binary'):
            return str(self.chargeEnable)
        if (name == self.name + '.system_plus.binary'):
            return str(self.sysPlus)
        if (name == self.name + '.contactor.binary'):
            return str(self.contactor)

