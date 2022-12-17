## 버스 혼잡도 경보 시스템 🚨
### 라즈베리파이를 이용한 버스 내 혼잡도 경보 시스템 <hr>

프로젝트 개발 기간 : 2021.11.01 ~ 2021.11.28<br>
프로젝트 개발 인원 : 1인
<hr>

## 📌 주요 기능 <hr>
1) 라즈베리파이를 연결하고 putty에 로그인을 한 다음, mosquitto를 백그라운드로 실행한다.
2) mqtt.py와 mqtt1.py를 백그라운드로 실행시킨 후, app.py를 실행한다.
3) 시크릿 창에서 IP주소를 입력하여 웹에 접속한다.
4) Connect 버튼을 클릭하여 브로커에 접속하면 다음과 같이 '연결되었습니다' 라는 문구가 출력된다.
<center><img width="40%" src="https://user-images.githubusercontent.com/68533847/208235662-b97103e0-b883-4a20-b65e-d84e510a670d.png"></center>
5) 버스 내 허용 인원수를 사용자가 입력하여 확인 버튼을 누른 후, 시작 버튼을 누르면 다음과 같이 현재 인원수와 앞으로 탑승 가능한 인원수가 출력된다.
<center><img width="40%" src="https://user-images.githubusercontent.com/68533847/208235721-d9e57423-4604-4066-8f19-0c4653a7c4e3.png"></center>


