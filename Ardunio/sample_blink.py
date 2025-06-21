from arduino import Arduino
import time

if __name__ == '__main__':
    b = Arduino(port="COM5", baud_rate=115200)
    device = {
        "L": 98
    }

    # declare output pins as a list/tuple
    b.specify_output_device(device)

    for i in range(0, 30):
        b.set_build_in_led_low()
        time.sleep(0.5)
        b.set_build_in_led_high()

    b.close()

