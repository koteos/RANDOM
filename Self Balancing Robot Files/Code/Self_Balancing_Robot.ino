#include "arduino_secrets.h"
#include <Adafruit_LSM6DS3TRC.h>
#include "thingProperties.h"

//Define setup variables for IMU using adafruit LSM6DS3 library
Adafruit_LSM6DS3TRC IMU;
Adafruit_Sensor *IMU_accel, *IMU_gyro;

//define specific IMU variables to be used with other parts of the code
float gyroX, gyroY, gyroZ; //raw x,y,z gyro values
float accelX, accelY, accelZ; //raw x,y,z accelerometer values
float gyroXDrift, gyroYDrift, gyroZDrift; //store steady state gyro values when IMU is held still (used for calibration of IMU)

float accelPitch, accelRoll; //pitch from accelerometer values alone
float gyroPitch, gyroRoll, gyroYaw; //pitch, roll, and yaw from gyroscope values alone (comment this out for final code. This is just for testing purposes.)

unsigned int timePrev, timeCurrent, timeDelta; //used to keep track of loop times for angle calculation
unsigned int timePrev2, timeCurrent2, timeDelta2; //used to keep track of loop times for PID control

//Kalman filter variables
float kalmanPitch = 0; //pitch angle after using the kalman filter. Initialize to 0 degrees, which is considered standing straight up
float kalmanPitchUncertainty; //pitch angle uncertainty after a kalman filter iteration
float accelUncertainty = 3; //Educated guess of the accelerometer angle uncertainty
float gyroUncertainty = 4; //Educated guess of the gyroscope angle per second uncertainty

//Motor variables
const int Motor1_Ena1 = 32;
const int Motor1_PWM1 = 33;
const int Motor1_PWM2 = 25;
const int Motor1_Ena2 = 26;
const int Motor2_Ena1 = 27;
const int Motor2_PWM1 = 14;
const int Motor2_PWM2 = 13;
const int Motor2_Ena2 = 23;

//7000*2^12 = 28,672,000 Hz < 40 MHz, so good to go.
const int PWM_Frequency = 7000;
const int PWM_Resolution = 12; //0 - 4095

void setup() {
  
  //Motor setup
  pinMode(Motor1_Ena1, OUTPUT);
  pinMode(Motor1_PWM1, OUTPUT);
  pinMode(Motor1_PWM2, OUTPUT);
  pinMode(Motor1_Ena2, OUTPUT);
  pinMode(Motor2_Ena1, OUTPUT);
  pinMode(Motor2_PWM1, OUTPUT);
  pinMode(Motor2_PWM2, OUTPUT);
  pinMode(Motor2_Ena2, OUTPUT);

  ledcSetup(0, PWM_Frequency, PWM_Resolution);
  ledcSetup(1, PWM_Frequency, PWM_Resolution);
  ledcSetup(2, PWM_Frequency, PWM_Resolution);
  ledcSetup(3, PWM_Frequency, PWM_Resolution);

  ledcAttachPin(Motor1_PWM1, 0);
  ledcAttachPin(Motor1_PWM2, 1);
  ledcAttachPin(Motor2_PWM1, 2);
  ledcAttachPin(Motor2_PWM2, 3);
  
  digitalWrite(Motor1_Ena1, LOW);
  ledcWrite(0, 0); //Motor1_PWM1
  ledcWrite(1, 0); //Motor1_PWM1
  digitalWrite(Motor1_Ena2, LOW);
  digitalWrite(Motor2_Ena1, LOW);
  ledcWrite(2, 0); //Motor1_PWM1
  ledcWrite(3, 0); //Motor1_PWM1
  digitalWrite(Motor2_Ena2, LOW);

  //Built in LED indicator
  pinMode(2, OUTPUT);
  
  // Initialize serial and wait for port to open:
  Serial.begin(115200);
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
 */
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  //If unable to communicate with IMU, don't proceed with program
  if (!IMU.begin_I2C()) {
    Serial.println("Failed to find LSM6DS chip");
    while (1) {
      delay(10);
    }
  }

  Serial.println("LSM6DS Found!");

  IMU_accel = IMU.getAccelerometerSensor();
  IMU_accel->printSensorDetails();

  IMU_gyro = IMU.getGyroSensor();
  IMU_gyro->printSensorDetails();

  
  calibrateIMU(3000); //calibrate the IMU for 3 seconds
  Serial.println("IMU calibrated!"); //Tell the user that the IMU is calibrated, with enthusiasm.
  
}

