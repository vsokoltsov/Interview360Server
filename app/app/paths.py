import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))

BASE_DIR = os.path.join(PROJECT_ROOT, 'app')
COMMON_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.dirname(__name__)),
        '../'))
if COMMON_DIR not in sys.path:
    sys.path.insert(1, COMMON_DIR)
