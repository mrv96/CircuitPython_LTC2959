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
    max_voltage_high = UnaryStruct(LTC2959_REG_MAX_VOLTAGE_MSB, ">H")
    min_voltage_low = UnaryStruct(LTC2959_REG_MIN_VOLTAGE_MSB, ">H")
    current = ROUnaryStruct(LTC2959_REG_CURRENT_MSB, ">h")
    current_threshold_high = UnaryStruct(LTC2959_REG_CURRENT_THRESHOLD_HIGH_MSB, ">h")
    current_threshold_low = UnaryStruct(LTC2959_REG_CURRENT_THRESHOLD_LOW_MSB, ">h")
    max_voltage_high = UnaryStruct(LTC2959_REG_MAX_CURRENT_MSB, ">h")
    min_voltage_low = UnaryStruct(LTC2959_REG_MIN_CURRENT_MSB, ">h")
    temperature = ROUnaryStruct(LTC2959_REG_TEMPERATURE_MSB, ">H")
    temperature_threshold_high = UnaryStruct(LTC2959_REG_TEMPERATURE_THRESHOLD_HIGH_MSB, ">H")
    temperature_threshold_low = UnaryStruct(LTC2959_REG_TEMPERATURE_THRESHOLD_LOW_MSB, ">H")
    gpio = ROUnaryStruct(LTC2959_REG_GPIO_MSB, ">h")
    gpio_threshold_high = UnaryStruct(LTC2959_REG_GPIO_THRESHOLD_HIGH_MSB, ">h")
    gpio_threshold_low = UnaryStruct(LTC2959_REG_GPIO_THRESHOLD_LOW_MSB, ">h")

    def __init__(self, i2c: I2CDevice) -> None:
        self.i2c_device = i2c
        self.sampling = 0  # TODO: use an enum

    def __trigger_adc(self):
        if self.sampling == 0b101:
            self.adc_mode = 0b101

    def set_adc_mode(self, value):
        self.sampling = value
        if self.sampling != 0b101:
            self.adc_mode = self.sampling

    def read_voltage(self):
        self.__trigger_adc()
        return self.voltage * 0.995e-3

    def read_current(self):
        self.__trigger_adc()
        return self.current * 2.975e-6

    def read_temperature(self):
        self.__trigger_adc()
        return self.temperature * 12.8e-3 - 273.15
