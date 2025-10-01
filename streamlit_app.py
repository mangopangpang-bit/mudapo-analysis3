# streamlit_app.py
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("무대포 분석 - Streamlit 앱")
st.write("버튼 클릭으로 최신 축구 경기 데이터를 가져오고 분석합니다.")

# ---------------------------
# 1️⃣ 데이터 수집 함수 (웹 스크래핑)
# ---------------------------
def fetch_match_data():
    # 예시: 무료 축구 경기 일정 사이트 스크래핑
    url = "https://www.football-data.co.uk/englandm.php"  # 실제 사이트는 바꿔도 됨
    response = requests.get(url)
    if response.status_code != 200:
        st.error("데이터를 가져오는데 실패했습니다.")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 예시: 경기 테이블 스크래핑
    matches = []
    table = soup.find("table")  # 첫 번째 테이블
    if not table:
        st.warning("경기 데이터를 찾을 수 없습니다.")
        return pd.DataFrame()
    
    for row in table.find_all("tr")[1:]:  # 헤더 제외
        cols = row.find_all("td")
        if len(cols) >= 5:
            matches.append({
                "경기": cols[0].text.strip(),
                "팀A": cols[1].text.strip(),
                "팀B": cols[2].text.strip(),
                "점수A": int(cols[3].text.strip() or 0),
                "점수B": int(cols[4].text.strip() or 0)
            })
    return pd.DataFrame(matches)

# ---------------------------
# 2️⃣ 버튼 클릭 시 데이터 가져오기
# ---------------------------
if st.button("데이터 가져오기"):
    df = fetch_match_data()
    if not df.empty:
        st.success("데이터 로드 완료 ✅")
        st.dataframe(df)
        
        # ---------------------------
        # 3️⃣ 간단 분석: 승리팀 계산
        # ---------------------------
        df["승리팀"] = df.apply(
            lambda row: row["팀A"] if row["점수A"] > row["점수B"] else (row["팀B"] if row["점수B"] > row["점수A"] else "무승부"),
            axis=1
        )
        st.subheader("승리팀 분석")
        st.dataframe(df[["경기", "팀A", "팀B", "점수A", "점수B", "승리팀"]])
    else:
        st.warning("가져온 데이터가 없습니다.")
