import time

import serial as s


# gcode_init_commands = (
#     # '$$',
#     '$0=10',
#     '$1=25',
#     '$2=0',
#     '$3=0',
#     '$4=0',
#     '$5=0',
#     '$6=0',
#     '$10=3',
#     '$11=0.010',
#     '$12=0.002',
#     '$13=0',
#     '$20=0',
#     '$21=0',
#     '$22=0',
#     '$23=3',
#     '$24=250.000',
#     '$25=500.000',
#     '$26=250',
#     '$27=1.000',
#     '$100=80.000',
#     '$101=80.000',
#     '$102=84.926',
#     '$110=8000.000',
#     '$111=8000.000',
#     '$112=8000.000',
#     '$120=4000.000',
#     '$121=4000.000',
#     '$122=4000.000',
#     '$130=200.000',
#     '$131=200.000',
#     '$132=15.000',
# )

class AutoMachine:

    def __init__(self, port: str, rate: int = 115200, check_control: bool = False):
        # 打开串口
        self.serial = s.Serial(port, rate, timeout=0.5)  # /dev/ttyUSB0
        if self.serial.isOpen():
            print("Open port success")
        else:
            print("Open port failed")
        time.sleep(2)

        if self.recv() == b"\r\nGrbl 0.9j ['$' for help]\r\n":  # 连接成功会返回欢迎词
            print("Connected machine successfully")
        else:
            print("Connection fail or connect to another machine")

        check_setting_commands = '$$'  # 测试发送命令, 用于检查参数, 但写字机参数已经写入固件, 所以只需检查无需再次设置
        self.serial.write(bytes(check_setting_commands + '\n', encoding='ascii'))
        time.sleep(3)
        para = self.recv()  # 返回的参数太长了, 这里就不判断了, 但不获取的话会影响下一个命令返回值的获取, 所以这里必有获取一下
        # print(para)

        print("init machine")
        gcode_init_commands2 = (
            'G21',  # set mm units
            'G90',  # set absolute coordinates
            'G28',  # home all axes
        )

        for gic2 in gcode_init_commands2:
            # print("Sending Gcode: ", gic2)
            self.serial.write(bytes(gic2 + '\n', encoding='ascii'))
            time.sleep(3)  # 不知道是不是写字机MCU速度慢, 如果命令发送太快, 虽然返回OK, 但有可能会不被执行, 所以这里要设置等待
            if self.recv() != b'ok\r\n':
                print('fail on {0}'.format(gic2))

        print("Set distance unit to mm, set positioning to absolute completed")

        if check_control:  # 初始化后简单测试能否控制笔的三轴移动
            x_pos, y_pos, z_pos = self.get_current_position()
            changing_pos = (10.0, 0.0)
            print("Checking pen control")
            time.sleep(5)
            for cp in changing_pos:
                index = 0
                axis = (x_pos, y_pos, z_pos)
                gcode_init_xyz_commands = (
                    'G1X{0}F1000.0'.format(x_pos + cp),
                    'G1Y{0}F1000.0'.format(y_pos + cp),
                    'G1Z{0}F1000.0'.format(y_pos + cp)
                )
                for gic_xyz in gcode_init_xyz_commands:
                    print("Checking {0}-axis".format(gic_xyz[2]))
                    self.serial.write(bytes(gic_xyz + '\n', encoding='ascii'))
                    time.sleep(3)
                    if self.recv() != b'ok\r\n':
                        print('fail on {0}'.format(gic_xyz))
                    position = self.get_current_position()
                    if position[index] != axis[index] + cp:
                        print("fail on target position {0} by current position is {1}".format(gic_xyz, position))

    def recv(self):
        """
        获取串口返回值
        :return:
        """
        while True:
            data = self.serial.read_all()
            if data == '':
                continue
            else:
                break
        return data

    def get_current_position(self):
        """
        获取笔当前位置
        :return: x, y, z三轴所在位置
        """
        gcode_status_command = '?'
        # print("Sending Gcode: ", gcode_status_command)
        self.serial.write(bytes(gcode_status_command + '\n', encoding='ascii'))
        time.sleep(0.5)
        response = self.recv()
        response = response.decode(encoding='utf-8').split(',')
        x_position = response[1].split(":")[1]
        y_position = response[2]
        z_position = response[3]
        return float(x_position), float(y_position), float(z_position)

    def pen_up_down(self, position: float = 0.0, speed: float = 1000.0):
        """
        控制落笔与抬笔
        :param position:  笔的上下位置, 在绝对坐标系体系里可以设置为0 ~ 14, 其中0.0为最低(初始位置), 14为最高
        :param speed:  笔上下移动的速度, 可以设置为0.0 ~ 10000.0, 如果低于500.0速度会很慢, 如果高于5000.0速度实际上好像没分别
        :return: 无
        """
        # G1 命令的作用为线性(单向移动), 即只允许有一个方向的参数, 一般来说因为落笔抬笔时笔的位置已设置好, 所以这时一般用G1
        # 具体可以参考 https://www.simplify3d.com/support/articles/3d-printing-gcode-tutorial/
        gcode_pen_down_command = 'G1Z{0}F{1}'.format(position, speed)
        print("Sending Gcode: ", gcode_pen_down_command)
        self.serial.write(bytes(gcode_pen_down_command + '\n', encoding='ascii'))
        time.sleep(2)
        if self.recv() != b'ok\r\n':
            print('fail')

    def pen_move_to(self, x_position: float = 0.0, y_position: float = 0.0, speed: float = 1000.0):
        """
        控制笔左右移动(X-axis)与平台上下移动(Y-axis)
        :param x_position:  笔的左右位置, 可以设置为0 ~ 200, 其中0.0为最左(初始位置), 200.0为最右(靠近电机位置)
        :param y_position:  平台的上下位置, 可以设置为0 ~ 180, 其中0.0为最上(初始位置), 即最远离笔的位置, 180为最下(靠近电机位置)
        :param speed:  移动的速度, 可以设置为0.0 ~ 10000.0, 如果低于500.0速度会很慢, 如果高于5000.0速度实际上好像没分别
        :return: 无
        """
        # G90与G91都为三向移动, 即允许(也必须有)三个方向的参数, 这里为了定位方便使用的是G90(绝对坐标)
        # G90是绝对坐标, G91是相对坐标, 具体分别可以参照: https://gcodetutor.com/gcode-tutorial/g90-g91-gcode.html
        gcode_pen_move_command = 'G90X{0}Y{1}Z0.0F{2}'.format(x_position, y_position, speed)
        # print("Sending Gcode: ", gcode_pen_move_command)
        self.serial.write(bytes(gcode_pen_move_command + '\n', encoding='ascii'))
        time.sleep(2)
        if self.recv() != b'ok\r\n':
            print('fail')

    def pen_reset(self, reset_pattern: str = 'All'):
        """
        使笔回到原点
        :param reset_pattern: 可以是All, X, Y或者Z
        :return:
        """
        # G28 用于使笔归位, 默认是回到原点(0.0,0.0,0.0), 但也可以仅仅回复X, Y或者Z
        gcode_pen_reset_command = {'all': 'G28',
                                   'x': 'G28 X',
                                   'y': 'G28 Y',
                                   'z': 'G28 Z'
                                   }
        self.serial.write(bytes(gcode_pen_reset_command[reset_pattern.lower()] + '\n', encoding='ascii'))
        time.sleep(2)
        if self.recv() != b'ok\r\n':
            print('fail')

    def close_serial(self):
        """
        不使用自动书写机时请务必关闭COM口以免COM中被占
        :return:
        """
        self.serial.close()


if __name__ == '__main__':
    am = AutoMachine(port='COM3')
    time.sleep(5)  # 建议如果有移动笔的命令, 等待时间应该延长
    am.pen_up_down(position=5.0)
    time.sleep(5)
    am.pen_up_down(position=0.0)
    time.sleep(5)
    am.pen_reset()
    time.sleep(5)
    am.close_serial()
