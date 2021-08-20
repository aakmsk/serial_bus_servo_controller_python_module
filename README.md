# serial_bus_servo_controller_python_module
This is a python module to control serial servos (such as LX-224) connected to a serial bus servo controller from a windows machine or a linux machine (such as Raspberry Pi).

LX-224 (https://www.hiwonder.hk/products/hiwonder-lx-224-intelligent-serial-bus-servo)</br>
serial bus servo controller (https://www.hiwonder.hk/collections/servo/products/serial-bus-servo-controller)

# Introduction
In order to make a robot, I used hiwonder's servo (LX-224) and control board (serial bus servo controller), and I tried to control it from python by connecting raspberry pi and control board via USB serial connection. However, there was not much information available, it took a lot of time until I was able to use it. 

In consideration of future use, I created a python module to control the servo from a PC through the control board.

I hope it will be usefull for those who are looking for the same kind of usage as me.

# Connection method
The main connection procedure is in the following three steps.

1. Connect the serial pins of the control board to the USB serial converter.
1. Connect the USB serial converter to the PC (such as raspberry pi).
1. Connect servos and power supply as necessary.

![](https://raw.githubusercontent.com/aakmsk/serial_bus_servo_controller/main/images/img.jpg)

# Download the module
## Terminal:
```
git clone https://github.com/aakmsk/serial_bus_servo_controller.git
cd serial_bus_servo_controller/scripts
```

# Usage
Start the python interpreter.

## Python:
```
import serial_bus_servo_controller as sbsc
controller = sbsc.SBS_Controller("/dev/ttyUSB0")
```
Pass the device name corresponding to the USB serial converter as an argument, and instantiate the SBS_Controller class defined in the module.

- Control specified servos
```
# This is an example of rotating servos with IDs 1 and 2 to positions 100 and 400, respectively, in 500ms.

controller.cmd_servo_move([1, 2], [200, 400], 500)
```
- Get the rotation positions of specified servos
```
# Get the current rotation position of the servos with IDs 1 and 2

p_val = controller.cmd_mult_servo_pos_read([1, 2])
```
- Power off the specified servos
```
# Power off the servos with IDs 1 and 2

controller.cmd_mult_servo_unload([1, 2])
```
- Get the battery voltage
```
b_val = controller.cmd_get_battery_voltage()
```