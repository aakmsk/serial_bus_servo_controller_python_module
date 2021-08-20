# coding: utf-8
import serial
import time

class SBS_Controller:
    def __init__(self, dev, baud_rate=9600):
        """
        SBS_Controller: Serial Bus Servo controller class.
                        By using this class, you can control servos with Serial Bus Servo Controller.
                        Serial Bus Servo Controller (https://www.hiwonder.hk/products/serial-bus-servo-controller)
        functions:
            cmd_servo_move
            cmd_get_battery_voltage
            cmd_mult_servo_unload
            cmd_mult_servo_pos_read
        Prameters:
            dev: string
                e.g. dev = "/dev/ttyUSB0"
            baud_rate: int
                e.g. baud_rate = 9600 
                (note. Serial bus servo communication Baud Rate is 115200 baud.
                       On the other hand, LSC Series Servo Controller communication Baud Rate is 9600 baud.
                       For this reason, You have to select 9600 baud.
                       Don't get confused.)
        """
        self.ser = serial.Serial(dev, baud_rate)

    def cmd_servo_move(self, servo_id, angle_position, time):
        """
        Description: Control the rotation of any servo.
                     The rotation time of all servos commanded by this function will be the same.
        Parameters: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]   
            angle_position: list
                e.g. angle_position = [1000, 2000, 1000, 2000]  
                (note. The number of elements must be the same as servo_id)
            time: int (ms)
                e.g. time = 1000    
        return:
        """
        buf = bytearray(b'\x55\x55')                # header 
        buf.extend([0xff & (len(servo_id)*3+5)])    # length (the number of control servo * 3 + 5)
        buf.extend([0x03])                          # command value

        buf.extend([0xff & len(servo_id)])          # The number of servo to be controlled
        
        time = 0xffff & time
        buf.extend([(0xff & time), (0xff & (time >> 8))])   # Lower and Higher 8 bits of time value

        for i in range(len(servo_id)):
            p_val = 0xffff & angle_position[i]
            buf.extend([0xff & servo_id[i]])    # servo id
            buf.extend([(0xff & p_val), (0xff & (p_val >> 8))])   # Lower and Higher 8 bits of angle posiotion value

        self.ser.write(buf)

    def cmd_get_battery_voltage(self):
        """
        Description: Get the servo controller's battery voltage in unit millivolts.
        return: 
            battery_voltage: float (V)
        """
        # transmit
        buf = bytearray(b'\x55\x55')    # header 
        buf.extend([0x02])              # length
        buf.extend([0x0F])              # command value
        # Empty the contents of the cache in preparation for receiving data.
        count = self.ser.inWaiting()    # Check receive cache.
        if count != 0:
            _ = self.ser.read(count)    # Read out data
        # Send command.
        self.ser.write(buf)

        # Receive
        count = 0
        recv_cmd_len = 6
        while count != recv_cmd_len:        # Waiting for reception to finish.
            count = self.ser.inWaiting()
        recv_data = self.ser.read(count)    # Read the received byte data.
        if count == recv_cmd_len:                      # Check if the number of bytes of data received is correct as a response to this command.
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[3] == 0x0F : # Check if the received data is a response to a command.
                battery_voltage = 0xffff & (recv_data[4] | (0xff00 & (recv_data[5] << 8))) # Read battery  voltage
                battery_voltage = battery_voltage / 1000.0

        return battery_voltage

    def cmd_mult_servo_unload(self, servo_id):
        """
        Description: Power off multiple servos and its motors, after sending this command.
        Parameters: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]     
        return:
        """
        buf = bytearray(b'\x55\x55')                # header 
        buf.extend([0xff & (len(servo_id)+3)])      # length (the number of control servo + 3)
        buf.extend([0x14])                          # command value

        buf.extend([0xff & len(servo_id)])          # The number of servo to be controlled.

        for i in range(len(servo_id)):
            buf.extend([0xff & servo_id[i]])    # servo id

        self.ser.write(buf)      

    def cmd_mult_servo_pos_read(self, servo_id):
        """
        Description: Read a angle position values of multiple servos.
        Parameters: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]   
        return: 
            angle_pos_values: list 
                note. The list size is the same as the number of servos you want to get values.
        """
        # transmit
        buf = bytearray(b'\x55\x55')            # header 
        buf.extend([0xff & (len(servo_id)+3)])  # length (the number of control servo + 3)
        buf.extend([0x15])                      # command value
        buf.extend([0xff & len(servo_id)])          # The number of servo to be controlled.

        for i in range(len(servo_id)):
            buf.extend([0xff & servo_id[i]])    # servo id

        # Empty the contents of the cache in preparation for receiving data.
        count = self.ser.inWaiting()    # Check receive cache.
        if count != 0:
            _ = self.ser.read(count)    # Read out data
        # Send command.
        self.ser.write(buf)

        # Receive
        count = 0
        recv_cmd_len = len(servo_id) * 3 + 5
        angle_pos_values = servo_id.copy()  # Create a list whose size is the same as the number of servos you want to get values from.
        while count != recv_cmd_len:        # Waiting for reception to finish.
            count = self.ser.inWaiting()
        recv_data = self.ser.read(count)    # Read the received byte data.
        if count == recv_cmd_len:           # Check if the number of bytes of data received is correct as a response to this command.
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[3] == 0x15:  # Check if the received data is a response to a command.
                for i in range(len(servo_id)):
                    angle_pos_values[i] = 0xffff & (recv_data[6+3*i] | (0xff00 & (recv_data[7+3*i] << 8))) # Read battery  voltage

        return angle_pos_values
