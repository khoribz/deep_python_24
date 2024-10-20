"""
Unit tests for the `MusicalInstrument` class and its associated exception handling.
These tests cover the validation of instrument attributes and how they are managed using descriptors.
"""

import pytest
from descriptor import MusicalInstrument
from exceptions import WrongInstrumentType, WrongMaterial, WrongSoundRegister


def test_valid_instrument():
    """
    Test creating a valid `MusicalInstrument` object and ensure all attributes
    are correctly set and the string representation is accurate.
    """
    instrument = MusicalInstrument('string', 'wood', 'medium')
    assert instrument.instrument_type == 'string'
    assert instrument.material == 'wood'
    assert instrument.sound_register == 'medium'
    assert str(instrument) == "Instrument: Type - string, Material - wood, Sound Register - medium"


def test_invalid_params():
    """
    Test creating `MusicalInstrument` objects with invalid parameters to ensure
    appropriate exceptions are raised for each invalid attribute.
    """
    with pytest.raises(WrongInstrumentType):
        MusicalInstrument('electronic', 'wood', 'medium')
    with pytest.raises(WrongMaterial):
        MusicalInstrument('string', 'glass', 'medium')
    with pytest.raises(WrongSoundRegister):
        MusicalInstrument('string', 'wood', 'ultra-high')
    with pytest.raises(WrongInstrumentType):
        MusicalInstrument(None, 'wood', 'medium')
    with pytest.raises(WrongMaterial):
        MusicalInstrument('string', 142, 'medium')
    with pytest.raises(WrongSoundRegister):
        MusicalInstrument('string', 'wood', 'wood')


def test_change_attributes():
    """
    Test changing the attributes of a valid `MusicalInstrument` object to valid and invalid values,
    and ensure that appropriate exceptions are raised when setting invalid values.
    """
    instrument = MusicalInstrument('string', 'wood', 'medium')
    instrument.instrument_type = 'wind'
    assert instrument.instrument_type == 'wind'
    assert str(instrument) == "Instrument: Type - wind, Material - wood, Sound Register - medium"
    with pytest.raises(WrongInstrumentType):
        instrument.instrument_type = 'electronic'
    assert instrument.instrument_type == 'wind'

    instrument.material = 'metal'
    assert instrument.material == 'metal'
    assert str(instrument) == "Instrument: Type - wind, Material - metal, Sound Register - medium"
    with pytest.raises(WrongMaterial):
        instrument.material = 'glass'
    assert instrument.material == 'metal'

    instrument.sound_register = 'low'
    assert instrument.sound_register == 'low'
    assert str(instrument) == "Instrument: Type - wind, Material - metal, Sound Register - low"
    with pytest.raises(WrongSoundRegister):
        instrument.sound_register = 'ultra-high'
    assert instrument.sound_register == 'low'


def test_independent_objects_all_attributes():
    """
    Test that multiple `MusicalInstrument` objects maintain independent attributes,
    and changing attributes of one object does not affect the other.
    """
    instrument1 = MusicalInstrument('string', 'wood', 'medium')
    instrument2 = MusicalInstrument('wind', 'metal', 'high')

    assert instrument1.instrument_type == 'string'
    assert instrument1.material == 'wood'
    assert instrument1.sound_register == 'medium'
    assert instrument2.instrument_type == 'wind'
    assert instrument2.material == 'metal'
    assert instrument2.sound_register == 'high'

    instrument1.instrument_type = 'keyboard'
    instrument1.material = 'plastic'
    instrument1.sound_register = 'high'

    assert instrument1.instrument_type == 'keyboard'
    assert instrument1.material == 'plastic'
    assert instrument1.sound_register == 'high'

    assert instrument2.instrument_type == 'wind'
    assert instrument2.material == 'metal'
    assert instrument2.sound_register == 'high'
