#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import serial

"""
需要先把控制程序py2arduino_multi_servo.pde通过Arduino IDE烧录到Arduino UNO R3开发板上, 再配合下面的脚本来实现Python控制硬件设备
主要的作用是通过串口把控制字符发送到开发板上, 再通过控制程序控制对应的硬件设备
"""

command_list = {
    "set_digital_low": "1",
    "set_digital_high": "2",
    "get_digital_status": "3",
    "set_analog_value": "4",
    "get_analog_status": "5",
    "set_servo_angle": "6",
    "turn_servo_then_turn_back": "7",
    "reset_servo_angle_to_0": "8",
    "reset_servo_angle_to_90": "9",
    "get_servo_angle": "10",
    "set_build_in_led_low": "21",
    "set_build_in_led_high": "22",
    "reset_the_board": "91",
}

class Arduino(object):

    __OUTPUT_PINS = -1

    def __init__(self, port, baud_rate=115200):
        self.serial = serial.Serial(port, baud_rate)
        self.output_devices = None

    def __str__(self):
        return "Arduino is on port %s at %d baud_rate" % (self.serial.port, self.serial.baudrate)

    def specify_output_device(self, output_device: dict):
        """指定输出(控制)的设备并且指定设备所使用的端口, 可以同时指定一个或者多个设备

        :param output_device: 输出(控制)的设备类型与对应设备使用的端口
                              其中, 设备类型可以为数字开关(直接输出高低电平)为"Pin", 伺服电机为"Servo", 内置LED为"L"
                              Pin可以使用的端口为1 - 13
                              由于某些需要, 要在初始化时预先设置Servo的角度, Servo的角度可以是1 ~ 180度, 一般Servo的初始位置是约90度
                              Servo可以使用的端口为3, 5, 6, 9, 10, 11(PWM端口) (最多可以连接6个, 但暂时只能一次控制一个Servo)
                              内置LED端口为98(但98不是实际Build in LED的端口, 只是为了与其它设备分开所以将它设定为98
                              示例:
                              {"Pin": (1,3,5,7),
                               "Servo": [(90, 9)],
                               "L": 98
                              }
        :return: None
        """

        self.reset_the_board()
        time.sleep(1)
        self.output_devices = output_device
        device_pin_list = list()
        pin_list = list()
        if output_device.get("Pin"):
            device_pin_list.append(output_device["Pin"])
            pin_list.append(output_device["Pin"])

        if output_device.get("Servo"):
            servo_list = output_device["Servo"]
            if isinstance(servo_list, list):
                for sl in servo_list:
                    # 这里的数字是控制程序初始化时设定的添加Servo控制的代号, 其实可以自己定义的, 注意串口传字符限制比较多,
                    # 所以一般传数字在控制程序那边会容易解释出来, 但实际上这里可以传英文字比如直接把Servo作为关键字传过去
                    device_pin_list.append(99)  # Servo的控制代号
                    device_pin_list.append(sl[0])  # Servo的初始角度
                    device_pin_list.append(sl[1])  # Servo的端口号
                    pin_list.append(sl[1])
            else:
                device_pin_list.append(99)
                device_pin_list.append(servo_list[0])
                device_pin_list.append(servo_list[1])
                pin_list.append(servo_list[1])

        if output_device.get("L"):
            device_pin_list.append(98) # 这里的数字是控制程序初始化时设定的添加内置LED控制的代号, 其实可以自己定义的
            pin_list.append(98)

        pin_list = tuple(set(pin_list))  # 去重
        if len(pin_list) > 0:
            self.__send_data(len(pin_list))
            for dpl in device_pin_list:
                self.__send_data(dpl)
            self.__OUTPUT_PINS = pin_list

    def set_digital_low(self, pin):
        self.__send_data(command_list['set_digital_low'])
        self.__send_data(pin)
        return True

    def set_digital_high(self, pin):
        self.__send_data(command_list['set_digital_high'])
        self.__send_data(pin)
        return True

    def get_digital_status(self, pin):
        """
        获得指定pin号的状态, 一般来说1为高电平状态, 0为低电平状态
        :param pin:
        :return:
        """
        self.__send_data(command_list['get_digital_status'])
        self.__send_data(pin)
        return self.__format_pin_state(self.__get_data()[0])

    def set_analog_value(self, pin, value):
        self.__send_data(command_list['set_analog_value'])
        self.__send_data(pin)
        self.__send_data(value)
        return True

    def get_analog_status(self, pin):
        """
        模拟输入的状态就不止0与1, 一般会是0 - 1024之类的比较大范围的值
        :param pin:
        :return:
        """
        self.__send_data(command_list['get_analog_status'])
        self.__send_data(pin)
        return self.__get_data()

    def set_servo_angle(self, servo_index=1, angle=90, servo_speed=25):
        """
        设置舵机的角度
        :param servo_index: 范围1 - 6, 注意这是舵机的顺序而不是它的端口号, 根据设置的时的顺序排列
        :param angle: 设置舵机转动的目标角度, 范围1 - 180
        :param servo_speed: 设置舵机转动的速度, 范围1 - 50
        :return:
        """
        self.__send_data(command_list['set_servo_angle'])
        # 如果有超过一个Servo, 需要先指定Servo
        if len(self.output_devices['Servo']) > 1:
            self.__send_data(str(servo_index))
        self.__send_data(angle)
        self.__send_data(servo_speed)
        return True

    def turn_servo_then_turn_back(self, servo_index=1, angle=90, servo_speed=25):
        """
        把舵机转一个角度, 然后隔一会儿后让舵机转回原来的角度
        :param servo_index: 范围1 - 6, 注意这是舵机的顺序而不是它的端口号, 根据设置的时的顺序排列
        :param angle: 设置舵机转动的目标角度, 范围1 - 180
        :param servo_speed: 设置舵机转动的速度, 范围1 - 50
        :return:
        """
        self.__send_data(command_list['turn_servo_then_turn_back'])
        # 如果有超过一个Servo, 需要先指定Servo
        if len(self.output_devices['Servo']) > 1:
            self.__send_data(str(servo_index))
        self.__send_data(angle)
        self.__send_data(servo_speed)
        return True

    def reset_servo_angle_to_0(self):
        """
        设置舵机的角度为0
        :return:
        """
        self.__send_data(command_list['reset_servo_angle_to_0'])
        return True

    def reset_servos_angle_to_90(self):
        """
        设置舵机的角度为90
        :return:
        """
        self.__send_data(command_list['reset_servo_angle_to_90'])
        return True

    def get_servo_angle(self, servo_index=1) -> int:
        """
        获取舵机现在的角度, 只有曾经set过角度后才能正确读取
        :return: 舵机角度
        """
        if len(self.output_devices['Servo']) > 1:
            self.__send_data(str(servo_index))
        self.__send_data(command_list['get_servo_angle'])
        return int(self.__get_data())

    def set_build_in_led_low(self):
        self.__send_data(command_list['set_build_in_led_low'])
        return True

    def set_build_in_led_high(self):
        self.__send_data(command_list['set_build_in_led_high'])
        return True

    def turn_off_all_digital_pins(self):
        for each_pin in self.__OUTPUT_PINS:
            self.set_digital_low(each_pin)
        return True

    def reset_the_board(self):
        self.__send_data(command_list['reset_the_board'])
        return True

    def __send_data(self, serial_data):

        # 由于在prototype.pde中规定readData中会先打印"w"再接收输入
        # 所以如果arduino中返回的未返回新一个"w"前, 可以认为是未到可以输入的状态
        while self.__get_data()[0] != "w":
            pass
        serial_data = str(serial_data).encode('utf-8')
        self.serial.write(serial_data)

    def __get_data(self):
        input_string = self.serial.readline()
        input_string = input_string.decode('utf-8')
        return input_string.rstrip('\n')

    def __format_pin_state(self, pinValue):
        if pinValue == '1':
            return True
        else:
            return False

    def close(self):
        self.serial.close()
        return True
