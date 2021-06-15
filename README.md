# recq

This is a package to collect operating information from the REC Q BMS via CANBUS, Binary Inputs, and later RS-485.

This is an expirement in packaging following [this guide](https://packaging.python.org/tutorials/packaging-projects/), as modified by [this guide](https://docs.python-guide.org/writing/structure/), and some help from section 2.2 of the [setup script documentation](https://docs.python.org/3/distutils/setupscript.html).

### Getting Started

Note, this code depends a a very specific set of hardware running.  Some details can be found [here](https://github.com/natecostello/van_two_point_oh/blob/master/blog/2021-4-08/rpi-to-rec-q-can-comms.md).

```
%python3 -m pip install git+https://github.com/natecostello/rec_bms_status.git
```
```
%python3
>>>from recq.binary import BinaryMonitor
>>> b = BinaryMonitor()
>>> b.chargeEnable
1
>>> b.sysPlus
0
>>> b.contactor
1

>>> from recq.canbus import CanBusMonitor
>>> import os
>>> os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
0
>>> c = CanBusMonitor()
>>> c.start()
>>> c.charge_current_limit
70.0
>>> c.alarmBits
'10101000 10100000 10000010 00000000'
```
