import time
import paho.mqtt.client as mqtt
import circuit # 초음파 센서 입력 모듈 임포트

def on_connect(client, userdata, flag, rc):
    client.subscribe("permit", qos = 0) # "permit" 토픽을 mqtt에 등록하여 메시지 기다림

permit = 0 # 허용 인원수 전역 변수로 지정 및 초기화
poss = 0 # 탑승 가능 인원수 전역 변수로 지정 및 초기화

def on_message(client, userdata, msg) :
    msg = int(msg.payload)
    global permit, poss # permit, poss 전역 변수 이용
    permit = msg # mqtt로부터 받아온 값을 permit에 저장
    poss = msg # mqtt로부터 받아온 값을 poss에 저장

broker_ip = "localhost" # 현재 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect # 콜백 함수 등록
client.on_message = on_message # 콜백 함수 등록

client.connect(broker_ip, 1883)
client.loop_start()

curr = 0 # 현재 인원수(버스 내) 전역 변수로 지정 및 초기화
cong = 0 # 혼잡도 전역 변수로 지정 및 초기화

while(True):
    distance1 = circuit.measureDistance("on") # 탑승에 해당하는 초음파 센서로 거리 측정
    distance2 = circuit.measureDistance("off") # 하차에 해당하는 초음파 센서로 거리 측정
    
    if curr == 0 and poss == 0: # 현재 인원수와 탑승 가능한 인원수가 0명이면
        poss = permit # 탑승 가능한 인원수는 허용 인원수 값으로 설정

    if distance1 < 10: # 승차하면
        curr += 1 # 현재 인원수 1 증가
        poss -= 1 # 버스 내 허용 인원수 1 감소

        circuit.turnOnWhiteLED() # 흰색 LED on
        time.sleep(1) # 1초간 on
        circuit.turnOffWhiteLED() # 흰색 LED off

        if curr > permit: # 현재 인원수가 허용 인원수를 초과하면
            poss = 0 # 허용 인원수는 0명
            circuit.buzzerOn() # 부저가 울린다
            curr -= 1 # 현재 인원수는 1 감소 (승차하지 않는다)
    
    if distance2 < 10: # 하차하면
        curr -= 1 # 현재 인원수 1 감소
        poss += 1 # 버스 내 허용 인원수 1 증가
        
        circuit.turnOnRedLED() # 빨간색 LED on
        time.sleep(1) # 1초간 on
        circuit.turnOffRedLED() # 빨간색 LED off
        
        if poss <= 0: # 허용 인원수가 0보다 작거나 같으면
            poss = 0 # 0으로 지정
        
        if curr <= 0: # 현재 인원수가 0보다 작거나 같으면
            curr = 0 # 0으로 지정 (버스 내에 아무도 없음)
        poss = permit # 앞으로 탑승 가능한 인원수는 허용 인원수와 같게 됨
    
    cong1 = int(permit / 2) # 허용 가능한 인원수의 50%
    cong2 = int(permit * 80 / 100) # 허용 가능한 인원수의 80%

    if curr <= cong1: # 현재 인원수가 허용 가능한 인원수의 50% 이하이면
        cong = 0 # 혼잡도는 '여유' 상태 (0으로 설정)
    
    # 현재 인원수가 허용 가능한 인원수의 50% 초과, 80% 이하이면
    elif curr > cong1 and curr <= cong2:
        cong = 1 # 혼잡도는 '보통' 상태 (1로 설정)
    
    elif curr > cong2: # 현재 인원수가 허용 가능한 인원수의 80%를 넘으면
        cong = 2 # 혼잡도는 '혼잡' 상태 (2로 설정)
    
    # 현재 인원수 값을 'current' 토픽으로 mqtt에 보낸다
    client.publish("current", curr, qos=0)
    # 허용 인원수 값을 'possible' 토픽으로 mqtt에 보낸다
    client.publish("possible", poss, qos=0)
    # 혼잡도 값을 "congestion" 토픽으로 mqtt에 보낸다
    client.publish("congestion", cong, qos=0)
    
    # 측정된 온도값을 temperature 변수에 저장
    temperature = circuit.getTemperature()
    # 현재 온도 값을 "temperature" 토픽으로 mqtt에 보낸다
    client.publish("temperature", temperature, qos=0)
    
    # 측정된 습도값을 humidity 변수에 저장
    humidity = circuit.getHumidity()

    # 현재 습도 값을 "humidity" 토픽으로 mqtt에 보낸다
    client.publish("humidity", humidity, qos=0)
    
    # 측정된 조도값을 bright 변수에 저장
    bright = circuit.getBrightness()
    # 현재 조도 값을 "brightness" 토픽으로 mqtt에 보낸다
    client.publish("brightness", bright, qos=0)
    
    time.sleep(1)

client.loop_stop()
client.disconnect()