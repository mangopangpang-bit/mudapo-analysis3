
import streamlit as st
import pandas as pd
import numpy as np

st.title("무대포 분석 - Streamlit 앱")
st.write("여기에 축구 데이터 분석 결과를 표시합니다.")

# 예시 데이터
data = {
    "경기": ["경기1", "경기2", "경기3"],
    "승리팀": ["팀A", "팀B", "팀C"],
    "점수": [2, 1, 3]
}
df = pd.DataFrame(data)

st.subheader("분석 결과")
st.table(df)

st.write("앱 배포 테스트 완료 ✅")
