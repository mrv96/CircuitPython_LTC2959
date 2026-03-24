# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 mrv96
#
# SPDX-License-Identifier: Unlicense

# TESTED WITH FT232H
# import os
# os.environ['BLINKA_FT232H'] = '1'

import board
from adafruit_bus_device.i2c_device import I2CDevice

from ltc2959 import LTC2959, LTC2959_I2C_ADDRESS

if __name__ == "__main__":
    ltc2959_device = LTC2959(I2CDevice(board.I2C(), LTC2959_I2C_ADDRESS))
    ltc2959_device.set_adc_mode(0b101)
    print(ltc2959_device.read_voltage(), "[V]")
    print(ltc2959_device.read_current(), "[A]")
    print(ltc2959_device.read_temperature(), "[Celsius]")
