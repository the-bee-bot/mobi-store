import sys
import os

# insert the path where app module can be loaded
path = os.path.join(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)
from app import app as application
