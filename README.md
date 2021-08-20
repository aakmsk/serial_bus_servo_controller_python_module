# serial_bus_servo_controller_python_module
This is a python module to control serial servos (such as LX-224) connected to a serial bus servo controller from a windows machine or a linux machine (such as Raspberry Pi).

LX-224 (https://www.hiwonder.hk/products/hiwonder-lx-224-intelligent-serial-bus-servo)</br>
serial bus servo controller (https://www.hiwonder.hk/collections/servo/products/serial-bus-servo-controller)

# Introduction
In order to make a robot, I used hiwonder's servo (LX-224) and control board (serial bus servo controller), and I tried to control it from python by connecting raspberry pi and control board via USB serial connection. However, there was not much information available, it took a lot of time until I was able to use it. 

In consideration of future use, I created a python module to control the servo from a PC through the control board.

I hope it will be usefull for those who are looking for the same kind of usage as me.

# Connection method

