"""
This module defines custom exception classes used to handle validation errors
for the `MusicalInstrument` class and its associated descriptors.
"""


class WrongInstrumentType(Exception):
    """
        Exception raised when an invalid instrument type is provided.
    """


class WrongMaterial(Exception):
    """
        Exception raised when an invalid material is provided.
    """


class WrongSoundRegister(Exception):
    """
        Exception raised when an invalid sound register is provided.
    """
