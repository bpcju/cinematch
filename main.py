import requests
import pandas as pd

# 설정 (TMDB에서 발급받은 API 키를 입력하세요)
API_KEY = "3411864e47b9fdd5b811c78da2d33e0b"
BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies():
    """인기 영화 목록 조회"""
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("API 호출 실패:", response.status_code)
        return []

# --- 테스트 실행 ---
if __name__ == "__main__":
    print("=== 현재 인기 영화 Top 5 ===")
    populars = get_popular_movies()
    
    if populars:
        movie_list = []
        for m in populars[:5]:
            movie_list.append({
                "제목": m.get('title'),
                "개봉일": m.get('release_date'),
                "평점": m.get('vote_average')
            })
        
        df = pd.DataFrame(movie_list)
        print(df)