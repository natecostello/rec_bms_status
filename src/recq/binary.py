from gpiozero import DigitalInputDevice

class BinaryMonitor:

    def __init__(self, internalRelayPin=25, chargeEnablePin=18, sysPlusPin=23, contactorPin=24):
        self._internalRelay = DigitalInputDevice(internalRelayPin)
        self._chargeEnable = DigitalInputDevice(chargeEnablePin)
        self._sysPlus = DigitalInputDevice(sysPlusPin)
        self._contactor = DigitalInputDevice(contactorPin)

    @property
    def internalRelay(self):
        return self._internalRelay.value

    @property
    def chargeEnable(self):
        return self._chargeEnable.value

    @property
    def sysPlus(self):
        return self._sysPlus.value

    @property
    def contactor(self):
        return self._contactor.value