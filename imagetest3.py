from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>이미지 맵 테스트</title>
</head>
<body>
    <img src="static/images/image.jpg" usemap="#mapname" alt="이미지 설명">

    <map name="mapname">
        <area shape="rect" coords="34,44,270,350" href="https://example1.com" alt="영역 1">
        <area shape="circle" coords="337,300,44" href="https://example2.com" alt="영역 2">
        <area shape="poly" coords="67,36,324,45,289,183" href="https://example3.com" alt="영역 3">
    </map>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
