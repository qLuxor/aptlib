"""
Control Thor Labs APT Devices without relying on the Thor Labs ActiveX control.
All that is required is the pylibftdi wrapper to libftdi1 driver.
"""
import sys
from .aptmotor import AptMotor
from .aptpiezo import AptPiezo

