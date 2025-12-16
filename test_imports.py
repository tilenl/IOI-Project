#!/usr/bin/env python
"""Test script to verify package imports"""

try:
    import numpy as np
    print(f"✓ numpy version: {np.__version__}")
except Exception as e:
    print(f"✗ numpy error: {e}")

try:
    import matplotlib.pyplot as plt
    print(f"✓ matplotlib version: {plt.matplotlib.__version__}")
except Exception as e:
    print(f"✗ matplotlib error: {e}")

try:
    import openvisuspy as ovp
    print("✓ openvisuspy imported successfully")
    if hasattr(ovp, '__version__'):
        print(f"  Version: {ovp.__version__}")
except Exception as e:
    print(f"✗ openvisuspy error: {e}")
    
try:
    import OpenVisus
    print("✓ OpenVisus imported successfully")
    print(f"  Available modules: {[x for x in dir(OpenVisus) if not x.startswith('_')][:10]}")
except Exception as e:
    print(f"✗ OpenVisus error: {e}")