//Motor functions
void Motor_1_Speed(int speed) //speed ranging from -4095 to 4095 (negative is reverse, positive is forward)
{
  static int prev_Speed; //to keep track of motor direction. Saved across function calls

  if (prev_Speed*speed < 0 || speed == 0) //Only negative when speed and previous speed are different signs. If speed = 0, turn off MOSFETs
  {
    //turn off MOSFETs for 500 uS to prevent MOSFET shoot through
    digitalWrite(Motor1_Ena1, LOW);
    ledcWrite(0, 0); //Motor1_PWM1
    ledcWrite(1, 0); //Motor1_PWM2
    digitalWrite(Motor1_Ena2, LOW);
    delayMicroseconds(500);
  }

  if (speed < 0)
  {
    digitalWrite(Motor1_Ena1, HIGH);
    ledcWrite(1, constrain(abs(speed), 0, 4095)); //Motor1_PWM2
  }

  if (speed > 0)
  {
    digitalWrite(Motor1_Ena2, HIGH);
    ledcWrite(0, constrain(speed, 0, 4095)); //Motor1_PWM1
  }
  prev_Speed = speed; //save the current speed for next time function is called
}

void Motor_2_Speed(int speed) //speed ranging from -4095 to 4095 (negative is reverse, positive is forward)
{
  static int prev_Speed; //to keep track of motor direction. Saved across function calls

  if (prev_Speed*speed < 0 || speed == 0) //Only negative when speed and previous speed are different signs. If speed = 0, turn off MOSFETs
  {
    //turn off MOSFETs for 500 uS to prevent MOSFET shoot through
    digitalWrite(Motor2_Ena1, LOW);
    ledcWrite(2, 0); //Motor2_PWM1
    ledcWrite(3, 0); //Motor2_PWM2
    digitalWrite(Motor2_Ena2, LOW);
    delayMicroseconds(500);
  }

  if (speed > 0)
  {
    digitalWrite(Motor2_Ena1, HIGH);
    ledcWrite(3, constrain(speed, 0, 4095)); //Motor2_PWM2
  }

  if (speed < 0)
  {
    digitalWrite(Motor2_Ena2, HIGH);
    ledcWrite(2, constrain(abs(speed), 0, 4095)); //Motor2_PWM1
  }
  prev_Speed = speed; //save the current speed for next time function is called
}

void calibrateIMU(int calibrateTime)
{
  int iterations = 0;
  imuCalibrated = 0;
  ArduinoCloud.update();
  //take gyro values and sum them up over the time specified by calibrateTime
  for (int i = 0; i < calibrateTime; i++) //calibrate time is in mS
  {
    sensors_event_t accel;
    sensors_event_t gyro;
    IMU_accel->getEvent(&accel);
    IMU_gyro->getEvent(&gyro);
    
    gyroXDrift += gyro.gyro.x;
    gyroYDrift += gyro.gyro.y;
    gyroZDrift += gyro.gyro.z;
    delay(1);
    iterations++;
  }

  //take the average of the gyro drift values
  gyroXDrift /= iterations;
  gyroYDrift /= iterations;
  gyroZDrift /= iterations;
  imuCalibrated = 1;
  ArduinoCloud.update();
}

