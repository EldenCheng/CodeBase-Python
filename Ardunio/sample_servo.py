from arduino import Arduino
import time

b = Arduino(port="COM5", baud_rate=115200)
device = {
    "Servo": [(90, 9)]
}

# declare output pins as a list/tuple
b.specify_output_device(device)

for i in range(1, 6):
    b.set_servo_angle(servo_index=1, angle=120, servo_speed=20)
    time.sleep(1)
    b.set_servo_angle(servo_index=1, angle=i * 10, servo_speed=20)
    time.sleep(1)

print(b.get_servo_angle(servo_index=1))

b.close()