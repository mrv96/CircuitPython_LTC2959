# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 mrv96
#
# SPDX-License-Identifier: MIT
"""
`ltc2959`
================================================================================

CircuitPython module for the LTC2959 ultra-low power battery gas gauge.


* Author(s): mrv96

Implementation Notes
--------------------

**Hardware:**

* Analog Devices `LTC2959 Ultra-Low Power Battery Gas Gauge
  <https://www.analog.com/en/products/ltc2959.html>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from enum import IntEnum

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/mrv96/CircuitPython_LTC2959.git"


LTC2959_I2C_ADDRESS = 0x63

LTC2959_REG_STATUS = 0x00
LTC2959_REG_ADC_CONTROL = 0x01
LTC2959_REG_CULOMB_COUNTER_CONTROL = 0x02
LTC2959_REG_ACCUMULATED_CHARGE_31_24 = 0x03
LTC2959_REG_ACCUMULATED_CHARGE_23_16 = 0x04
LTC2959_REG_ACCUMULATED_CHARGE_15_8 = 0x05
LTC2959_REG_ACCUMULATED_CHARGE_7_0 = 0x06
LTC2959_REG_CHARGE_THRESHOLD_LOW_31_24 = 0x07
LTC2959_REG_CHARGE_THRESHOLD_LOW_23_16 = 0x08
LTC2959_REG_CHARGE_THRESHOLD_LOW_15_8 = 0x09
LTC2959_REG_CHARGE_THRESHOLD_LOW_7_0 = 0x0A
LTC2959_REG_CHARGE_THRESHOLD_HIGH_31_24 = 0x0B
LTC2959_REG_CHARGE_THRESHOLD_HIGH_23_16 = 0x0C
LTC2959_REG_CHARGE_THRESHOLD_HIGH_15_8 = 0x0D
LTC2959_REG_CHARGE_THRESHOLD_HIGH_7_0 = 0x0E
LTC2959_REG_VOLTAGE_MSB = 0x0F
LTC2959_REG_VOLTAGE_LSB = 0x10
LTC2959_REG_VOLTAGE_THRESHOLD_HIGH_MSB = 0x11
LTC2959_REG_VOLTAGE_THRESHOLD_HIGH_LSB = 0x12
LTC2959_REG_VOLTAGE_THRESHOLD_LOW_MSB = 0x13
LTC2959_REG_VOLTAGE_THRESHOLD_LOW_LSB = 0x14
LTC2959_REG_MAX_VOLTAGE_MSB = 0x15
LTC2959_REG_MAX_VOLTAGE_LSB = 0x16
LTC2959_REG_MIN_VOLTAGE_MSB = 0x17
LTC2959_REG_MIN_VOLTAGE_LSB = 0x18
LTC2959_REG_CURRENT_MSB = 0x19
LTC2959_REG_CURRENT_LSB = 0x1A
LTC2959_REG_CURRENT_THRESHOLD_HIGH_MSB = 0x1B
LTC2959_REG_CURRENT_THRESHOLD_HIGH_LSB = 0x1C
LTC2959_REG_CURRENT_THRESHOLD_LOW_MSB = 0x1D
LTC2959_REG_CURRENT_THRESHOLD_LOW_LSB = 0x1E
LTC2959_REG_MAX_CURRENT_MSB = 0x1F
LTC2959_REG_MAX_CURRENT_LSB = 0x20
LTC2959_REG_MIN_CURRENT_MSB = 0x21
LTC2959_REG_MIN_CURRENT_LSB = 0x22
LTC2959_REG_TEMPERATURE_MSB = 0x23
LTC2959_REG_TEMPERATURE_LSB = 0x24
LTC2959_REG_TEMPERATURE_THRESHOLD_HIGH_MSB = 0x25
LTC2959_REG_TEMPERATURE_THRESHOLD_HIGH_LSB = 0x26
LTC2959_REG_TEMPERATURE_THRESHOLD_LOW_MSB = 0x27
LTC2959_REG_TEMPERATURE_THRESHOLD_LOW_LSB = 0x28
LTC2959_REG_GPIO_MSB = 0x29
LTC2959_REG_GPIO_LSB = 0x2A
LTC2959_REG_GPIO_THRESHOLD_HIGH_MSB = 0x2B
LTC2959_REG_GPIO_THRESHOLD_HIGH_LSB = 0x2C
LTC2959_REG_GPIO_THRESHOLD_LOW_MSB = 0x2D
LTC2959_REG_GPIO_THRESHOLD_LOW_LSB = 0x2E


class LTC2959AdcMode(IntEnum):
    SLEEP = 0
    SMART_SLEEP = 1
    CONTINUOUS_VOLTAGE = 2
    CONTINUOUS_CURRENT = 3
    CONTINUOUS_ALTERNATE = 4
    SINGLE_SHOT = 5
    CONTINUOUS = 6
    DEFAULT = SLEEP


class LTC2959AdcGpio(IntEnum):
    ALERT = 0
    CHARGE_COMPLETE = 1
    ANALOG_DUAL_SUPPLY = 2
    ANALOG_SINGLE_SUPPLY = 3
    DEFAULT = ANALOG_SINGLE_SUPPLY


class LTC2959AdcVoltageInput(IntEnum):
    VDD = 0
    VBAT_LOW_SIDE_SENSING = 0
    SENSEN = 1
    VBAT_HIGH_SIDE_SENSING = 1
    DEFAULT = VDD


class LTC2959:
    gpio_alert = ROBit(LTC2959_REG_STATUS, 7)
    current_alert = ROBit(LTC2959_REG_STATUS, 6)
    charge_overflow_underflow = ROBit(LTC2959_REG_STATUS, 5)
    temperature_alert = ROBit(LTC2959_REG_STATUS, 4)
    charge_alert_high = ROBit(LTC2959_REG_STATUS, 3)
    charge_alert_low = ROBit(LTC2959_REG_STATUS, 2)
    voltage_alert = ROBit(LTC2959_REG_STATUS, 1)
    uvlo_alert = ROBit(LTC2959_REG_STATUS, 0)
    adc_mode = RWBits(3, LTC2959_REG_ADC_CONTROL, 5)
    gpio_configure = RWBits(2, LTC2959_REG_ADC_CONTROL, 3)
    configure_voltage_input = RWBit(LTC2959_REG_ADC_CONTROL, 2)
    culomb_counter_deband = RWBits(2, LTC2959_REG_CULOMB_COUNTER_CONTROL, 6)
    do_not_count = RWBit(LTC2959_REG_CULOMB_COUNTER_CONTROL, 3)
    accumulated_charge = UnaryStruct(LTC2959_REG_ACCUMULATED_CHARGE_31_24, ">I")
    charge_threshold_low = UnaryStruct(LTC2959_REG_CHARGE_THRESHOLD_LOW_31_24, ">I")
    charge_threshold_high = UnaryStruct(LTC2959_REG_CHARGE_THRESHOLD_HIGH_31_24, ">I")
    voltage = ROUnaryStruct(LTC2959_REG_VOLTAGE_MSB, ">H")
    voltage_threshold_high = UnaryStruct(LTC2959_REG_VOLTAGE_THRESHOLD_HIGH_MSB, ">H")
    voltage_threshold_low = UnaryStruct(LTC2959_REG_VOLTAGE_THRESHOLD_LOW_MSB, ">H")
    max_voltage = UnaryStruct(LTC2959_REG_MAX_VOLTAGE_MSB, ">H")
    min_voltage = UnaryStruct(LTC2959_REG_MIN_VOLTAGE_MSB, ">H")
    current = ROUnaryStruct(LTC2959_REG_CURRENT_MSB, ">h")
    current_threshold_high = UnaryStruct(LTC2959_REG_CURRENT_THRESHOLD_HIGH_MSB, ">h")
    current_threshold_low = UnaryStruct(LTC2959_REG_CURRENT_THRESHOLD_LOW_MSB, ">h")
    max_current = UnaryStruct(LTC2959_REG_MAX_CURRENT_MSB, ">h")
    min_current = UnaryStruct(LTC2959_REG_MIN_CURRENT_MSB, ">h")
    temperature = ROUnaryStruct(LTC2959_REG_TEMPERATURE_MSB, ">H")
    temperature_threshold_high = UnaryStruct(LTC2959_REG_TEMPERATURE_THRESHOLD_HIGH_MSB, ">H")
    temperature_threshold_low = UnaryStruct(LTC2959_REG_TEMPERATURE_THRESHOLD_LOW_MSB, ">H")
    gpio = ROUnaryStruct(LTC2959_REG_GPIO_MSB, ">h")
    gpio_threshold_high = UnaryStruct(LTC2959_REG_GPIO_THRESHOLD_HIGH_MSB, ">h")
    gpio_threshold_low = UnaryStruct(LTC2959_REG_GPIO_THRESHOLD_LOW_MSB, ">h")

    def __init__(self, i2c: I2CDevice, rsense: float = 50e-3) -> None:
        self.i2c_device = i2c
        self.adc_single_shot: bool = False
        self.rsense = rsense

    @staticmethod
    def __raw_to_voltage(value: int) -> float:
        return 62.6 / 65536 * value

    @staticmethod
    def __voltage_to_raw(value: float) -> int:
        return round(value / 62.6 * 65536) & 0xFFFF

    def __raw_to_current(self, value: int) -> float:
        return 97.5e-3 / self.rsense / 32768 * value

    def __current_to_raw(self, value: float) -> int:
        return round(value * self.rsense / 97.5e-3 * 32768) & 0xFFFF

    @staticmethod
    def __raw_to_temperature(value: int) -> float:
        return 825 / 65536 * value - 273.15

    @staticmethod
    def __temperature_to_raw(value: float) -> int:
        return round((value + 273.15) / 825 * 65536) & 0xFFFF

    def set_adc_config(
        self, mode: LTC2959AdcMode, gpio: LTC2959AdcGpio, vin: LTC2959AdcVoltageInput
    ) -> None:
        self.adc_single_shot = True if mode == LTC2959AdcMode.SINGLE_SHOT else False
        if not self.adc_single_shot:
            self.adc_mode = mode
        self.gpio_configure = gpio
        self.configure_voltage_input = vin

    def read_adc_single_shot(self) -> None:
        if not self.adc_single_shot:
            raise RuntimeError("ADC is not configured in single-shot mode")
        self.adc_mode = LTC2959AdcMode.SINGLE_SHOT

    def get_voltage(self) -> float:
        return self.__raw_to_voltage(self.voltage)

    def get_max_voltage(self) -> float:
        return self.__raw_to_voltage(self.max_voltage)

    def set_max_voltage(self, value: float) -> None:
        self.max_voltage = self.__voltage_to_raw(value)

    def get_min_voltage(self) -> float:
        return self.__raw_to_voltage(self.min_voltage)

    def set_min_voltage(self, value: float) -> None:
        self.min_voltage = self.__voltage_to_raw(value)

    def get_current(self) -> float:
        return self.__raw_to_current(self.current)

    def get_max_current(self) -> float:
        return self.__raw_to_current(self.max_current)

    def set_max_current(self, value: float) -> None:
        self.max_current = self.__current_to_raw(value)

    def get_min_current(self) -> float:
        return self.__raw_to_current(self.min_current)

    def set_min_current(self, value: float) -> None:
        self.min_current = self.__current_to_raw(value)

    def get_temperature(self) -> float:
        return self.__raw_to_temperature(self.temperature)