//Calculates the pitch and roll using accelerometer, gyroscope, and kalman filter, in degrees.
void calculateAngles()
{
  sensors_event_t accel;
  sensors_event_t gyro;
  IMU_accel->getEvent(&accel);
  IMU_gyro->getEvent(&gyro);

  //obtain raw IMU accelerometer values
  accelX = accel.acceleration.x;
  accelY = accel.acceleration.y;
  accelZ = accel.acceleration.z;

  //Keep track of loop times in milliseconds
  timeCurrent = millis();
  timeDelta = timeCurrent - timePrev;
  timePrev = millis();
  
  //obtain calibrated gyroscope values in degrees per second
  gyroX = (gyro.gyro.x - gyroXDrift)*(180/M_PI);
  gyroY = (gyro.gyro.y - gyroYDrift)*(180/M_PI);
  gyroZ = (gyro.gyro.z - gyroZDrift)*(180/M_PI);

  //obtain pitch and roll from accelerometer alone in degrees
  accelPitch = atan2(accelZ, sqrt(accelX*accelX + accelY*accelY))*(180/M_PI);
  //accelRoll = atan2(accelX, sqrt(accelY*accelY + accelZ*accelZ))*(180/M_PI); //comment this out for final code. This is just for testing purposes.

  //obtain pitch and roll from gyroscope alone in degrees (comment this out for final code. This is just for testing purposes)
  gyroPitch += gyroX/1000*timeDelta;


  //Calculate the pitch angle using Kalman filter. Function automatically updates kalmanPitch variable
  kalmanFilter(kalmanPitch, kalmanPitchUncertainty, gyroX, accelPitch, accelUncertainty, gyroUncertainty, timeDelta);
  pitchAngle = kalmanPitch; //update the dashboard

  //Serial monitor friendly format
  /*Serial.print("accelPitch: ");
  Serial.print(accelPitch);
  Serial.print(", accelRoll: "); //comment this out for final code. This is just for testing purposes.
  Serial.print(accelRoll); //comment this out for final code. This is just for testing purposes.
  Serial.print(", gyroPitch: "); //comment this out for final code. This is just for testing purposes.
  Serial.print(gyroPitch); //comment this out for final code. This is just for testing purposes.
  Serial.print(", gyroRoll: "); //comment this out for final code. This is just for testing purposes.
  Serial.print(gyroRoll); //comment this out for final code. This is just for testing purposes.
  Serial.print(", gyroYaw: "); //comment this out for final code. This is just for testing purposes.
  Serial.println(gyroYaw); //comment this out for final code. This is just for testing purposes.
  */

  //Serial plotter friendly format
  Serial.println(pitchAngle); //comment this out for final code. This is just for testing purposes.
}

void kalmanFilter(float &kalmanState, float &kalmanUncertainty, float kalmanInput, float kalmanMeasurement, float accelUncertainty, float gyroUncertainty, float timeStepMillis)
{
  float kalmanGain;
  kalmanState = kalmanState + timeStepMillis/1000*kalmanInput; //Calculate the initial prediction of the pitch angle
  kalmanUncertainty = kalmanUncertainty + pow((timeStepMillis/1000*gyroUncertainty), 2); //calculate the initial uncertainty prediction
  kalmanGain = kalmanUncertainty/(kalmanUncertainty + pow(accelUncertainty,2)); //calculate the kalman gain
  kalmanState = kalmanState + kalmanGain*(kalmanMeasurement - kalmanState); //Calculate the pitch angle from the kalman filter
  kalmanUncertainty = (1 - kalmanGain)*kalmanUncertainty; //Prepare for the next iteration step by calculating current uncertainty
}

//Controls for balance as well as user input for movement
void balanceControls()
{
  static float proportional;
  static float integral;
  static float derivative;
  static float signalOutput;
  static float currentAngle;
  static float previousAngle;
  
  calculateAngles();
  currentAngle = kalmanPitch;

  timeCurrent2 = millis();
  timeDelta2 = timeCurrent2 - timePrev2;
  timePrev2 = millis();

  //PID control signal calculation
  proportional = kP*(setPoint - currentAngle); //when tilted forward, angle is negative, so we want a positive output (forward signal)
  integral = constrain(integral + (kI*(setPoint - currentAngle)*timeDelta2), -4095, 4095); //when tilted forward, angle is negative, so we want to accumulate positive output (forward signal)
  derivative = -kD*(currentAngle - previousAngle)/timeDelta2; //when tilting towards level from foward tilt, angle difference is positive (pitching up), so want a negative signal to counteract P and I
 
  
  signalOutput = constrain(proportional+integral+derivative, -3895, 3895); //reserve 200 values for non-balancing movements
  //Only have outputs above 1500 or below -1500
  if (signalOutput < 1000 && signalOutput >= 0)
  {
    signalOutput = 1000;
  }
  if (signalOutput > -1000 && signalOutput <= 0)
  {
    signalOutput = -1000;
  }
  previousAngle = currentAngle;

  //Motor control
  if (forwardInput == 1)
  {
    Motor_1_Speed(signalOutput + 200);
    Motor_2_Speed(signalOutput + 200);
  }
  else if (reverseInput == 1)
  {
    Motor_1_Speed(signalOutput - 200);
    Motor_2_Speed(signalOutput - 200);
  }
  else if (rotateLeftInput == 1)
  {
    Motor_1_Speed(signalOutput - 200);
    Motor_2_Speed(signalOutput + 200);
  }
  else if (rotateRightInput == 1)
  {
    Motor_1_Speed(signalOutput + 200);
    Motor_2_Speed(signalOutput - 200);
  }
  else
  {
    Motor_1_Speed(signalOutput);
    Motor_2_Speed(signalOutput);
  }

  //if balance mode turned off, reset values
  if (balanceMode == 0)
  {
    proportional = 0;
    integral = 0;
    derivative = 0;
    signalOutput = 0;
    currentAngle = 0;
    previousAngle = 0;
  }
}

