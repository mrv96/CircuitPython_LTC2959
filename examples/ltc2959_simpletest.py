# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 mrv96
#
# SPDX-License-Identifier: Unlicense

# TESTED WITH FT232H
# import os
# os.environ['BLINKA_FT232H'] = '1'

import sched
import time

import board
from adafruit_bus_device.i2c_device import I2CDevice

from ltc2959 import (
    LTC2959,
    LTC2959_CULOMB_COUNTER_RESET_VALUE,
    LTC2959_I2C_ADDRESS,
    LTC2959AdcGpio,
    LTC2959AdcMode,
    LTC2959AdcVoltageInput,
    LTC2959Deband,
)


def monitor_accumulated_charge(scheduler, elapsed_time):
    # schedule the next call first
    scheduler.enter(1, 1, monitor_accumulated_charge, (scheduler, elapsed_time + 1))

    accumulated_charge = ltc2959_device.get_relative_accumulated_charge()
    print(f"{elapsed_time} [s], {accumulated_charge} [Ah]")

    ltc2959_status = ltc2959_device.read_status()
    if ltc2959_status.charge_overflow_underflow:
        print("WARNING: charge Overflow/Underflow")
    if ltc2959_status.uvlo_alert:
        print("WARNING: UVLO Alert")

    if accumulated_charge != 0:
        raise SystemExit()


if __name__ == "__main__":
    ltc2959_device = LTC2959(I2CDevice(board.I2C(), LTC2959_I2C_ADDRESS))

    print("Read ADC values")

    # Read Vdd first
    ltc2959_device.set_adc_config(
        LTC2959AdcMode.SINGLE_SHOT, LTC2959AdcGpio.DEFAULT, LTC2959AdcVoltageInput.DEFAULT
    )
    ltc2959_device.read_adc_single_shot()

    vdd = ltc2959_device.get_voltage()

    # Read VBat and print all available measures got from ADC
    ltc2959_device.set_adc_config(
        LTC2959AdcMode.SINGLE_SHOT, LTC2959AdcGpio.DEFAULT, LTC2959AdcVoltageInput.SENSEN
    )
    ltc2959_device.read_adc_single_shot()

    print(f"- Vdd:\t{vdd} [V]")
    print(f"- VBat:\t{ltc2959_device.get_voltage()} [V]")
    print(f"- IBat:\t{ltc2959_device.get_current()} [A]")
    print(f"- T:\t{ltc2959_device.get_temperature()} [Celsius]")
    print()

    # Prepare the scheduler to monitor accumulated charge every second
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(1, 1, monitor_accumulated_charge, (my_scheduler, 0))

    # Initialize the LTC2959 device for monitoring accumulated charge
    ltc2959_device.read_status()  # reset ULVO alert (set by default on power up)
    ltc2959_device.set_deband(LTC2959Deband.VOLTAGE_0UV)  # count charge even if current < 400uA
    ltc2959_device.accumulated_charge = LTC2959_CULOMB_COUNTER_RESET_VALUE

    print("Waiting for changes in accumulated charge...")
    my_scheduler.run()
