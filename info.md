Skogås station: 740000757
Fäbodvägen: 740045561

# wsgi.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from main import app as application