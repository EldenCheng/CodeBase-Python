#include <Servo.h>

#ifndef SERIAL_RATE
#define SERIAL_RATE         115200
#endif

#ifndef SERIAL_TIMEOUT
#define SERIAL_TIMEOUT      5
#endif

Servo myservo;  // 定义Servo对象来控制伺服电机

void setup() {
    Serial.begin(SERIAL_RATE);
    Serial.setTimeout(SERIAL_TIMEOUT);

    // 初始化的时候, 读取串口输入确定使用多少个输出pin
    int outputNum = readData();
    for (int i = 0; i < outputNum; i++) {
        // 读取串口获得端口的序号, 将对应端口设置为输出
        int outputPin = readData();
        if (outputPin == 96) {
            Serial.println("Please input servo port");
            myservo.attach(readData());  // 指定伺服电机控制线连接的pin号
        }
        else if (outputPin == 98) {
            // Serial.println("Setup build in LED");
            pinMode(LED_BUILTIN, OUTPUT);
        }
        else {
            Serial.println("Setup Pin");
            pinMode(outputPin, OUTPUT);
        }
    }
}

void loop() {
    switch (readData()) {
        case 1 :
            //set digital low
            digitalWrite(readData(), LOW); break;
        case 2 :
            //set digital high
            digitalWrite(readData(), HIGH); break;
        case 3 :
            //get digital value
            Serial.println(digitalRead(readData())); break;
        case 4 :
            // set analog value
            analogWrite(readData(), readData()); break;
        case 5 :
            //read analog value
            Serial.println(analogRead(readData())); break;
        case 6 :
            //set the servo angle
            Serial.println("Set servo angle from input");
            myservo.write(readData());  // 舵机角度写入
            delay(1);                   // 等待转动到指定角度
            break;
        case 7 :
            //set the servo angle to 0
            myservo.write(0);
            delay(1);
            break;
        case 8 :
            //get the servo angle
            Serial.println(myservo.read()); break;
        case 97 :
            //set build in LED low
            digitalWrite(LED_BUILTIN, LOW);
            break;
        case 98 :
            //set build in LED high
            digitalWrite(LED_BUILTIN, HIGH);
            break;
        case 99:
            //just dummy to cancel the current read, needed to prevent lock
            //when the PC side dropped the "w" that we sent
            break;
    }
}

int readData() {
    /*
    输出"w"作为标志后, 一直循环等待客户端通过串口传输字符,在接收到字符后,解析出数字返回.
    注意, 在实际操作发现有些串口传输软件会添加\0, 0x之类的字符作为结束符, 这个方法会把这些结束符解析出数字0
    */
    Serial.println("w");
    while(1) {
        if(Serial.available() > 0) {
            int result = Serial.parseInt();
            if (result != 0){
              Serial.println(result);
              return result;
            }
        }
    }
}