void loop() {
  ArduinoCloud.update();
  while (balanceMode == 1)
  {
    ArduinoCloud.update();
    balanceControls();
  }
  Motor_1_Speed(manualControl);
  Motor_2_Speed(manualControl);
}

/*
  Since Motor1F is READ_WRITE variable, onMotor1FChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onMotor1FChange()  {
  // Add your code here to act upon Motor1F change
}
/*
  Since Motor1R is READ_WRITE variable, onMotor1RChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onMotor1RChange()  {
  // Add your code here to act upon Motor1R change
}
/*
  Since Motor2F is READ_WRITE variable, onMotor2FChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onMotor2FChange()  {
  // Add your code here to act upon Motor2F change
}
/*
  Since Motor2R is READ_WRITE variable, onMotor2RChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onMotor2RChange()  {
  // Add your code here to act upon Motor2R change
}
/*
  Since CloudConnected is READ_WRITE variable, onCloudConnectedChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onCloudConnectedChange()  {
  // Add your code here to act upon CloudConnected change
}
/*
  Since ImuCalibrated is READ_WRITE variable, onImuCalibratedChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onImuCalibratedChange()  {
  // Add your code here to act upon ImuCalibrated change
}
/*
  Since KP is READ_WRITE variable, onKPChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onKPChange()  {
  // Add your code here to act upon KP change
}
/*
  Since KD is READ_WRITE variable, onKDChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onKDChange()  {
  // Add your code here to act upon KD change
}
/*
  Since KI is READ_WRITE variable, onKIChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onKIChange()  {
  // Add your code here to act upon KI change
}
/*
  Since ForwardInput is READ_WRITE variable, onForwardInputChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onForwardInputChange()  {
  // Add your code here to act upon ForwardInput change
}
/*
  Since ReverseInput is READ_WRITE variable, onReverseInputChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onReverseInputChange()  {
  // Add your code here to act upon ReverseInput change
}
/*
  Since RotateLeftInput is READ_WRITE variable, onRotateLeftInputChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onRotateLeftInputChange()  {
  // Add your code here to act upon RotateLeftInput change
}
/*
  Since RotateRightInput is READ_WRITE variable, onRotateRightInputChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onRotateRightInputChange()  {
  // Add your code here to act upon RotateRightInput change
}
/*
  Since BalanceMode is READ_WRITE variable, onBalanceModeChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onBalanceModeChange()  {
  // Add your code here to act upon BalanceMode change
}
/*
  Since CalibrateIMUState is READ_WRITE variable, onCalibrateIMUStateChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onCalibrateIMUStateChange()  {
  // Add your code here to act upon CalibrateIMUState change
  digitalWrite(Motor1_Ena1, LOW);
  ledcWrite(0, 0); //Motor1_PWM1
  ledcWrite(1, 0); //Motor1_PWM1
  digitalWrite(Motor1_Ena2, LOW);
  digitalWrite(Motor2_Ena1, LOW);
  ledcWrite(2, 0); //Motor1_PWM1
  ledcWrite(3, 0); //Motor1_PWM1
  digitalWrite(Motor2_Ena2, LOW);
  delay(1000);
  calibrateIMU(3000); //calibrate the IMU for 3 seconds
}
/*
  Since PitchAngle is READ_WRITE variable, onPitchAngleChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onPitchAngleChange()  {
  // Add your code here to act upon PitchAngle change
}
/*
  Since SetPoint is READ_WRITE variable, onSetPointChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onSetPointChange()  {
  // Add your code here to act upon SetPoint change
}
/*
  Since ManualControl is READ_WRITE variable, onManualControlChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onManualControlChange()  {
  // Add your code here to act upon ManualControl change
}