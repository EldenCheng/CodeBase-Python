

if __name__ == '__main__':

    response = b'<Idle,MPos:0.000,0.000,0.000,WPos:0.000,0.000,0.000>\r\nok\r\n'
    response = response.decode(encoding='utf-8').split(',')
    # response = response.split(',')
    x_position = response[1].split(":")[1]
    # x_position = response[1].split(":")
    y_position = response[2]
    z_position = response[3]
    print(x_position)
    print(y_position)
    print(z_position)

