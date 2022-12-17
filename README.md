# 버스 혼잡도 경보 시스템 🚨
### 라즈베리파이를 이용한 버스 내 혼잡도 경보 시스템 <br><br>

프로젝트 개발 기간 : 2021.11.01 ~ 2021.11.28<br>
프로젝트 개발 인원 : 1인<br>

## 📌 주요 기능 <hr>
1) 라즈베리파이를 연결하고 putty에 로그인을 한 다음, mosquitto를 백그라운드로 실행한다.
2) mqtt.py와 mqtt1.py를 백그라운드로 실행시킨 후, app.py를 실행한다.
3) 시크릿 창에서 IP주소를 입력하여 웹에 접속한다.
4) Connect 버튼을 클릭하여 브로커에 접속하면 다음과 같이 '연결되었습니다' 라는 문구가 출력된다.
<img width="40%" src="https://user-images.githubusercontent.com/68533847/208235662-b97103e0-b883-4a20-b65e-d84e510a670d.png">

5) 버스 내 허용 인원수를 사용자가 입력하여 확인 버튼을 누른 후, 시작 버튼을 누르면 다음과 같이 현재 인원수와 앞으로 탑승 가능한 인원수가 출력된다.
<img width="40%" src="https://user-images.githubusercontent.com/68533847/208235721-d9e57423-4604-4066-8f19-0c4653a7c4e3.png">

6) 사람이 승차하게 되면 흰색 LED에 불이 켜지고 현재 인원수와 앞으로 탑승 가능한 인원수가 다음과 같이 조정된다. 혼잡도는 '여유' 상태인 초록색으로 표시된다.
<img width="50%" src="https://user-images.githubusercontent.com/68533847/208235853-b24ae21d-5d24-4326-8c62-922c694154d7.png">

7) 사람이 계속 승차하여 버스 내 현재 인원수가 허용 인원수의 80%를 넘게 되면 혼잡도는 '혼
잡' 상태인 빨간색으로 표시된다.
<img width="50%" src="https://user-images.githubusercontent.com/68533847/208235972-10b0acc3-597a-470e-b2a2-70ac488af143.png">

8) 버스 내 현재 인원수가 허용 인원수를 넘어서게 되면 경고음이 울린다.
<img width="50%" src="https://user-images.githubusercontent.com/68533847/208236002-ffd9778c-074b-46fb-9eb3-ec8fcfb8196c.png">

9) 버스 내 온도와 습도는 각각 측정과 중단 버튼을 통해 확인할 수 있다.
<img width="50%" src="https://user-images.githubusercontent.com/68533847/208236022-c23a89fb-149b-4f16-ae63-ad23617d6b1f.png">

10) Camera 버튼을 누르면 승차와 하차의 모습을 촬영하여 웹 브라우저에 보여준다.
<img width="511" src="https://user-images.githubusercontent.com/68533847/208236045-de194423-1c0f-446f-8553-2ef3d5c07dcb.png">