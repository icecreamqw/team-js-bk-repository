from flask import Flask, render_template_string, request, jsonify
import openai

# OpenAI API 키 설정 (본인의 OpenAI API 키를 사용하세요)
openai.api_key = ''

app = Flask(__name__)

# HTML, CSS, JavaScript 포함된 템플릿
template = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>서울시 피트니스 네트워크</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1rem;
            text-align: center;
        }
        nav ul {
            list-style: none;
        }
        nav ul li {
            display: inline;
            margin-right: 20px;
        }
        nav ul li a {
            color: white;
            text-decoration: none;
        }
        .banner {
            text-align: center;
            margin: 50px 0;
        }
        input[type="text"] {
            padding: 10px;
            width: 300px;
        }
        button {
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        .card-container {
            display: flex;
            justify-content: space-around;
            padding: 20px;
        }
        .card {
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 5px;
            text-align: center;
            padding: 10px;
        }
        .card img {
            max-width: 100%;
            height: auto;
        }
        footer {
            text-align: center;
            padding: 1rem;
            background-color: #333;
            color: #fff;
        }
        /* 챗봇 스타일 */
        .chat-container {
            margin: 20px;
        }
        .chat-box {
            width: 100%;
            height: 300px;
            border: 1px solid #ccc;
            padding: 10px;
            overflow-y: scroll;
        }
        .chat-input {
            margin-top: 10px;
            display: flex;
        }
        .chat-input input {
            width: 80%;
            padding: 10px;
        }
        .chat-input button {
            width: 20%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <header>
        <h1>서울시 피트니스 네트워크</h1>
        <nav>
            <ul>
                <li><a href="#home">홈</a></li>
                <li><a href="#search">챗봇</a></li>
                <li><a href="#trainers">커뮤니티</a></li>
                <li><a href="#community">마이 페이지</a></li>
            </ul>
        </nav>
    </header>

    <section id="home">
        <div class="banner">
            <h2>서울에서 최고의 피트니스 센터를 찾아보세요!</h2>
            <input type="text" placeholder="센터 검색...">
            <button onclick="search()">검색</button>
        </div>
    </section>

    <section id="featured">
        <h2>추천 피트니스 센터</h2>
        <div class="card-container">
            <div class="card">
                <img src="https://via.placeholder.com/300" alt="Fitness Center 1">
                <h3>헬스장 1</h3>
                <p>서울 강남구</p>
                <button>더보기</button>
            </div>
        </div>
    </section>

    <section id="chatbot">
        <h2>ChatGPT 챗봇</h2>
        <div class="chat-container">
            <div id="chat-box" class="chat-box">
                <p><strong>챗봇:</strong> 안녕하세요! 무엇을 도와드릴까요?</p>
            </div>
            <div class="chat-input">
                <input type="text" id="user-input" placeholder="질문을 입력하세요...">
                <button onclick="sendMessage()">전송</button>
            </div>
        </div>
    </section>

    <footer>
        <p>&copy; 2024 서울시 피트니스 네트워크</p>
    </footer>

    <script>
        function search() {
            alert('검색 기능이 곧 추가됩니다!');
        }

        // 챗봇 메시지 전송 함수
        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            const chatBox = document.getElementById('chat-box');
            const userMessage = `<p><strong>사용자:</strong> ${userInput}</p>`;
            chatBox.innerHTML += userMessage;
            document.getElementById('user-input').value = ''; // 입력란 초기화

            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput }),
            })
            .then(response => response.json())
            .then(data => {
                const botMessage = `<p><strong>챗봇:</strong> ${data.response}</p>`;
                chatBox.innerHTML += botMessage;
                chatBox.scrollTop = chatBox.scrollHeight; // 스크롤을 최신 메시지로 이동
            });
        }
    </script>
</body>
</html>
'''

# ChatGPT API를 호출하는 함수
def generate_response(user_input):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=user_input,
        max_tokens=100
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    return render_template_string(template)

# 사용자의 입력을 받아 ChatGPT 응답을 처리하는 라우트
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    bot_response = generate_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
