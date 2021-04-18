import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from recq.binary import BinaryMonitor
from recq.canbus import CanBusMonitor

# No idea if this is doing what it supposed to as described
# https://docs.python-guide.org/writing/structure/
# but they are running (though perhaps from the pip'd install)