import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# 1. 한국 시간 설정 및 7일 전 날짜 계산
tz_kst = timezone(timedelta(hours=9))
today = datetime.now(tz_kst)
week_ago = today - timedelta(days=7)

# 2. 화면에 보여줄 날짜 글씨 만들기
date_text = f"{week_ago.strftime('%Y년 %m월 %d일')} ~ {today.strftime('%Y년 %m월 %d일')}"

# 3. 요청하신 관심 법인명 리스트로 업데이트!
keywords = [
    "사단법인 오늘은", "사랑의열매", "소셜임팩트뉴스", "열고닫기", 
    "우아한 형제들", "콜렉티브 꼼", "크레타서점", "펭귄의 날갯짓", 
    "하자센터", "282북스", "jyp엔터테인먼트"
]

# 4. 타이틀을 '주간 ES보드 뉴스 클리핑'으로 변경
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>주간 ES보드 뉴스 클리핑</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #2c3e50; margin-bottom: 5px; }}
        .date-info {{ text-align: center; color: #7f8c8d; font-size: 15px; margin-bottom: 30px; font-weight: bold; }}
        h2 {{ color: #2980b9; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 40px; }}
        li {{ margin-bottom: 10px; line-height: 1.5; }}
        a {{ text-decoration: none; color: #1a0dab; font-size: 16px; }}
        a:hover {{ text-decoration: underline; color: #d35400; }}
    </style>
</head>
<body>
    <h1>📊 주간 ES보드 뉴스 클리핑</h1>
    <div class="date-info">🗓️ 수집 기간: {date_text}</div>
"""

for keyword in keywords:
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')

    html_content += f"    <h2>🏢 {keyword}</h2>\n    <ul>\n"

    # 5. 해당 주간에 뉴스가 없을 경우를 대비한 친절한 안내 문구 추가
    if not items:
         html_content += "        <li>이번 주 관련 뉴스가 없습니다.</li>\n"
    else:
        for item in items[:5]:
            title = item.title.text
            link = item.link.text
            html_content += f"        <li><a href='{link}' target='_blank'>{title}</a></li>\n"
    
    html_content += "    </ul>\n"

html_content += """
</body>
</html>
"""

# 완성된 내용을 파일로 저장
with open("weekly_news.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("주간 ES보드 뉴스 클리핑 수집 완료!")
