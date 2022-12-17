var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
function startConnect() { // 접속을 시도하는 함수
    clientID = "clientID-" + parseInt(Math.random() * 100); // 랜덤한 사용자 ID 생성
    
    // 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
    broker = document.getElementById("broker").value; // 브로커의 IP 주소
    
    // id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
    // MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
    client = new Paho.MQTT.Client(broker, Number(port), clientID);
    
    // client 객체에 콜백 함수 등록
    client.onConnectionLost = onConnectionLost; // 접속이 끊어졌을 때 실행되는 함수 등록
    client.onMessageArrived = onMessageArrived; // 메시지가 도착하였을 때 실행되는 함수 등록
    
    // 브로커에 접속. 매개변수는 객체 {onSuccess : onConnect}
    // 객체의 프로퍼티는 onSuccess이고 그 값이 onConnect
    // 접속에 성공하면 onConnect 함수를 실행
    client.connect({
        onSuccess: onConnect,
    });
}

var isConnected = false;
// 브로커로의 접속이 성공할 때 호출
function onConnect() {
    isConnected = true;
    document.getElementById("connect").innerHTML += '<span>연결되었습니다.</span><br/>';
}

var topicSave;
function subscribe(topic) { // 'topic'으로 subscribe
if(client == null) return;
if(isConnected != true) {
    topicSave = topic;
    window.setTimeout("subscribe(topicSave)", 500);
    return
    }
    client.subscribe(topic); // 브로커에 subscribe
}

function publish(topic, msg) { // 토픽이 'topic'으로 된 msg를 브로커에게 보낸다
    if(client == null) return; // 연결되지 않았음
    client.send(topic, msg, 0, false);
    // 콘솔창에 출력
    console.log("publish: " + msg.destinationName + ": " + msg.payloadString);
}

function unsubscribe(topic) {
    if(client == null || isConnected != true) return;
    client.unsubscribe(topic, null); // 브로커에 subscribe
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // 매개변수인 responseObject는 응답 패킷의 정보를 담은 개체
    document.getElementById("connect").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("connect").innerHTML += '<span>오류 : ' +
        responseObject.errorMessage + '</span><br/>';
    }
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
    console.log("onMessageArrived: " + msg.destinationName + ": " + msg.payloadString);
    
    // 토픽이 "current"인 msg가 도착하면 그 값을 출력 (현재 인원수 값)
    if(msg.destinationName == "current")
        document.getElementById("current").innerHTML = '<span>' + msg.payloadString + '</span><br/>';
    
        // 토픽이 "possible"인 msg가 도착하면 그 값을 출력 (앞으로 탑승 가능한 인원수 값)
    if(msg.destinationName == "possible")
        document.getElementById("possible").innerHTML = '<span>' + msg.payloadString + '</span><br/>';
    
    // 토픽이 "congestion"인 msg가 도착하면 그 값을 출력 (혼잡도 값)
    if(msg.destinationName == "congestion") {
        var canvas = document.getElementById("myCanvas1"); // canvas에 혼잡도를 표시
        var ctx = canvas.getContext("2d");
        if(msg.payloadString == 0) { // 혼잡도가 '여유'인 경우
            ctx.clearRect(130, 0, 40, 40);
            ctx.clearRect(65, 0, 40, 40);
            ctx.beginPath();
            ctx.fillStyle = "green";
            ctx.arc(20, 20, 20, 0, Math.PI * 2, true);
            ctx.fill(); // 초록색 동그라미 그린다
        }

        else if(msg.payloadString == 1) { // 혼잡도가 '보통'인 경우
            ctx.clearRect(0, 0, 40, 40);
            ctx.clearRect(130, 0, 40, 40);
            ctx.beginPath();
            ctx.fillStyle = "yellow"; // 초록색 동그라미 그린다
            ctx.arc(85, 20, 20, 0, Math.PI * 2, true);
            ctx.fill(); // 노란색 동그라미 그린다
        }

        else { // 혼잡도가 '혼잡'인 경우
        ctx.clearRect(40, 0, 40, 40);
        ctx.clearRect(65, 0, 40, 40);
        ctx.beginPath();
        ctx.fillStyle = "red";
        ctx.arc(150, 20, 20, 0, Math.PI * 2, true);
        ctx.fill(); // 빨간색 동그라미 그린다
        }
    }
    // 토픽이 "temperature"인 msg가 도착하면 그 값을 출력 (온도 값)
    if(msg.destinationName == "temperature")
        document.getElementById("temp_message").innerHTML = '<span>' + msg.payloadString + '</span><br/>';

    // 토픽이 "humidity"인 msg가 도착하면 그 값을 출력 (습도 값)
    if(msg.destinationName == "humidity")
        document.getElementById("humid_message").innerHTML = '<span>' + msg.payloadString + '</span><br/>';

    // 토픽이 "image"인 msg가 도착하면 사진 출력
    if(msg.destinationName == "image")
        drawImage(msg.payloadString);

    // 토픽이 "brightness"인 msg가 도착하면 화면 야간모드
    if(msg.destinationName == "brightness") {
        var dark1 = document.getElementById("ent");
        var dark2 = document.getElementById("current");
        var dark3 = document.getElementById("possible");
        var dark4 = document.getElementById("temp_message");
        var dark5 = document.getElementById("humid_message");
        if(msg.payloadString < 200) { // 조도값이 200 미만이면 화면 배경을 어둡게, 글씨는 하얗게
            dark1.style.backgroundColor = "black";
            dark2.style.color = "white";
            dark3.style.color = "white";
            dark4.style.color = "white";
            dark5.style.color = "white";
        }
        else { // 조도값이 200이상이면 원래 상태대로 설정
        dark.style.backgroundColor = "linen";
        dark2.style.color = "black";
        dark3.style.color = "black";
        dark4.style.color = "black";
        dark5.style.color = "black";
        }
    }
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
    client.disconnect(); // 브로커에 접속 해제
    document.getElementById("connect").innerHTML += '<span>종료합니다.</span><br/>';
}