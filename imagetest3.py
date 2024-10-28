from flask import Flask, render_template_string, request, jsonify
import openai

# OpenAI API 키 설정 (본인의 OpenAI API 키를 사용하세요)
openai.api_key = ' '
app = Flask(__name__)

# HTML, CSS, JavaScript 포함된
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
            margin-right: 30px;
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

        /* 지도 스타일 */
        img[usemap] {
            border: 1px solid #ddd;
            max-width: 100%;
            height: auto;
            display: block; /* 이미지를 블록 요소로 변환 */
            margin: 0 auto; /* 블록 요소를 가운데 정렬 */
        }
        /* 이미지 맵 스타일 (마우스 오버 시 효과) */
        area:hover {
            cursor: pointer;
            outline: 2px solid #28a745;
        }
    </style>
</head>
<body>
    <header>
        <h1>서울시 피트니스 네트워크</h1>
        <nav>
            <ul>
                <li><a href="#home">미정</a></li>
                <li><a href="#search">미정</a></li>
                <li><a href="#trainers">미정</a></li>
                <li><a href="#community">미정</a></li>
            </ul>
        </nav>
    </header>

    <section id="home">
        <div class="banner">
            <h2>서울에서 최고의 피트니스 센터를 찾아보세요!</h2>
            <input type="text" placeholder="센터 검색...">
            <button onclick="search()">검색</button>
        </div>
   
        </div>
    </section>

    <!-- 서울특별시 지도 -->
    <section id="map">
      <div class="banner">
        <h2>서울특별시 지역 선택</h2>
        <img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzEwMDNfMjYy%2FMDAxNjk2MzI5NDU4Nzc2.aOCTdfY18de7L41hBjp9pYCZHF1wDKHaFaoaAZiVM8sg.3YLCSSm8RdNwOPhtFkSsgcQWy0Xsh-lwyfa6mSDTH40g.PNG.sunstory77%2Fimage.png&type=sc960_832" alt="서울특별시 지도" usemap="#seoul-map">

        <map name="seoul-map">
            <area target="" alt="강서구" title="강서구" href="강서.html" coords="129,256,34" shape="circle">
            <area target="" alt="양천구" title="양천구" href="" coords="180,332,28" shape="circle">
            <area target="" alt="은평구" title="은평구" href="" coords="289,148,34" shape="circle">
            <area target="" alt="도봉구" title="도봉구" href="" coords="438,95,23" shape="circle">
            <area target="" alt="노원구" title="노원구" href="" coords="501,136,24" shape="circle">
            <area target="" alt="강북구" title="강북구" href="" coords="416,140,21" shape="circle">
            <area target="" alt="중랑구" title="중랑구" href="" coords="526,195,26" shape="circle">
            <area target="" alt="강동구" title="강동구" href="" coords="599,270,22" shape="circle">
            <area target="" alt="송파구" title="송파구" href="" coords="548,346,24" shape="circle">
            <area target="" alt="성북구" title="성북구" href="" coords="416,201,25" shape="circle">
            <area target="" alt="동대문구" title="동대문구" href="" coords="466,226,24" shape="circle">
            <area target="" alt="광진구" title="광진구" href="" coords="517,283,24" shape="circle">
            <area target="" alt="종로구" title="종로구" href="" coords="356,222,24" shape="circle">
            <area target="" alt="서대문구" title="서대문구" href="" coords="287,231,30" shape="circle">
            <area target="" alt="중구" title="중구" href="" coords="382,267,24" shape="circle">
            <area target="" alt="성동구" title="성동구" href="" coords="446,279,25" shape="circle">
            <area target="" alt="마포구" title="마포구" href="" coords="277,285,24" shape="circle">
            <area target="" alt="용산구" title="용산구" href="" coords="357,312,26" shape="circle">
            <area target="" alt="강남구" title="강남구" href="" coords="469,369,30" shape="circle">
            <area target="" alt="서초구" title="서초구" href="" coords="403,389,28" shape="circle">
            <area target="" alt="동작구" title="동작구" href="" coords="323,361,26" shape="circle">
            <area target="" alt="영등포구" title="영등포구" href="" coords="261,334,25" shape="circle">
            <area target="" alt="관악구" title="관악구" href="" coords="309,423,27" shape="circle">
            <area target="" alt="금천구" title="금천구" href="" coords="240,425,24" shape="circle">
            <area target="" alt="구로구" title="구로구" href="" coords="151,378,26" shape="circle">
            <!-- 다른 지역 추가 -->
        </map>
    </section>

    <section id="chatbot">
     <div class="banner">
        <h2>GYM 챗봇</h2>
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

# OpenAI API를 사용하여 사용자의 질문에 대한 응답 생성
def generate_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

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
