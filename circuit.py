import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008 # 조도센서 사용을 위한 라이브러리
# 온/습도 센서
from adafruit_htu21d import HTU21D
import busio
# 초음파 센서에 대한 전역 변수 선언 및 초기화
trig1 = 20
trig2 = 26
echo1 = 16
echo2 = 5
sda = 2 # GPIO 핀 번호, sda라고 이름이 보이는 핀
scl = 3 # GPIO 핀 번호, scl이라고 이름이 보이는 핀
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c) # HTU21D 장치를 제어하는 객체 리턴
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)
GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)
GPIO.output(trig1, False)
GPIO.output(trig2, False)

# 초음파 센서
def measureDistance(getOnOff):
    global trig, echo
    
    if getOnOff == "on": # 승차에 대한 초음파 센서 trig, echo 설정
        trig = trig1
        echo = echo1
    elif getOnOff == "off": # 하차에 대한 초음파 센서 trig, echo 설정
        trig = trig2
        echo = echo2
    GPIO.output(trig, True) # 신호 1 발생
    time.sleep(0.00001) # 짧은 시간 후 0으로 떨어뜨려 falling edge 만듦
    GPIO.output(trig, False) # 신호 0 발생

    while(GPIO.input(echo) == 0):
        pass
    pulse_start = time.time() # 신호 1 -> 초음파 발생 시작
    while(GPIO.input(echo) == 1):
        pass
    pulse_end = time.time() # 신호 0 -> 초음파 수신 완료
    
    pulse_duration = pulse_end - pulse_start
    return 340*100/2*pulse_duration

# 온/습도 센서
def getTemperature() :
    return float(sensor.temperature) # HTU21D 장치로부터 온도 값 읽기
def getHumidity() :
    return float(sensor.relative_humidity) # HTU21D 장치로부터 습도 값 읽기

# LED 점등을 위한 전역 변수 선언 및 초기화
redLED = 13
whiteLED = 6

GPIO.setup(redLED, GPIO.OUT) # GPIO 13번 핀을 출력 선으로 지정
GPIO.setup(whiteLED, GPIO.OUT) # GPIO 6번 핀을 출력 선으로 지정

def turnOnRedLED(): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
    GPIO.output(redLED, True)

def turnOffRedLED(): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
    GPIO.output(redLED, False)

def turnOnWhiteLED(): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
    GPIO.output(whiteLED, True)

def turnOffWhiteLED(): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
    GPIO.output(whiteLED, False)

#부저에 대한 전역 변수 선언 및 초기화
buzzer = 18
GPIO.setup(buzzer, GPIO.OUT) # GPIO 18번 핀을 출력 선으로 지정

def buzzerOn():
    pwm = GPIO.PWM(buzzer, 262) # 262에 해당하는 특정 주파수로 음 설정
    pwm.start(50.0)
    time.sleep(1.5) # 1.5초 동안 부저 울림
    pwm.stop()

#조도센서
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

def getBrightness(): # 조도센서로부터 값을 얻는다
    return mcp.read_adc(0)