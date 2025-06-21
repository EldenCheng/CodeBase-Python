#include <Servo.h>

#ifndef SERIAL_RATE
#define SERIAL_RATE         115200
#endif

#ifndef SERIAL_TIMEOUT
#define SERIAL_TIMEOUT      5
#endif

// 定义Servo对象来控制伺服电机, UNO R3开发板上有6个支持PWN的端口, 理论上可以支持6个伺服电机
Servo servo1st, servo2nd, servo3rd, servo4th, servo5th, servo6th;
Servo servoList[6] = {servo1st, servo2nd, servo3rd, servo4th, servo5th, servo6th};
Servo currentServo;
int outputNum = 0;
int servoNum = 0;
int currentAngle = 0;
int setAngle = 0;
int servoSpeed = 1;

//初始化,  当Arduino控制器通电或复位后，setup函数会运行一次。
void setup() {
    Serial.begin(SERIAL_RATE);
    Serial.setTimeout(SERIAL_TIMEOUT);

    // 初始化的时候, 读取串口输入确定使用多少个输出pin
    outputNum = readData();
    for (int i = 0; i < outputNum; i++) {
        // 读取串口获得端口的序号, 将对应端口设置为输出
        Serial.println("Please input output device type, 1 - 13 for normal output, 98 for Buildin LED and 99 for Servo");
        int outputPin = readData();
        if (outputPin == 99) {
          Serial.println("Please input servo init angel [0 ~ 180, by default about 90]");
          servoList[servoNum].write(readData());  // 初始化时先指定伺服电机的角度
          Serial.println("Please input servo port [3, 5, 6, 9, 10, 11]");
          servoList[servoNum].attach(readData());  // 指定伺服电机控制线连接的pin号
          servoNum++;
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

void(* resetFunc) (void) = 0; //用于Reset开发板的状态

//控制命令
void loop() {
    switch (readData()) {
        case 1 :
            //set digital low
            Serial.println("Please select which pin to control");
            digitalWrite(readData(), LOW);
            break;
        case 2 :
            //set digital high
            Serial.println("Please select which pin to control");
            digitalWrite(readData(), HIGH);
            break;
        case 3 :
            //get digital value
            Serial.println(digitalRead(readData())); break;
        case 4 :
            // set analog value, 0 ~ 1024
            Serial.println("Please select which analog to control");
            analogWrite(readData(), readData());
            break;
        case 5 :
            //get analog value
            Serial.println(analogRead(readData())); break;
        case 6 :
            // Set Servo angle
            if (servoNum == 1){
              currentServo = servoList[0];
              }
            else if (servoNum > 1){
              Serial.println("Please select which servo to control");
              currentServo = servoList[readData() - 1];
              }
            //set the servo angle
            Serial.println("Set servo angle from input");
            setAngle = readData();
            Serial.println("Set servo speed from input, the range is 1(fast) - 50(slow)");
            servoSpeed = readData();
            // Serial.println(servoSpeed);

            // 使舵机转动
            currentAngle = currentServo.read();
            if (setAngle > currentAngle) {
              for (int i = currentAngle; i <= setAngle; i++) {
                // Serial.println(i);
                currentServo.write(i);  // 舵机角度写入
                delay(servoSpeed); // 用于控制转动速度
                }
              }
            else {
                for (int i = currentAngle; i >= setAngle; i--) {
                // Serial.println(i);
                currentServo.write(i);
                delay(servoSpeed);
                }
              }

            break;
        case 7 :
            // Set Servo angle then let the Servo back to original angle after a while
            if (servoNum == 1){
              currentServo = servoList[0];
              }
            else if (servoNum > 1){
              Serial.println("Please select which servo to control");
              currentServo = servoList[readData() - 1];
              }
            //set the servo angle
            Serial.println("Set servo angle from input");
            setAngle = readData();
            Serial.println("Set servo speed from input, the range is 1(fast) - 50(slow)");
            servoSpeed = readData();
            // Serial.println(servoSpeed);

            // 使舵机转动
            currentAngle = currentServo.read();
            if (setAngle > currentAngle) {
              for (int i = currentAngle; i <= setAngle; i++) {
                // Serial.println(i);
                currentServo.write(i);  // 舵机角度写入
                delay(servoSpeed); // 用于控制转动速度
                }
              }
            else {
                for (int i = currentAngle; i >= setAngle; i--) {
                // Serial.println(i);
                currentServo.write(i);
                delay(servoSpeed);
                }
              }

            // 等待一段时间让舵机转到指定角度
            // 为了方便, 这里就不检测舵机是否转到指定角度, 而是根据servoSpeed设定等待值, 再+0.5秒
            delay(servoSpeed * 100 + 500);

            // 使舵机回位
            setAngle = currentAngle;
            currentAngle = currentServo.read();
            if (setAngle > currentAngle) {
              for (int i = currentAngle; i <= setAngle; i++) {
                // Serial.println(i);
                currentServo.write(i);  // 舵机角度写入
                delay(servoSpeed); // 用于控制转动速度
                }
              }
            else {
                for (int i = currentAngle; i >= setAngle; i--) {
                // Serial.println(i);
                currentServo.write(i);
                delay(servoSpeed);
                }
              }

            break;
        case 8 :
            //set the servos angle to 0, reset the Servos
            servo1st.write(0);
            delay(500);
            servo2nd.write(0);
            delay(500);
            servo3rd.write(0);
            delay(500);
            servo4th.write(0);
            delay(500);
            servo5th.write(0);
            delay(500);
            servo6th.write(0);
            delay(500);
            break;

        case 9 :
            //set the servos angle to 90, reset the Servos normal status
            servo1st.write(90);
            delay(500);
            servo2nd.write(90);
            delay(500);
            servo3rd.write(90);
            delay(500);
            servo4th.write(90);
            delay(500);
            servo5th.write(90);
            delay(500);
            servo6th.write(90);
            delay(500);
            break;
        case 10 :
            //get the servo current angle
            if (servoNum == 1){
              currentServo = servoList[0];
              }
            else if (servoNum > 1){
              Serial.println("Please select which servo to get");
              currentServo = servoList[readData() - 1];
              }
            currentAngle = currentServo.read();
            Serial.println(currentAngle);
            break;
        case 21 :
            //set build in LED low
            digitalWrite(LED_BUILTIN, LOW);
            break;
        case 22 :
            //set build in LED high
            digitalWrite(LED_BUILTIN, HIGH);
            break;
        case 51:
            //just dummy to cancel the current read, needed to prevent lock
            //when the PC side dropped the "w" that we sent
            break;
        case 91:
            //Reset the broad
            resetFunc();
            break;
        case 92:
            // Get the current output number, to check if the board is alreay initial
            Serial.println(outputNum);
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
              // Serial.println(result);
              return result;
            }
        }
    }
}