"""
This module defines descriptors and a `MusicalInstrument` class to represent musical instruments.
The descriptors are used to validate specific attributes such as instrument type, material,
and sound register. The `MusicalInstrument` class uses these descriptors to ensure that
each musical instrument created is valid based on predefined settings.
"""

import settings
from exceptions import WrongInstrumentType, WrongMaterial, WrongSoundRegister


class BaseDescriptor:
    """
       Base class for descriptors that validate attributes.
    """

    def __init__(self) -> None:
        """
        Initializes the BaseDescriptor. `_name` is initially set to None and
        later assigned in `__set_name__`.
        """
        self._name: str = ''

    def __set_name__(self, class_type: type, name: str) -> None:
        """
            Sets the name of the descriptor's hidden attribute.
            :param class_type: The class the descriptor is defined on.
            :param name: The name of the descriptor.
        """
        self._name = f'_hidden_{name}'

    def __get__(self, obj: object, class_type: type) -> object:
        """
        Retrieves the value of the hidden attribute from the instance.
        :param obj: The instance of the class.
        :param class_type: The class type.
        :return: The value of the hidden attribute.
        """
        if obj is None:
            return None
        return getattr(obj, self._name)

    def __set__(self, obj: object, value: str | int) -> None:
        """
            Sets the value of the hidden attribute with validation.
            :param obj: The instance of the class.
            :param value: The value to be set after validation.
        """
        self.validate(value)
        setattr(obj, self._name, value)

    def validate(self, value: str | int) -> None:
        """
            Abstract method for validation, to be implemented in subclasses.
            :param value: The value to be validated.
            :raises NotImplementedError: if not overridden by subclasses.
        """
        raise NotImplementedError


class InstrumentType(BaseDescriptor):
    """
        Descriptor for validating the type of a musical instrument.
    """

    def validate(self, value: str | int) -> None:
        if value not in settings.INSTRUMENT_ALLOWED_TYPES:
            raise WrongInstrumentType


class Material(BaseDescriptor):
    """
        Descriptor for validating the material of a musical instrument.
    """

    def validate(self, value: str | int) -> None:
        if value not in settings.ALLOWED_MATERIALS:
            raise WrongMaterial


class SoundRegister(BaseDescriptor):
    """
        Descriptor for validating the sound register of a musical instrument.
    """

    def validate(self, value: int | str) -> None:
        if value not in settings.SOUND_ALLOWED_REGISTERS:
            raise WrongSoundRegister


class MusicalInstrument:
    """
        Represents a musical instrument with specific type, material, and sound register.
    """
    instrument_type = InstrumentType()
    material = Material()
    sound_register = SoundRegister()

    def __init__(self, instrument_type: str, material: str, sound_register: str) -> None:
        """
            Initializes the musical instrument with the given type, material, and sound register.
            :param instrument_type: Type of the instrument.
            :param material: Material the instrument is made of.
            :param sound_register: Sound register of the instrument.
        """
        self.instrument_type = instrument_type
        self.material = material
        self.sound_register = sound_register

    def __str__(self) -> str:
        """
            Returns a string representation of the musical instrument.
            :return: String describing the instrument's type, material, and sound register.
        """
        return (f"Instrument: Type - {self.instrument_type}, Material - {self.material}, "
                f"Sound Register - {self.sound_register}")
