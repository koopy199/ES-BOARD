import requests
from bs4 import BeautifulSoup

# 관심 있는 법인명 리스트
keywords = ["사단법인 오늘은","펭귄의 날갯짓","하자센터","콜렉티브 꼼","크레타서점","우아한 형제들","열고닫기","소셜임팩트뉴스","282북스","사랑의열매","jyp엔터테인먼트"]

html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>주간 ES보드 뉴스 클리핑</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1 { text-align: center; color: #2c3e50; }
        h2 { color: #2980b9; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 40px; }
        li { margin-bottom: 10px; line-height: 1.5; }
        a { text-decoration: none; color: #1a0dab; font-size: 16px; }
        a:hover { text-decoration: underline; color: #d35400; }
    </style>
</head>
<body>
    <h1>📊 주간 ES보드 뉴스 클리핑</h1>
"""

for keyword in keywords:
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')

    html_content += f"    <h2>🏢 {keyword}</h2>\n    <ul>\n"

    for item in items[:5]:
        title = item.title.text
        link = item.link.text
        html_content += f"        <li><a href='{link}' target='_blank'>{title}</a></li>\n"
    
    html_content += "    </ul>\n"

html_content += """
</body>
</html>
"""

# 완성된 내용을 'weekly_news.html' 이라는 파일로 저장
with open("weekly_news.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("뉴스 수집 완료!")
