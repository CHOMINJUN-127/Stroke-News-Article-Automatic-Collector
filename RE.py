import csv
import time
import random
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def collect_stroke_news():
    """뇌졸중 뉴스 기사 38개를 자동으로 수집하여 CSV에 저장"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    articles = []
    page = 1
    search_term = "뇌졸중"
    
    print("뇌졸중 기사 38개를 수집 중입니다...")
    
    while len(articles) < 38:
        start = (page - 1) * 10 + 1
        url = f'https://search.naver.com/search.naver?where=news&query={quote_plus(search_term)}&start={start}'
        
        try:
            req = Request(url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            
            news_items = soup.select('.news_area')
            
            if not news_items:
                break
            
            for item in news_items:
                if len(articles) >= 38:
                    break
                
                try:
                    title_elem = item.select_one('.news_tit') or item.select_one('a.news_tit')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    link = title_elem.get('href', '')
                    
                    press_elem = item.select_one('.info_group .press')
                    press = press_elem.text.strip() if press_elem else '알 수 없음'
                    
                    date_elem = item.select_one('.info_group .info')
                    date = date_elem.text.strip() if date_elem else '날짜 없음'
                    
                    summary_elem = item.select_one('.news_dsc')
                    summary = summary_elem.text.strip() if summary_elem else '요약 없음'
                    
                    if not any(article[0] == title for article in articles):
                        articles.append([title, press, date, summary, link])
                        print(f"{len(articles)}. [{press}] {title[:50]}...")
                
                except Exception as e:
                    continue
            
            if len(news_items) < 10:
                break
                
            page += 1
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"페이지 {page} 오류: {e}")
            break
    
    # CSV 파일로 저장
    if articles:
        with open('뇌졸중 기사.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['제목', '언론사', '날짜', '요약', 'URL'])
            
            for article in articles:
                writer.writerow(article)
        
        print(f"\n✅ {len(articles)}개의 뇌졸중 기사를 '뇌졸중 기사.csv'에 저장했습니다!")
    else:
        print("❌ 기사를 찾을 수 없습니다.")

# 실행
collect_stroke_news()