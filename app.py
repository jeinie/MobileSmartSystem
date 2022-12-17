from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index(): # 첫 페이지는 display.html
    return render_template('display.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)