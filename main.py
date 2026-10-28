
import os
import sys
import urllib.parse
 
import pandas as pd
import requests
 
# .env 파일이 있으면 읽어오기 (python-dotenv 미설치여도 동작)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
 
# 설정
# 키는 코드에 직접 쓰지 않고 환경변수 또는 .env 파일(TMDB_API_KEY=키)에서 읽어옵니다.
# 설정 (.strip()을 붙여서 보이지 않는 공백이나 줄바꿈 문자를 제거합니다)
API_KEY = os.getenv("TMDB_API_KEY")
if API_KEY:
    API_KEY = API_KEY.strip()
BASE_URL = "https://api.themoviedb.org/3"
 
 
def check_api_key():
    """API 키가 있는지, 형식이 올바른지(32자리 16진수) 확인"""
    if not API_KEY:
        print("TMDB_API_KEY가 설정되지 않았습니다.")
        print("같은 폴더에 .env 파일을 만들고 TMDB_API_KEY=발급받은키 를 적어주세요.")
        sys.exit(1)
 
    is_hex = all(c in "0123456789abcdefABCDEF" for c in API_KEY)
    if len(API_KEY) != 32 or not is_hex:
        print("경고: API 키 형식이 올바르지 않아 보입니다 (32자리 16진수여야 함).")
        print(f"      현재 길이: {len(API_KEY)}자")
 
 
def get_popular_movies():
    """인기 영화 목록 조회"""
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("API 호출 실패:", response.status_code, response.text)
        return []
 
 
def get_genres():
    """전체 장르 목록 조회"""
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=ko-KR"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("genres", [])
    else:
        print("장르 목록 조회 실패:", response.status_code, response.text)
        return []
 
 
def get_movies_by_genre(genre_id):
    """특정 장르별 영화 조회"""
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=ko-KR&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("장르별 영화 조회 실패:", response.status_code, response.text)
        return []
 
 
def search_movies_by_keyword(keyword):
    """영화 제목 키워드 검색 (한글 인코딩 적용)"""
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={encoded_keyword}&language=ko-KR&page=1"
 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("영화 검색 실패:", response.status_code, response.text)
        return []
 
 
# --- 대화형 인터페이스 실행 ---
if __name__ == "__main__":
    check_api_key()
 
    while True:
        print("\n==============================")
        print("🎬 CineMatch 영화 추천 프로그램 🎬")
        print("==============================")
        print("1. 현재 인기 영화 Top 5 조회")
        print("2. 전체 장르 목록 보기")
        print("3. 특정 장르 영화 조회")
        print("4. 영화 키워드 검색")
        print("0. 프로그램 종료")
 
        choice = input("원하는 메뉴 번호를 입력하세요: ")
 
        if choice == '1':
            print("\n=== 현재 인기 영화 Top 5 ===")
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
 
        elif choice == '2':
            print("\n=== CineMatch 전체 장르 목록 ===")
            genres = get_genres()
            for g in genres:
                print(f"장르 이름: {g['name']} (ID: {g['id']})")
 
        elif choice == '3':
            genre_id = input("조회할 장르 ID를 입력하세요 (예: 28-액션, 35-코미디): ")
            movies = get_movies_by_genre(genre_id)
            if movies:
                movie_list = []
                for m in movies[:5]:
                    movie_list.append({
                        "제목": m.get('title'),
                        "개봉일": m.get('release_date'),
                        "평점": m.get('vote_average')
                    })
                df = pd.DataFrame(movie_list)
                print(f"\n=== 장르 ID {genre_id} 영화 Top 5 ===")
                print(df)
            else:
                print("해당 장르의 영화를 찾을 수 없습니다.")
 
        elif choice == '4':
            keyword = input("검색할 영화 제목을 입력하세요 (예: 어벤져스): ")
            movies = search_movies_by_keyword(keyword)
            if movies:
                movie_list = []
                for m in movies[:5]:
                    movie_list.append({
                        "제목": m.get('title'),
                        "개봉일": m.get('release_date'),
                        "평점": m.get('vote_average')
                    })
                df = pd.DataFrame(movie_list)
                print(f"\n=== '{keyword}' 검색 결과 Top 5 ===")
                print(df)
            else:
                print("검색 결과가 없습니다.")
 
        elif choice == '0':
            print("CineMatch 프로그램을 종료합니다. 수고하셨습니다!")
            break
        else:
            print("잘못된 입력입니다. 올바른 번호를 입력해주세요.")